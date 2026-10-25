"""Hermes Handoff native plugin entry point (no registration-time I/O)."""
import copy
import json
import os
from pathlib import Path


def register(ctx):
    from hermes_constants import get_hermes_home
    from .server.hermes_handoff import HermesHandoff, TOOL_SCHEMA
    from .server.handoff_open import HandoffOpening, SafeRefusal, canonical_workspace, setup_cli, preflight_tools

    adapter = HermesHandoff(get_hermes_home())
    opening = HandoffOpening(adapter)
    schema = copy.deepcopy(TOOL_SCHEMA)
    properties = schema["parameters"]["properties"]
    properties["action"]["enum"] += ["prepare_open", "opening_status", "summarize"]
    properties.update(attempt_id={"type": "string"}, model={"type": "string"}, provider={"type": "string"})

    def observe(session_id=None, model=None, provider=None, **kwargs):
        try:
            opening.observe(session_id=session_id, model=model, provider=provider)
            attempt_id = os.environ.get("HERMES_HANDOFF_ATTEMPT")
            if attempt_id:
                opening.identify(attempt_id, session_id)
        except (ValueError, OSError):
            pass  # unavailable route is an explicit prepare error, never a default

    def handle(args, session_id=None):
        try:
            if not isinstance(args, dict):
                raise ValueError("arguments must be an object")
            action = args.get("action")
            if not isinstance(action, str):
                raise ValueError("action must be a string")
            if action in {"prepare_open", "opening_status", "summarize"}:
                allowed = {"action", "workspace", "attempt_id", "ref", "model", "provider"}
                if set(args) - allowed:
                    raise ValueError("unsupported argument")
                workspace = canonical_workspace(args.get("workspace"))
                adapter._session(session_id)
                if action == "opening_status":
                    result = opening.status(args.get("attempt_id"))
                    if result["workspace"] != workspace:
                        raise ValueError("wrong workspace")
                elif action == "prepare_open":
                    result = opening.prepare(args.get("ref"), args.get("workspace"), session_id,
                                             args.get("attempt_id"), model=args.get("model"), provider=args.get("provider"))
                else:
                    result = opening.summarize(session_id, args.get("workspace"), ctx.llm,
                                               model=args.get("model"), provider=args.get("provider"))
                return json.dumps(result, ensure_ascii=False)
            if action == "read" and "attempt_id" in args:
                if set(args) - {"action", "workspace", "ref", "attempt_id"}:
                    raise ValueError("unsupported read argument")
                result = opening.acknowledge(args["attempt_id"], session_id, args.get("workspace"), args.get("ref"))
                return json.dumps(result, ensure_ascii=False)
            return json.dumps(adapter.handle(args, session_id=session_id), ensure_ascii=False)
        except SafeRefusal as exc:
            return json.dumps({"error": "Hermes Handoff refused the operation", "error_type": "SafeRefusal",
                               "hint": str(exc)})
        except (ValueError, OSError) as exc:
            # Never echo filesystem paths, IDs or raw user input on failure.
            return json.dumps({"error": "Hermes Handoff refused the operation", "error_type": type(exc).__name__,
                               "hint": "Check exact host session, profile database, canonical state, ref/project binding and request_id conflict."})

    def cli_open(args):
        try:
            # Keep the host's selection; never defeat focus mode by forcing a
            # broader --toolsets list just to make this plugin available.
            preflight_tools(args.workspace)
            return opening.open_from_cli(args)
        except SafeRefusal as exc:
            print(str(exc))
            return 1
        except (ValueError, OSError):
            print("Hermes Handoff refused opening: check TTY, prepared attempt, profile/workspace/ref and route.")
            return 1

    ctx.register_hook("pre_api_request", observe)
    ctx.register_cli_command("handoff-open", "Open a prepared handoff in a new foreground session", setup_cli, cli_open)
    ctx.register_command("hh", lambda raw_args: "Create a handoff, then prepare_open with a stable attempt_id. Run hermes handoff-open REF --workspace PATH --attempt-id ID from another terminal; origin remains open. First turn waits for confirmation.",
                         description="Handoff opening instructions (not the native /handoff)")
    ctx.register_tool(name="hermes_handoff", toolset="hermes_handoff", schema=schema,
                      handler=handle, description=schema["description"])
    ctx.register_skill(name="handoff", path=Path(__file__).parent / "skills" / "hermes-handoff" / "SKILL.md",
                       description="Create or manually resume a semantic Hermes handoff with exact evidence and safe central storage.")

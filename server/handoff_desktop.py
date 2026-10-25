"""Desktop journal adapter. RPC and navigation remain in the public UI SDK.

No fake TTY, DB write, tool-policy override, automatic inference retry or TTL.
"""
import hashlib
import json

from .handoff_open import canonical_workspace, identifier, preflight_tools, profile_for_home, route


class HandoffDesktop:
    def __init__(self, opening):
        self.opening = opening

    def handle(self, body):
        allowed = {"action", "attempt_id", "source_session", "profile", "workspace", "runtime_session", "stored_session", "model", "provider"}
        if not isinstance(body, dict) or set(body) - allowed:
            raise ValueError("invalid Desktop request")
        action = body.get("action")
        opening = self.opening
        value = opening.status(body.get("attempt_id"))
        if (body.get("source_session") != value["source_session"] or
                body.get("profile") != profile_for_home(opening.adapter.home) or
                canonical_workspace(body.get("workspace")) != value["workspace"]):
            raise ValueError("wrong Desktop origin")
        opening.adapter._session(value["source_session"])
        if action == "status":
            return value
        if action == "claim":
            # TUI gateway normal selection uses platform_toolsets.cli; focus
            # detection itself is Desktop-specific. Do not broaden either.
            preflight_tools(value["workspace"], "desktop")
            if body.get("model") is not None or body.get("provider") is not None:
                selected = route(body.get("model"), body.get("provider"))
                if any(value[k] != selected[k] for k in selected):
                    digest = hashlib.sha256(json.dumps([value["attempt_id"], selected], sort_keys=True).encode()).hexdigest()
                    value = opening.prepare(value["ref"], value["workspace"], value["source_session"], "desktop-" + digest, **selected)
            value = opening._reserve(value["attempt_id"], value["workspace"])
            if body.get("model") is not None and any(value[k] != body[k] for k in ("model", "provider")):
                raise ValueError("already reserved with a different destination route")
            return {**value, "prompt": opening.prompt(value)}
        if action not in {"created", "submit_requested", "submitted", "opened"}:
            raise ValueError("unsupported Desktop action")
        runtime = identifier(body.get("runtime_session"))
        stored = identifier(body.get("stored_session"))
        if runtime == stored or stored == value["source_session"]:
            raise ValueError("runtime and persistent identity must differ from origin")
        with opening.store._lock():
            value = opening.status(value["attempt_id"])
            if value["status"] not in {"launch_requested", "session_identified", "handoff_read"}:
                raise ValueError("Desktop attempt not reserved")
            if value.get("desktop_runtime_session") not in (None, runtime) or value.get("desktop_stored_session") not in (None, stored):
                raise ValueError("Desktop identity conflict")
            if action in {"submitted", "opened"}:
                # SessionDB persists parent/cwd on submit, not session.create.
                # Check before accepting the receipt, including opened retries.
                opening._validate_destination(value, stored)
            phase = value.get("desktop_phase")
            expected = {"created": None, "submit_requested": "created", "submitted": "submit_requested", "opened": "submitted"}
            # No replay of submit_requested: a lost response is uncertain, not
            # permission to send a second prompt. Opening an existing tab is safe.
            if action == "opened" and phase == "opened":
                return value
            if phase != expected[action]:
                raise ValueError("Desktop phase conflict; manual recovery required")
            value.update(desktop_runtime_session=runtime, desktop_stored_session=stored, desktop_phase=action)
            opening._write("attempt", value["attempt_id"], value)
        if action == "submitted":
            return opening.identify(value["attempt_id"], stored)
        return value

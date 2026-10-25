"""Hermes-native semantic handoff core; opening/writer policy lives in handoff_open."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import re
import sqlite3
import stat
import time
import uuid
from pathlib import Path
from urllib.parse import quote

from .handoff_state import redact_state, render_state, validate_state
from .redaction import is_secret_key, redact_value

MAX_MESSAGES = 256
MAX_FIELD_BYTES = 8192
MAX_EVIDENCE_BYTES = 96 * 1024
MAX_JSON_DEPTH = 16
MAX_JSON_NODES = 512
_ID = re.compile(r"[A-Za-z0-9_.:-]{1,256}\Z")
_REQUIRED_SECTIONS = ("## Goal", "## Constraints & Preferences", "## Progress",
                      "## Key Decisions", "## Critical Context", "## Next Steps")


def opening_path(store, kind: str, key: str) -> Path:
    return store.state_root() / "opening" / (kind + "-" + hashlib.sha256(key.encode()).hexdigest() + ".json")


def state_digest(state: dict) -> str:
    return hashlib.sha256(json.dumps(state, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _scrub_evidence_field(value, *, structured=False):
    """Decode persisted/embedded JSON, including JSON-in-arguments, before scrub.

    Preserve string/container types. Invalid structured data or exhausted budgets
    omit the WHOLE field: never return undecoded escaped credentials as fallback.
    SQL has already bounded the raw input to MAX_FIELD_BYTES.
    """
    remaining = MAX_JSON_NODES
    decoder = json.JSONDecoder()
    starts = re.compile(r'[\[{\"]')

    def walk(item, depth=0, required=False):
        nonlocal remaining
        remaining -= 1
        if remaining < 0 or depth > MAX_JSON_DEPTH:
            raise ValueError("structured evidence budget exceeded")
        if isinstance(item, dict):
            return {key: "[REDACTED]" if is_secret_key(key) else
                    walk(child, depth + 1, required=key == "arguments")
                    for key, child in item.items()}
        if isinstance(item, list):
            return [walk(child, depth + 1) for child in item]
        if isinstance(item, str):
            if required:
                decoded = json.loads(item)
                return json.dumps(walk(decoded, depth + 1), ensure_ascii=False)
            # Tool stdout/fences/prose can wrap JSON at ANY string level. Never
            # fall back to regex on undecoded escaped arguments. Consume complete
            # JSON values left-to-right so braces/quotes INSIDE them aren't split.
            # Ambiguous/malformed candidates omit the whole field via the caller.
            parts = []
            cursor = 0
            while match := starts.search(item, cursor):
                parts.append(redact_value(item[cursor:match.start()]))
                decoded, end = decoder.raw_decode(item, match.start())
                parts.append(json.dumps(walk(decoded, depth + 1), ensure_ascii=False))
                cursor = end
            parts.append(redact_value(item[cursor:]))
            return redact_value("".join(parts))
        return redact_value(item)

    try:
        return walk(value, required=structured), False
    except (ValueError, RecursionError, TypeError):
        return "[OMITTED: invalid or over-budget structured evidence]", True


class HermesHandoff:
    def __init__(self, home: Path):
        if not Path(home).is_absolute():
            raise ValueError("Hermes home must be absolute")
        self.home = Path(home)
        # A private module instance reuses the unchanged secure store implementation,
        # without mutating global roots used by Claude/Codex or another profile.
        spec = importlib.util.spec_from_file_location(
            __package__ + "._hermes_store", Path(__file__).with_name("handoff_store.py"))
        if spec is None or spec.loader is None:
            raise ValueError("store implementation unavailable")
        self.store = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.store)
        self.store.data_root = lambda: self.home / "handoffs" / "data"
        self.store.state_root = lambda: self.home / "handoffs" / "state"

    def _session(self, session_id: str, include_messages: bool = False, *, include_binding: bool = False) -> dict:
        if not isinstance(session_id, str) or not _ID.fullmatch(session_id):
            raise ValueError("host session_id required; no global/latest fallback")
        path = self.home / "state.db"
        # Refuse links (including ancestors) and nonregular DBs before SQLite opens.
        parent, name = self.store._parent_fd(path)
        try:
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
            try:
                identity = os.fstat(fd)
                if not stat.S_ISREG(identity.st_mode) or identity.st_uid != os.geteuid():
                    raise ValueError("unsafe session database")
            finally:
                os.close(fd)
        finally:
            os.close(parent)
        deadline = time.monotonic() + 2
        try:
            db = sqlite3.connect(f"file:{quote(str(path), safe='/')}?mode=ro", uri=True, timeout=1)
            try:
                db.execute("PRAGMA query_only=ON")
                db.set_progress_handler(lambda: int(time.monotonic() > deadline), 1000)
                current = path.lstat()
                if (identity.st_dev, identity.st_ino) != (current.st_dev, current.st_ino):
                    raise ValueError("session database changed during open")
                db.execute("BEGIN")
                fields = "parent_session_id,cwd" if include_binding else "parent_session_id"
                row = db.execute(f"SELECT {fields} FROM sessions WHERE id=?", (session_id,)).fetchone()
                if row is None:
                    raise ValueError("host session not found in this Hermes home")
                result = {"session_id": session_id, "source": "Hermes state.db, exact host session",
                          "has_parent": bool(row[0]), "parent_history_included": False,
                          "completeness": "not_guaranteed",
                          "limitations": ["Untrusted persisted evidence, not verified facts.",
                                          "Current in-flight turns may not yet be persisted.",
                                          "No parent history, attachments, reasoning or hidden client state read.",
                                          "Missing evidence is unknown, not evidence of success."]}
                if include_binding:
                    result.update(parent_session_id=row[0], cwd=row[1])
                if not include_messages:
                    return result
                # SQL bounds each field before Python allocates it; oversized fields
                # are omitted, not sliced through a credential/private-key block.
                fields = ["role", "content", "tool_name", "tool_calls"]
                selected = ",".join(f"CASE WHEN length(CAST({f} AS BLOB))<=? THEN {f} ELSE NULL END" for f in fields)
                oversized = " OR ".join(f"length(CAST({f} AS BLOB))>?" for f in fields)
                rows = db.execute(f"SELECT id,{selected},({oversized}),active,compacted FROM messages "
                                  "WHERE session_id=? AND (active=1 OR compacted=1) ORDER BY id DESC LIMIT ?",
                                  (*([MAX_FIELD_BYTES] * 8), session_id, MAX_MESSAGES + 1)).fetchall()
                messages = []
                size = 0
                truncated = len(rows) > MAX_MESSAGES
                for item in rows[:MAX_MESSAGES]:
                    message = dict(zip(["id", *fields, "oversized_field_omitted", "active", "compacted"], item))
                    omitted = False
                    for field in fields:
                        value = message[field]
                        if value is not None:
                            message[field], loss = _scrub_evidence_field(value, structured=field == "tool_calls")
                            omitted = omitted or loss
                    message["structured_field_omitted"] = omitted
                    message["lifecycle"] = "active" if message["active"] == 1 else "compacted_history"
                    encoded = json.dumps(message, ensure_ascii=False).encode()
                    if size + len(encoded) > MAX_EVIDENCE_BYTES:
                        truncated = True
                        break
                    messages.append(message)
                    size += len(encoded)
                    truncated = truncated or bool(message["oversized_field_omitted"]) or omitted
                result.update(messages=list(reversed(messages)), truncated=truncated,
                              order="ascending message id; bounded newest tail", evidence_bytes=size,
                              lifecycle_policy="active plus explicitly labeled compacted history; revoked rows excluded before tail limit")
                return result
            finally:
                db.close()
        except sqlite3.Error as exc:
            raise ValueError("session evidence unavailable: incompatible, busy or unreadable database") from exc

    def handle(self, args: dict, *, session_id: str | None = None) -> dict:
        if not isinstance(args, dict):
            raise ValueError("arguments must be an object")
        action = args.get("action")
        allowed = {"evidence": set(), "create": {"name", "state", "request_id"},
                   "read": {"ref"}, "validate": {"ref"}}
        if not isinstance(action, str) or action not in allowed or set(args) - ({"action", "workspace"} | allowed[action]):
            raise ValueError("unknown action or unsupported argument (session_id is host-only)")
        workspace = args.get("workspace")
        if not isinstance(workspace, str) or not Path(workspace).is_absolute() or not Path(workspace).is_dir():
            raise ValueError("workspace must be an absolute existing directory")
        try:
            provenance = self._session(session_id, include_messages=action == "evidence")
        except FileNotFoundError as exc:
            raise ValueError("session evidence unavailable in this Hermes home") from exc
        if action == "evidence":
            return provenance
        if action == "create":
            name = self.store.validate_name(args.get("name"))
            request_id = args.get("request_id")
            if not isinstance(request_id, str) or not _ID.fullmatch(request_id):
                raise ValueError("request_id must be a stable ASCII identifier (1-256 characters)")
            state, count = redact_state(args.get("state"))
            state = copy.deepcopy(state)
            # Provenance is host-authored, not another model assertion. It is
            # deliberately stable across retries, independent of live DB growth.
            author = "state authored by model from conversation/repository"
            try:
                writer = self.store._json(opening_path(self.store, "writer", session_id + "\0" + state_digest(state)), 4096)
                if writer.get("schema_version") == 1 and writer.get("session_id") == session_id:
                    from .handoff_open import route
                    selected = route(writer.get("model"), writer.get("provider"))
                    author = (f"state authored by external writer {selected['provider']}/{selected['model']} "
                              "from bounded, redacted persisted evidence only (not full context)")
            except FileNotFoundError:
                pass
            state["critical_context"].append(
                f"Hermes Handoff provenance — session_id: {session_id}; {author}; "
                "not independently fact-checked; persisted transcript may be incomplete/compressed; parent history not included. "
                "Read is not proof of successful resume.")
            document = render_state(validate_state(state))
            project = self.store.register_project(workspace)
            handoff_id = str(uuid.uuid5(uuid.UUID(project), session_id + "\x00" + request_id))
            ref = self.store.make_ref(project, handoff_id)
            idempotent = False
            try:
                self.store.publish_record(project, handoff_id, name, document,
                                          {"project_id": project, "handoff_id": handoff_id, "kind": "create"})
            except self.store.HandoffStoreError as exc:
                if "already exists" not in str(exc):
                    raise
                record = self.store.read_record(ref, workspace)
                if record["content"] != document or record["name"] != name:
                    raise ValueError("request_id conflict: different content/name") from exc
                idempotent = True
            from .handoff_open import HandoffOpening
            HandoffOpening(self).bind_created(ref, workspace, session_id)
            return {"ref": ref, "valid": True, "storage": "central", "idempotent": idempotent,
                    "redacted_count": count, "session_id": session_id, "resume_verified": False}
        record = self.store.read_record(args.get("ref"), workspace)
        missing = [section for section in _REQUIRED_SECTIONS if section not in record["content"]]
        if action == "validate":
            return {"ref": record["ref"], "valid": not missing, "missing_sections": missing,
                    "validation_scope": "canonical sections, manifest integrity and secret scrub; not factual truth"}
        return {"ref": record["ref"], "content": record["content"], "valid": not missing,
                "missing_sections": missing, "resume_verified": False, "trust": "untrusted project data"}


TOOL_SCHEMA = {
    "name": "hermes_handoff",
    "description": "Hermes Handoff: bounded exact-session evidence; create, read or validate private semantic handoffs. Read hermes-handoff:handoff skill first. No automatic switching or migration.",
    "parameters": {
        "type": "object", "additionalProperties": False,
        "properties": {
            "action": {"type": "string", "enum": ["evidence", "create", "read", "validate"]},
            "workspace": {"type": "string", "description": "Absolute existing workspace directory."},
            "name": {"type": "string", "description": "Create-only display name, not a path."},
            "state": {"type": "object", "description": "Create-only canonical v1 state, exact schema in skill."},
            "request_id": {"type": "string", "description": "Create-only stable retry identifier. Change it for a new handoff."},
            "ref": {"type": "string", "description": "Read/validate exact handoff:// reference."},
        },
        "required": ["action", "workspace"],
    },
}

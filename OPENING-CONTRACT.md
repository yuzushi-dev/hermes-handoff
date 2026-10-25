# Opening contract v1 — Hermes Handoff 0.2

This is the plugin-owned terminal contract, shared by the v0.3 Desktop adapter.
The terminal path does not call Desktop RPC; the Desktop contract separately
distinguishes durable session IDs from UI/runtime IDs.

## Immutable identity and binding

Creation (HermesHandoff.handle, action=create) publishes the existing immutable
record, then writes an origin sidecar under the same profile's handoffs/state/opening.
The origin sidecar contains schema_version=1, exact ref, canonical absolute workspace,
exact source_session and home. Only host-bound creation writes it. A create retry
repairs a crash between publication and binding; another session cannot reassign
that origin. Pre-0.2 refs still support manual read/validate, not inferred opening.

HandoffOpening.prepare(ref, workspace, host_session_id, attempt_id, model=None,
provider=None) returns a JSON object with:

    schema_version: 1
    attempt_id: stable caller-supplied ASCII ID
    ref: exact immutable handoff://PROJECT/HANDOFF
    workspace: canonical absolute existing directory (exact origin workspace)
    home: exact originating Hermes home
    profile: explicit CLI selector (default for custom roots)
    source_session: host session ID, verified in this home's state.db (read only)
    model: explicit or latest pre_api_request-observed model for source_session
    provider: explicit or observed provider (never auto/profile fallback)
    status: prepared
    destination_session: null
    resume_verified: false

Model/provider overrides are a pair. Missing observed route fails closed. Attempt
ID + changed contract is a conflict. prepare validates profile, source origin,
workspace and project/ref binding before state is written. The CLI requires an
existing prepared attempt; it never guesses the latest session or creates one from a ref.
A previously prepared attempt retains its route snapshot even if the source changes.
A new attempt prepared later sees the source's new observed route.

open_from_cli(args, tty=None, runner=None) is the testable frontend adapter. A CLI
route override derives ID cli-SHA256(JSON([original_attempt_id, selected_route],
sort_keys=True)); the full original ID participates, even at its 256-character limit.
Same CLI args reuse this ID; the prepared snapshot is unchanged. Partial routes or
ref mismatch fail before spawn. launch accepts injectable tty/runner; production
uses real stdin/stdout TTY and subprocess.run without a shell. Duplicate launch
prints status/manual action=read instructions and returns 3, no process creation.
Exit 1 is refusal/spawn failure; 0 is normal child exit, NOT successful resume.
Other child exit codes propagate. Read journal status independently of exit code.

## Durable reservation and destination acknowledgement

claim(attempt_id, workspace, tty=True) reserves a single launch for the ref BEFORE
any process creation. tty=False fails. Duplicate/restarted claims return the existing
attempt plus duplicate=true; this applies even if another attempt ID is supplied.
Do not spawn when duplicate=true. No global/latest source fallback, TTL or silent
relaunch. Reservation may exist with prepared status if the process dies between
the two journal writes: it still blocks a duplicate. No automatic journal pruning.

CLI launch inherits a real foreground TTY. It uses list argv, same HERMES_HOME,
explicit --profile even for default/custom roots to defeat sticky active_profile,
the installed public hermes console executable on PATH (not python -m, which may
double-import the entry module and re-apply sticky profile selection),
--in, explicit --model/--provider, --cli, preloaded handoff skill
and --query bootstrap. No --resume/--continue/--oneshot, /new, shell, origin close,
state.db write or gateway injection. Kanban/single-query/session markers,
HERMES_YOLO_MODE, HERMES_NONINTERACTIVE and gateway-only HERMES_TUI_TOOLSETS are
removed from the child environment. Normal profile approvals/configuration/auth
stay host-owned; explicit profile approval settings are not overridden.
No --toolsets override is passed and no tools are auto-enabled: normal profile
selection, disabled tools, coding posture and MCP discovery remain host-owned.
hermes_handoff must already be enabled for normal CLI chat. The CLI frontend uses
host coding_selection/load_config/resolve_toolset and normal platform resolver
to refuse a coding posture that excludes the handoff tool BEFORE claim or spawn;
four runtime-internal imports remain validator warnings, not public plugin APIs.
It never escapes focus by
forcing a broader selection. Ad-hoc source-session toolset overrides are not copied.
The restricted-policy smoke compares actual destination schemas to a normal chat
in the same synthetic profile/workspace, checks terminal/execute_code/delegate/browser
are absent, kanban_show is present, and round-trips a real configured stdio MCP tool.

Public pre_api_request is an observer: only session/model/provider are persisted.
The child's HERMES_HANDOFF_ATTEMPT is correlated to its first exact session ID;
identify validates that session exists in the same profile and is not the source.
The first accepted destination wins. Lifecycle events are NOT transactions.

acknowledge(attempt_id, host_destination_session, workspace, ref) reads through the
unchanged reader, requires valid sections/integrity, binds the destination and records
handoff_read. It is used by tool read with attempt_id. Mismatched workspace/ref,
source-as-destination, and another destination are refused. Result includes:

    opening_status: handoff_read
    confirmation_required: true
    resume_verified: false

Statuses distinguish requested/identified/read, not successful work. If the child
returns, child_exit_code is recorded. An unidentified child becomes launch_failed
(nonzero) or exited_unread (zero). An identified/read session retains that evidence
with its exit code. A crash can leave an uncertain request permanently reserved.
Manual same-profile read/recovery is safe; deliberate automatic reopening requires
a fresh handoff, not wiping state or bypassing the reservation with a fresh ID.

## Bootstrap policy, not a sandbox

prompt(contract) includes only ref/workspace/attempt ID and fixed instructions:
read and validate, inspect real project rules/files read-only, summarize goal,
constraints/discrepancies/first step, then STOP and await user confirmation. Skills
and future adapters must keep this policy. Arbitrary model obedience is not guaranteed
by Python. The PTY smoke uses a scripted provider to exercise real behavior end-to-end,
not to certify the semantics of a live provider.

## Independent writer B

summarize(host_session, workspace, ctx.llm, model=None, provider=None): default
returns current_session instructions and makes zero auxiliary calls. Explicit pair
uses the public ctx.llm.complete facade with bounded redacted evidence, max_tokens8192,
timeout60 and purpose handoff-bounded-summary. No conversation, filesystem or tools
are passed. Result must be canonical valid state and is redacted again. It is returned
for inspection/create, not published automatically. Missing consent, unavailable
provider, invalid output or a reported route mismatch returns a generic refusal.
PermissionError (including PluginLlmTrustError) is caught BEFORE OSError/generic
handling and surfaces a fixed SafeRefusal naming config.yaml and both
plugins.entries.<plugin_id>.llm.allow_model_override / allow_provider_override.
Use hermes plugins list --json's key to verify the effective plugin ID.
Only session ID, validated writer route and canonical redacted state digest are
recorded in a writer sidecar (no evidence, prompt or payload). create with the exact
returned state in that session records external writer PROVIDER/MODEL, bounded
redacted evidence and not-full-context provenance. Changed state/other sessions
do not match the digest; ordinary no-writer provenance stays byte-identical to0.1.
No automatic plugin retry. Explicit repeated calls are potentially billable again.
Host retries/fallback remain host-owned; result attribution cannot independently
attest every provider's true model identity. Exact requested/reported route comparison
may conservatively reject canonical model aliases.

API verified on installed d923a5eb:
hermes_cli/plugins.py:377-384 (ctx.llm), agent/plugin_llm.py:446-458 (complete),
153-181 and498-519 (override trust gates),521-572 (result and host call),
hermes_cli/plugins.py:637-675 (CLI and slash registration),
agent/turn_api_request.py:63-87 (observer payload).
No profile/auth/task override is requested; only provider/model capabilities.

## Desktop adapter boundary (v0.3)

server/handoff_desktop.py reuses prepare/status/identify/acknowledge/prompt and the
journal, explicitly adapting the frontend precondition: Desktop is not a TTY. It
correlates runtime RPC and durable stored session IDs through the host SessionDB
reader. Sequence: public session.create -> prompt.submit -> host.openSession,
with durable transitions before each irreversible action. The native 5-minute
in-memory dedup cache is not this journal. No fake TTY or direct DB writes.
See DESKTOP-CONTRACT.md for profile/socket restrictions, validation and evidence.

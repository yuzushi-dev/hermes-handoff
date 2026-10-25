# Desktop opening contract — Hermes Handoff 0.3 candidate

Public-source context: source available for review/development; plugin release and
catalog listing pending. The isolation recipes and delivery notes below describe
historical private verification. Their smoke scripts, test helpers and artifacts
are not shipped in this native source repository. Do not substitute an active
user Desktop for the required isolated harness.

This adds an opt-in native Desktop plugin, not an npm/Claude launcher. Existing
CLI, refs, storage, redaction, canonical state and opening acknowledgements remain
compatible. No core patches, TTY impersonation or direct session database writes.

## UI and origin

After an authorized installation/enabling, the Desktop Handoff sidebar opens its
own route. Select an idle source chat on its own active profile gateway first.
Enter the absolute workspace. A (destination) and B (summary writer) are independent
model/provider pairs. Blank A means the exact source's last observed route, not the
profile default. Blank B means the current chat model prepares the state. B's
explicit override still needs the existing user-owned ctx.llm trust consent.

“Prepara handoff dalla chat” submits a fixed instruction with JSON parameters to
the EXACT captured source runtime: evidence, optional summarize(B), create, then
prepare_open(A). It does not run a separate hidden agent. Completion occurs in the
source chat; no blind polling/reinference. “Apri nuova sessione” consumes the frozen
attempt. An existing prepared attempt can be entered explicitly instead. A route
change at open derives a stable new attempt, without rewriting the original.

A persistent preparation receipt is saved BEFORE submit. A double click, reload
or uncertain response does not resubmit preparation/B. “Nuova preparazione (non
retry)” explicitly clears only the local UI receipt, never the journal or an old
reservation. It can cause another paid writer call; it is not automatic recovery.

captureOrigin uses the public SDK focusedSessionOwner, focusedStoredSessionId,
focusedSessionId, connectionId and profile. It rechecks these around async steps.
No latest/title/global-origin fallback and no automatic ensureAgent switch.

Important profile limitation: focusedSessionOwner.profile must equal
host.state.profile (the active socket's home), and its connection must match.
A named bot/profile chat focused through another profile's socket is REFUSED
BEFORE REST, reservation, create or submit, even if that is normal UI navigation.
It is NOT silently transferred to default. This conservative restriction keeps
REST and RPC tied to the same validated backend; cross-profile multiplexing is
not certified here. A matching named profile/socket is covered by SDK-stub
contract tests only; the observed real Desktop smoke uses a synthetic default
profile. Do not describe real named/bot support as verified.

## Supported lifecycle and durable refusal

The public SDK provides ctx.rest, host.request and host.openSession. Routes and
navigation use ROUTES_AREA/SIDEBAR_NAV_AREA; React and SDK are host-supplied.
Dashboard API: POST /opening?profile=CAPTURED_PROFILE with allowlisted actions.
The backend validates the profile/home, original source, exact workspace/ref and
real SessionDB session identities using read-only host methods.

1. Profile/tool policy preflight, before durable claim.
2. Reserve the v0.2 immutable-ref launch lock and create_requested phase.
3. session.create with captured profile, frozen model/provider/workspace, source
   parent_session_id, close_on_disconnect=false and a stable native idempotency key.
4. Persist both created runtime and durable stored IDs as provisional receipts;
   refuse source-as-target, swapped IDs or conflicting destination. No destination
   DB row is required at create time: the host persists it on prompt submission.
5. Persist submit_requested BEFORE prompt.submit to the runtime ID.
6. Require streaming + user_row_id receipt. Before accepting submitted, read the
   exact destination row from this home's SessionDB read-only and require its
   parent_session_id to equal the source and its canonical cwd to equal the frozen
   workspace. Missing row/columns/parent/cwd or invalid cwd fail closed without
   accepting submitted or binding the destination. The same check guards
   identify/first-turn acknowledgement and opened (including safe tab retries).
7. host.openSession on the stored ID with intent=tab; persist opened.

A completed retry only reopens the existing target tab. An uncertain phase,
crash or lost submit reply never creates/submits again; manual recovery is
required. A crash cannot be made exactly-once across network/DB boundaries.
The gateway's 300-second in-memory create cache is not relied on for durability.
No origin session.close is issued. Preparation intentionally adds a source turn;
opening/retry preserves source rows byte-for-byte, proven separately in smoke.

The first destination turn must read and validate the exact handoff, inspect
actual project rules/files, summarize discrepancies/next step, and WAIT FOR USER
CONFIRMATION. handoff_read records actual tool acknowledgement, not successful
continuation. resume_verified remains false. This is a model instruction, not a
sandbox or certification that arbitrary models obey it.

## Tool and MCP policy

No custom toolsets are passed on session.create. The installed gateway uses normal
CLI platform selection for a fresh Desktop agent, so the shared preflight uses
that same host resolver plus coding posture and disabled toolsets. It refuses
missing hermes_handoff, including a non-focus profile with an empty/file-only
selection, before claiming. HERMES_TUI_TOOLSETS gateway pins are conservatively
refused because the dashboard plugin cannot attest that override's effective
session policy. No profile config or tools are auto-enabled.

Observed restricted-profile Desktop smoke compares actual baseline/destination
tool schemas, requires equality, excludes terminal/execute_code/delegate/browser,
keeps kanban_show and round-trips a configured stdio MCP policy_canary. This is
runtime evidence, not a promise that source ad-hoc selections are transferred.

## Mandatory isolation for reviewers and reruns

The first historical boot2 probe used isolated HOME but not PID isolation. The
Hermes core reaper reported 16 orphan desktop-local backends reaped outside the
test. Impact cannot be reconstructed or declared harmless. Preserve the incident
logs; do not rerun that method, clean host processes or patch core as part of this
task. HOME/HERMES_HOME/XDG isolation ALONE IS NOT SAFE for launching Desktop.

The supported smoke invokes:
    unshare --user --map-root-user --pid --fork --mount-proc node scripts/smoke_handoff_desktop_ui.mjs NEW_ROOT SCENARIO

Before spawning Xvnc or Electron the UI driver requires PID=1, /proc/self -> 1,
/proc/1/cmdline identifying itself, and a PID namespace different from the
runner's. It writes isolation.json. Xvnc/Electron/gateway children are then confined
to that namespace/private process table. If unavailable: STOP, do not fall back.
Fault tests signal only explicitly identified processes within this namespace.
The historical boot probe now refuses nonisolated execution too; do not use it.
No installation or dependency changes are required on the verified machine.

Run through scripts/smoke_handoff_desktop.py, with installed Hermes Python,
PYTHONPATH pointing to Hermes source and HERMES_HOME/HOME pointing to the NEW
synthetic root from the start. Never directly launch the user Desktop. Scenarios:
normal (prepared handoff, default A/B), prepare (from actual source UI, explicit
separate A/B), crash (kill synthetic Electron immediately after create request,
restart/refuse duplicate), offline (suspend synthetic gateway/no create), policy
(profile excludes handoff/no claim or create). Socket guards allow loopback only.
All provider data are explicitly synthetic fixtures, not live model results.

Official API reference consulted:
https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk
Installed runtime refs: apps/desktop/src/sdk/index.ts, tui_gateway/methods_session.py,
tui_gateway/server.py, hermes_cli/tools_config.py; preflight needs the installed
private _get_platform_tools resolver because this version has no public equivalent.
This is a version-coupling risk. Installed Linux Hermes/Desktop only is certified.

## Delivery and nonclaims

artifacts/v0.3.0-review1 contains the native package/manifest, separate v0.3 source
hash manifest, command results, durable screenshots/DOM/frames/provider requests,
and incident evidence. Historical failed probes are not successful UI evidence.
Only the final verified run results are authoritative for the delivered snapshot.
No live/paid model quality, user-profile installation, other platforms/versions,
cross-profile gateway bots, publish, push, commit or deployment is claimed.
Review is Una; max two reworks as specified by the operator. Gates remain closed.

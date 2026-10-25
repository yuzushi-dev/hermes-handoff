# HANDOFF — Hermes Handoff

Distribution context: v0.3.0 is distributed through GitHub Releases;
catalog listing remains pending. The notes below are historical
private development records, not current authorizations or runnable instructions
for this 28-file repository. Their `artifacts/`, workspace, test and script paths
refer to separately retained private evidence/helpers, not files shipped here.
Local review of the native candidate passed; source availability is not installation.

## Current local fixes — task t_b7ae9f25

Current candidate evidence: artifacts/v0.3.0-ready-fixes. Desktop acceptance and
first-turn acknowledgement now independently check the persisted destination's
parent_session_id and canonical cwd, before binding or accepting submitted/opened.
Missing metadata fails closed; CLI policy and human confirmation are unchanged.
See DESKTOP-CONTRACT.md and docs/CANDIDATE-0.3.0.md for the current contract and
concordant 17-rule catalog policy. The reports below are historical execution
records, not current approval or evidence that dependency preparation passed.
Original media MIT/aesthetic approval and the passed native-candidate review are
separate from public-source review and the pending plugin release/catalog gates.

## v0.3 Desktop candidate — task t_1aa49c94

Modified locally against operator-approved v0.2 commit/tag d96467f1 /
hermes-handoff-v0.2.0. No new commit, stash/reset/checkout, push, publish or real
profile installation. Source hash manifest and verification commands/results:
artifacts/v0.3.0-review1. See DESKTOP-CONTRACT.md for UI, recovery and limitations.
The historical v0.2/v0.1 notes below are preserved; not v0.3 approval.

Observed UI smoke includes both opening a prepared handoff and actual preparation
from the source chat with independent synthetic A destination-model/B writer-model.
Read/validate/project-file/MCP tool calls are real through an actual Desktop/gateway;
provider text is explicitly scripted loopback data, not live semantic certification.
Named/bot focused chat on another profile's socket is intentionally REFUSED,
never rerouted to default. Matching named/socket is SDK-stub-tested only.

SAFETY INCIDENT: initial boot2 with isolated HOME but no PID namespace reported
16 orphan backends reaped by Hermes core. Impact unknown; user/operator informed.
Do not assert runtime user processes were untouched. Incident logs are preserved
under artifacts/v0.3.0-review1/incident. All subsequent real UI smoke must use the
new harness with PID namespace AND private /proc checks BEFORE spawning anything.
No host cleanup/kill or core correction. Review by Una, max two reworks per Gumi.

## Historical v0.2 candidate — task t_1d73b6f6

Modified locally; see HERMES-README.md and OPENING-CONTRACT.md for the new CLI,
independent writer B and Desktop boundary. Actual verification results are recorded
in the task transition and artifacts/v0.2.0-rework2-release (earlier release-check
is preserved, not current approval). Approved0.1 archive is
preserved unchanged. No commit/push/publish/real-profile installation or paid call.
The report below is the historical0.1 maker/rework handoff, not current approval.

v0.2 rework1 addresses Una/Gumi M1-M5: injectable launch with duplicate exit3;
testable CLI override via deterministic derived attempt; fixed safe trust hint
with real allow_*_override keys; session-scoped digest provenance for bounded
external writer, ordinary0.1 text unchanged; exclusive destination regression.
CLI now requires prepare_open first. Docs cover exit codes, recovery and plugin key.
No source-session close, profile configuration or original-repo modification.
Base0.1 commit d68d7ea was made by the operator, not this run; no new commit here.

v0.2 rework2 (last authorized rework) removes the explicit --toolsets override
found by Una round2. Normal profile tool/MCP policy is now resolved by the host,
not replaced by hermes-cli. No tools are added. CLI focus posture omitting handoff
is refused before claim/spawn using public coding_selection/load_config/resolve_toolset.
New restricted-policy smoke compares actual schemas to a normal same-profile chat,
requires kanban, forbids terminal/execute_code/browser/delegate and round-trips a
real synthetic stdio MCP server (scripts/smoke_policy_mcp.py; standard library only).
It also exercises actual focus-mode refusal. The original test and packaged rework1
smoke reproduced the tool-policy defect RED. An intermediate probe correctly failed
because the runtime SDK fixture lacked the mcp package; only the fixture was replaced,
not the core or its MCP client. No runtime installation/config change or paid call.
Current evidence/commands/hashes are in the rework2 review handoff. Not approval.
The first final-check directory (v0.2.0-rework2-final) is preserved as a FAILED
environment probe: AF_UNIX path too long and optional MCP missing from the bootstrap
venv when HOME is isolated. The verifier now reads the installed dependency generation
before isolating HOME and exposes that code path only to runtime commands (no install).
Short test alias <maker-scratch-alias> points to the maker's synthetic scratch;
all test files remain physically in scratch, outside Git. No test/assertion relaxed.
The intermediate rework2-verified run passed the full suite but native storage
correctly refused symlink ancestors in PTY smoke. The verifier now resolves smoke
roots physically, retaining the short alias ONLY for legacy socket tests. Native
no-follow guards are unchanged; intermediate failed evidence remains preserved.

## Historical v0.1 handoff

Result: passed for the local maker phase; NOT final approval.
Status: modified locally / verified locally. Not committed, not pushed,
not published, not installed in any user profile. Una review requested on the
same task t_3f9983de, followed by the final user gate. Rework R2: second and LAST cycle;
neither previous delivery was approved (residual F1 in the second).

## Changed

Single product: <private-development-checkout>/hermes-handoff
Git base: 0bbf0a2dcdeb16f44463e0f62e8aed4ba2951c63, local upstream
<local-upstream>/session-handoff. The source retains the user's 5 untracked files;
it was not modified. All provenance and the original MIT LICENSE are preserved.
Native product name: Hermes Handoff, slug hermes-handoff, version 0.1.0.
package.json/package-lock and source launchers remain session-handoff0.7.5; they are NOT
part of the native artifact: do not run npm install/setup on the fork.

Existing modified path (only one):
    server/handoff_state.py
    Direct import from the same redaction module rather than through MCP/launcher.

New paths, all explicit:
    __init__.py
    plugin.yaml
    server/hermes_handoff.py
    skills/hermes-handoff/SKILL.md
    tests/test_hermes_handoff.py
    scripts/pack_hermes_handoff.py
    scripts/smoke_hermes_handoff.py
    scripts/test_hermes_regression.py
    HERMES-README.md
    QUALITY-PARITY.md
    HANDOFF.md

No source deletion, commit, tag, push, publish or vault write.
The synthetic .l lab created by the maker is preserved, not deleted, in
<private-review-workspace>/diagnostic-shortnames.
Temporary files, logs, caches, synthetic session DBs and builds are in the dedicated workspace.

## Artifacts/evidence

Workspace: <private-review-workspace>
R2 plugin directory: <workspace>/dist-r2-final/hermes-handoff
R2 local package: <workspace>/dist-r2-final/hermes-handoff-0.1.0.tar.gz
Package and file SHA256 manifest: <workspace>/dist-r2-final/MANIFEST.json
Review/integration overlay: <workspace>/review-r2/overlay.tar.gz
Manifest of ALL tracked files + explicit new files: <workspace>/review-r2/source-manifest.json
Hashes verifiable with sha256sum -c: <workspace>/review-r2/source-files.sha256
Exact tracked diff: <workspace>/review-r2/tracked.patch
The dist-final/review and dist-r1-final/review-r1 deliveries remain intact for comparison.
These paths are produced by the final round; actual exit codes are recorded
in evidence/final-checks-r2.json and in the review lifecycle metadata, not inferred.

Checks already executed:
- RED before the adapter: missing import, native-red.txt exit2.
- Core+native: native2.txt exit0,134passed.
- Standard baseline: baseline-final.txt exit1,1379passed14skip,3AF_UNIX path too long.
- Standard regression: regression-standard.txt exit1,1388passed14skip, same3fail.
- Baseline with short tmp harness: baseline-harness.txt exit0,1382passed14skip.
- Regression with the same harness: regression-harness.txt exit0,1399passed14skip.
- Initial runtime on the package outside the checkout: doctor1/validate1 exit0 and smoke2
  exit0. The strengthened final round repeats on the updated package, reads the ref from another
  synthetic session and saves doctor-final/validate-final/smoke-final.txt.
- The Python linter IS configured: ruff.toml and .github/workflows/ci.yml:67-68.
  The first delivery had two F401 errors (unused imports), observed by Una; the previous
  claim that no linter existed was incorrect. Imports removed, full CI check rerun:
  `python -m ruff check . bin/session-handoff`, ruff-r1.txt exit0, All checks passed.
  No claim of a complete static typecheck.

## Rework R1 — changed / verified / remaining

F1: the Hermes reader decodes nested JSON (including arguments serialized as a
string) BEFORE the shared redactor, which was not modified. This applies to both
tool_calls and structured content. It preserves string/container types and
non-secret data; max 16 levels and 512 nodes per field already limited to 8KiB. Malformed
or over-budget structured data: entire field omitted, structured_field_omitted=true,
truncated=true, no fallback to the original escaped text. JSON-looking prose may
be conservatively omitted: this is a disclosed loss, not a reconstructed fact.

F2: SQL filter (active=1 OR compacted=1) BEFORE ORDER/LIMIT. Undo/edit/regenerate
(active=0,compacted=0) excluded; each message returns active,compacted,lifecycle.
compacted_history is history, not a current requirement or a newly executed test; the skill
was updated to require verification before promoting it. Schema without lifecycle:
fail-closed error, no fallback that includes withdrawn messages.

R1 evidence: evidence/r1-red.txt, nine new regressions failed on the initial code;
smoke-r1-red.txt exit1 on the PREVIOUS PACKAGE with real SessionDB/PluginManager/dispatch:
secret_scrubbed=false, withdrawn_rows_excluded=false and missing lifecycle.
Native tests added in R1:11 cases, plus runtime coverage with real append_message,
archive_and_compact and replace_messages(archive_dropped=True). No user DB.
evidence/regression-r1.txt exit0:1410passed14skipped, same harness as the baseline.
evidence/smoke-r1-check.txt exit0: all R1 checks true; valid/malformed JSON,
depth/node budgets on content and tool_calls, and compaction followed by undo.
The final round on the updated package is in *-r1-final.txt / final-checks-r1.json.
R1 NOT approved: R2 review found the same leak under ordinary text wrappers.

## Rework R2 — changed / verified / remaining

Hermes boundary: left-to-right JSONDecoder.raw_decode scan for JSON values
embedded in stdout/fences/prose and nested strings, without special prefixes.
Recursion and budgets of 16 levels/512 nodes per 8KiB field unchanged; error/ambiguity/budget
omits the entire field and sets structured_field_omitted/truncated. Shared redactor
UNCHANGED. Reassembled scrub also preserves assignments with double-quoted values.
Valid JSON preserves non-sensitive data/external text but normalizes whitespace/escapes.
Known loss: non-JSON braces/brackets/double quotes in prose or code may cause
the entire field to be omitted, even without secrets; the skill now discloses this and requires
uncertainties and current observations, not invented reconstructions.

Evidence: evidence/r2-red.txt9fail1pass before the fix; smoke-r2-red.txt exit1 on the
R1 PACKAGE through the real runtime. Ten new representative cases (5 wrappers,4 errors/
budget/ambiguity,1 nonsecret control). baseline-r2.txt1382pass14skip and regression-r2.txt
1420pass14skip exit0; focused-r2.txt163pass exit0; ruff-r2.txt exit0.
smoke-r2-check.txt and una-probe-r2-check.txt exit0 on the new package: Una R2 probe
with the same fixtures/assertions, only paths/CLI adapted in the workspace. Synthetic DB bytes
unchanged. NOT an independent review. Final doctor/validate/smoke/probe and manifest
verification are in *-r2-final.txt and final-checks-r2.json. No user DB or inference.
Independent Una review3 and the final user gate remain. Any residual issue => escalation,
not a third autonomous rework. No installation.

The limited meaning of parity, path:line matrix, losses, classification of
each invalid cohort and runtime limitations are in QUALITY-PARITY.md. The same renderer,
redaction and validation on equivalent state do NOT mean absolute semantic quality
or compared live LLM generations. The model remains responsible for synthesis.

Hermes runtime read/exercised: <installed-hermes-source>,
0.22.2, d923a5eb487a17c0a68801bba9ef0f56c81040a8, preexisting dirty=True.
Not modified by the product. No inference/spending/real credentials/transcripts.
The first smoke triggered dependency bootstrap only in the workspace's synthetic home:
documented failure, not success; the HERMES_DISABLE_LAZY_INSTALLS=1 flag now prevents
that bootstrap and is also set in the smoke script before Hermes imports.

## Repeatable maker commands

From the fork directory; choose NEW temp/build/smoke directories to avoid deleting
existing ones. Set W to a NEW absolute synthetic scratch directory. These historical
commands require the private development checkout and are not runnable from this
native repository; replace <installed-hermes-source> with the tested runtime path.

    HOME="$W" TMPDIR="$W" XDG_DATA_HOME="$W/home/data" XDG_STATE_HOME="$W/home/state" UV_CACHE_DIR="$W/cache" uv run --no-project --with pytest python scripts/test_hermes_regression.py --baseline --basetemp="$W/a"
    HOME="$W" TMPDIR="$W" XDG_DATA_HOME="$W/home/data" XDG_STATE_HOME="$W/home/state" UV_CACHE_DIR="$W/cache" uv run --no-project --with pytest python scripts/test_hermes_regression.py --basetemp="$W/c"
    HOME="$W" UV_CACHE_DIR="$W/cache" uv run --no-project --with ruff python -m ruff check . bin/session-handoff
    python3 scripts/pack_hermes_handoff.py "$W/dist-r2-final"
    HERMES_DISABLE_LAZY_INSTALLS=1 HERMES_HOME="$W/runtime-home" HERMES_BUNDLED_PLUGINS="$W/empty" HERMES_ENABLE_PROJECT_PLUGINS=0 TMPDIR="$W/tmp" <installed-hermes-source>/.venv/bin/python -m hermes_cli.main plugins doctor --ci "$W/dist-r2-final/hermes-handoff"
    HERMES_DISABLE_LAZY_INSTALLS=1 HERMES_HOME="$W/runtime-home" HERMES_BUNDLED_PLUGINS="$W/empty" HERMES_ENABLE_PROJECT_PLUGINS=0 TMPDIR="$W/tmp" <installed-hermes-source>/.venv/bin/python -m hermes_cli.main plugins validate "$W/dist-r2-final/hermes-handoff"
    HERMES_DISABLE_LAZY_INSTALLS=1 PYTHONPATH=<installed-hermes-source> TMPDIR="$W/tmp" <installed-hermes-source>/.venv/bin/python scripts/smoke_hermes_handoff.py "$W/dist-r2-final/hermes-handoff" "$W/smoke-r2-final"

Do not reuse existing --basetemp directories: pytest may clean them automatically; use a
new suffix. The runner only shortens temp names/prefixes for the AF_UNIX limit;
it does not change tests or assertions. Keep temporary files OUTSIDE any Git repo: otherwise
different fixture projects share git-common-dir and invalidate the store tests.

## Handoff to Una — separate write-set required

Una's policy verified by the operator: she may write ONLY under
her reviewer-owned workspace. The maker does NOT modify her policy or write there.
Una reads the fork, original artifacts and logs, but does NOT run tests that write to them.

Una creates a local copy under
<reviewer-workspace>/hermes-handoff-review-r2/source:
local clone of the fork (no network, no commit), verifies exact HEAD, then
applies the overlay with safe relative paths only and checks source-files.sha256 from
the copy's root. The manifest includes all tracked files to demonstrate equivalence,
not just new files. Do not copy runtime, .l, .git, caches or real transcripts.
If a target already exists with data, do not overwrite it: choose a new suffix.

To repeat tests, use HOME/TMPDIR/UV_CACHE_DIR and basetemp under a separate lab
in HER write-set, but outside the Git clone. That pathname is long: the UNIX limit
remains in default-socket tests (even with a short prefix). In that case classify the
pathnames and run the 3 tests in a shorter directory ONLY if already authorized by her
profile, for example <reviewer-scratch>/t; do NOT change the allowlist and
do not use Miku's workspace. Use the same short lab for baseline/regression.

Una repeats the build in a new directory of her own, doctor --ci, validate and smoke on the
packaged plugin, not just FakeContext or a summary. Save findings/evidence in her own
workspace. Also verify tar allowlist/hashes, absence of npm lifecycle and intact gates.
The test commands can be reused by replacing W with Una's lab and cwd with
the verified copy. Review is a new independent cycle; not claimed as executed.

## Resume/installation

Installation in the real runtime NOT authorized/executed. HERMES-README.md contains
instructions to copy ONLY the native directory, enable hermes-handoff in the
selected profile and start a new session AFTER specific user consent.
Supported invocation: skill_view(name="hermes-handoff:handoff"), then the
hermes_handoff tool with action evidence/create/read/validate, absolute workspace and exact
ref for reading. session_id comes only from the host. No auto_switch, launcher,
legacy path, migration or session control. Read does not equal successful resume.

Next step: Una checks the artifact and repeats tests on the hash-verified copy;
if a concrete finding remains, escalate (2 reworks exhausted). Otherwise,
approved review and user gate for any future installation/publication.

## For Luka:

Proposed note: wiki/projects/hermes-handoff (or a section linked to session-handoff).
User decision: local Hermes Handoff fork, native port scope A, not session migration
or Desktop. Source: task t_3f9983de and user/operator confirmation thread.
Canonical product: <private-development-checkout>/hermes-handoff; read-only local
upstream <local-upstream>/session-handoff, base0bbf0a2. Maker Miku, checker Una, final user
gate. Native adapter reuses core, requires host session binding, per-home storage and
manual resume. Parity limited to contract/renderer/redaction/validation for equivalent
state, not absolute LLM quality. Una blocked the first delivery for nested JSON
leaks and included withdrawn messages; R1 fixes lifecycle but R2 review finds residual F1
in ordinary stdout/fence/output wrappers. R2 also decodes embedded JSON
at all levels, with conservative omission on ambiguity and explicit loss;
shared redactor unchanged. Evidence: QUALITY-PARITY.md, R2 manifest and logs attached
to the task. High confidence in executed local checks; review, real installation, live
LLM quality and resumed-task success NOT verified. Contradictions: package.json in the
fork remains session-handoff0.7.5 for regression; the installable product is exclusively
the native hermes-handoff0.1.0 artifact, never npm install of the fork. No vault write.

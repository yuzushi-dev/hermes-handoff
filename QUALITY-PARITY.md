# QUALITY-PARITY — Hermes Handoff

Distribution context: v0.3.0 is distributed through GitHub Releases;
catalog listing remains pending. Native-candidate local review passed. The engineering
results below are retained history, not new certification or current approval.
All artifact/workspace/script/test references describe the separate private
development checkout and retained evidence, not files available in this repository.

Current v0.3 scope and evidence: DESKTOP-CONTRACT.md,
docs/CANDIDATE-0.3.0.md and artifacts/v0.3.0-ready-fixes. The v0.2/v0.1 reports
below are historical, including their former Desktop non-support and pending
review statements. Historical references to "public" policy resolvers are not a
current API guarantee: the four internal imports are disclosed in the candidate
document and README. Compatibility remains limited to the tested Linux runtime;
local checks do not approve publication or catalog admission.

## v0.2 scope and evidence boundary

Rework2 policy regression: --toolsets in the previous candidate replaced both
platform_toolsets.cli and the MCP spawn filter. A launcher assertion and real PTY
comparison to normal chat reproduced it RED. The launcher now passes no toolset
override and adds no tools. Public coding_selection/load_config/resolve_toolset
reject focus posture without handoff before claim/spawn. Profile selection and
configured MCP startup remain the normal host behavior, not a plugin reimplementation.
The strengthened --restricted-policy smoke uses actual platform_toolsets.cli:
file, hermes_handoff, kanban and a synthetic stdio MCP server. It compares real
schema sets to normal chat, asserts kanban remains and terminal/execute_code/browser/
delegate are absent, invokes the MCP canary through the real client and checks
focus refusal, source invariance and confirmation waiting. Test fixture MCP is a
tiny offline stdlib JSON-RPC server, not a mock of the Hermes MCP client. An earlier
SDK fixture failed with missing mcp; no core dependency was installed to hide it.
Final execution results and hashes: artifacts/v0.2.0-rework2-release and task transition.
The earlier rework2-final directory records two environment failures, not success:
AF_UNIX pathname length and missing optional MCP in the bootstrap .venv under an
isolated HOME. The verifier now reads the already-installed PM dependency generation
before isolation (no provisioning), and uses a short alias into profile scratch.
Native smoke roots are physically resolved: the intermediate rework2-verified
run passed the full suite but correctly rejected the alias as a store ancestor.
The no-follow store checks are unchanged; the alias is only for legacy socket tests.
These probes do not certify arbitrary model obedience or reproduce ad-hoc toolset
overrides from the source session. hermes_handoff must be enabled in the profile.

The following historical0.1 report is preserved, not current release approval.
v0.2 keeps its canonical validator/renderer/redactor/store unchanged and adds a
host-bound origin sidecar, route-only observer, opening journal/CLI and independent
writer through public ctx.llm.complete. See OPENING-CONTRACT.md and HERMES-README.md.
No new dependency or core patch; upstream session-handoff remains untouched.

New contract tests: tests/test_handoff_open.py. Initial RED: module missing (exit2).
Two additional hardening regressions were reproduced RED before the fix: a different
source session could prepare another origin's ref; a relative workspace was accepted.
Both now enforce host-created immutable origin/workspace binding. Existing read and
validate behavior is retained; old0.1 refs without origin metadata are manual-only.

Actual runtime probes use installed0.22.2 d923a5eb (already dirty, not changed here):
- scripts/smoke_hermes_handoff.py: real SessionDB/PluginManager/registry; retains
  the full0.1 secret/lifecycle checks and no session DB mutation.
- scripts/smoke_handoff_open.py: real foreground CLI on synthetic PTY, loopback
  scripted provider, native tool_describe/tool_call, read/validate and project-file
  reads, actual waiting without another model request, unchanged source rows,
  destination-only /exit. This is not a fake CLI or a semantic LLM judge.
- scripts/smoke_handoff_writer.py: actual registry -> plugin -> ctx.llm.complete ->
  loopback HTTP, default B makes zero calls and explicit B uses redacted bounded input.
  Non-loopback Python sockets are denied by a test-only guard; no real credentials.

The first PTY probes correctly failed: direct calls to deferred tools were not
available. The harness now uses the runtime's real public deferred bridge; the
profile must already enable its toolset. Another harness failure was a batched PTY
/exit arriving before submission was ready; typing/submitting separately exercises
normal shutdown. No failed probe is counted as a passed check.

B risk: an external writer sees ONLY bounded, already-redacted persisted evidence,
not the full live context. Missing or conservatively omitted JSON/prose can lose
critical goals/decisions. No invented repair of gaps. Model output is validated and
redacted again, returned for inspection, not automatically published. This warning
is in tool output and skill. Host override consent is required; provider/model API:
hermes_cli/plugins.py:377-384; agent/plugin_llm.py:446-458,498-572. No requested
profile/auth/task override; no paid live calls. The host may retry/fallback and model
aliases may differ: reported route mismatch is conservatively rejected, but attribution
is not independent proof of a remote provider's actual model or complete routing.

Limits: bootstrap confirmation is an instruction, not a sandbox against a disobedient
model. PTY scripted results prove integration/observed waiting, not live model quality.
Temporary custom endpoint/auth overrides are not copied; named profile providers
are needed. Durable uncertain launch reservations never auto-retry; inspect the
identified session or manually read the ref. Duplicate summarize may incur another
call; no exactly-once inference claim. Desktop is unimplemented in0.2. No real-profile
installation, paid provider call, commit, push or publication was performed.

Additional review before delivery found Hermes main.py:603-628 can override a
default/custom HERMES_HOME using sticky active_profile. The new regression failed
before adding an explicit --profile selector; the final PTY fixture deliberately
sets an invalid sticky profile to prove it cannot hijack the child launch.
That stronger smoke also exposed a double import when running python -m
hermes_cli.main: profile flags had already been consumed when the canonical module
was imported again. The product and PTY now use the installed public Hermes console
entry point (resolved on PATH), plus explicit profile; no core change or monkey patch.

Verification2 was fully green:1432passed14skipped, focused50passed, ruff,
doctor--ci, validate and all three real-runtime smokes exit0. The initial full
suite run had6environment failures: overly long AF_UNIX paths and temporary files
outside the sandbox's synthetic HOME. Only the harness layout changed: HOME is
the scratch root, TMPDIR is directly there, pytest --basetemp is a short child;
no assertions or code paths skipped/changed. Failed logs remain preserved.

The first v0.2 delivery was NOT approved: CLI override reused the prepared ID and
conflicted; duplicate launch returned0; writer trust errors were masked; external
writer provenance was incorrectly attributed to the current conversation.
Rework tests reproduced8fail/15pass before fixes (including the strengthened
duplicate assertion). Now a testable open_from_cli derives a deterministic attempt,
launch injects tty/runner and rejects duplicates with3, safe trust hints survive the
tool boundary, and a session/state digest supplies bounded-writer provenance.
The no-writer provenance text and all0.1 tests remain unchanged. Exclusive destination
binding is also regression-tested. External writer still sees bounded/redacted
evidence ONLY; no claim of full context or independently verified facts.

Current commands/results and artifact manifest are in task t_1d73b6f6's rework maker
handoff and artifacts/v0.2.0-rework1-final. Earlier release-check evidence remains
preserved, not current approval. Independent review Una is still required.
The first rework verification (rework1-check) passed focused/ruff/doctor/validate
and all real-runtime probes, but its full suite hit one AF_UNIX path-too-long
fixture failure (1442passed14skipped1failed). The final run uses a one-character
scratch leaf, as the previous successful release check did; no assertion is waived.
The strengthened PTY checks explicitly assert qualified skill preload, only read-only
tool calls, persisted destination != source, no hook payload, source rows unchanged
and waiting. A second PTY probe exercises the actual CLI A override; a separate
registry probe verifies actual PluginLlmTrustError hints with zero HTTP calls.

## Historical v0.1 report (superseded only by the v0.2 scope above)

Maker result: verified locally; Una review and user gate still required.

## Precise meaning of parity

The actual session-handoff pipeline does not certify truth or semantic completeness
with an automatic judge. The model follows a skill and produces canonical text or
v1 state; the server validates structure/limits, redacts common credentials and persists a
record. In this milestone parity means: the same applicable semantic instructions,
the same equivalent state, shared renderer and redaction, shared structural checks and
secure store. Tests actually compare outputs, not just headings.
It does NOT mean absolute model quality, equivalence of two stochastic generations,
factual truth or evaluation of live Claude/Codex/Hermes inference: no model
call was made. No transcripts or sessions were migrated.

Source provenance: session-handoff upstream, HEAD
0bbf0a2dcdeb16f44463e0f62e8aed4ba2951c63, package.json:2-4 = session-handoff0.7.5.
Integrated local fork: private Hermes Handoff development checkout. No new commit at that historical stage.
Native artifact: hermes-handoff0.1.0. Original MIT/LICENSE preserved.

## Contract matrix with path:line evidence

The following source paths are relative to the fork and identical to the source, except
for the two redaction import lines in server/handoff_state.py.

| Property | Actual Claude/Codex guarantee | Hermes | Evidence |
|---|---|---|---|
| Goal, constraints, Done/In Progress/Pending status | skills/session-handoff/SKILL.md:60-106; state v1 server/handoff_state.py:12-33,79-119 | Native skill requires the same concrete facts and distinguishes sources | skills/hermes-handoff/SKILL.md; equivalent test fixture and real smoke |
| Decisions with rationale/alternatives | source skill:92-106, no semantic enforcement | same skill obligation; smoke fixture preserves "because API contract" | scripts/smoke_hermes_handoff.py:smoke, state/created/read |
| Relevant failed attempts and problems | source skill:61,106; rejected_attempts in renderer:167-171 | unchanged array, same renderer; comparison test contains failed regex-only attempt | tests/test_hermes_handoff.py:113-139 |
| Exact file/symbol references | source skill:60-62,98; free text not judged | same obligation, src/example.py::apply_value fixture preserved | differential test and smoke |
| Executed vs unexecuted checks | verification v1; skill:61,98 | explicit instruction and fixture with exit1 + Full regression not executed | state renderer:170; smoke fixture |
| Blockers, assumptions, missing data | uncertainties v1; free-form state | sources/user/assumptions separated by instruction; unknown not converted to success | native skill; adapter _session/handle, provenance and completeness |
| Next step/resume | source skill:100-114; manual read != resume at 52-54 | exact ref, live verification before mutation; resume_verified=false | native adapter handle; smoke reads the ref from synthetic-beta |
| Structural validation | handoff_mcp.py:141-142,378-443 and handoff_state.py:79-119 | same validate_state/render_state; same canonical sections; no semantic judge | positive/negative differential test |
| Secret scrub | redaction.py:113-178; state:122-146; store:243-257 | same functions without a divergent copy; Hermes decodes JSON/arguments before scrub; whole-field omission on error/budget | tests/test_hermes_handoff.py; R1 runtime smoke with real SessionDB serialization |
| Secure persistence | handoff_store.py:54-66,261-409,640-724 | same store in private instance, profile roots; immutable records, hash, no-follow, atomic no-replace | symlink tests, concurrency 8 retry, ID conflict, profiles |
| Session binding | Claude/Codex client context; exact ID, no global mtime (skill:120-126) | host-only session_id, absent from schema; missing/forged rejected | installed model_tools.py:827-839; native adapter _session/handle; registry smoke |
| Compaction/incompleteness | checkpoint != semantic handoff (skill:24-37) | no hook; parent not read, completeness=not_guaranteed; undo excluded before limit, compacted history labelled | lifecycle/limit/schema tests; smoke with real archive_and_compact + replace_messages |

## Reuse and intentional differences

server/handoff_state.py now imports directly from server/redaction.py, the same
function that handoff_mcp.py:137-138 already re-exports. The change avoids importing
launcher/onboarding/telemetry into the native plugin; it does not change the algorithm. The rest of
handoff_state, redaction and handoff_store is shared directly, not reimplemented.
Each adapter has a private instance of the store module with roots under get_hermes_home:
no changes to global Claude/Codex roots and no mutation of os.environ
in product code. Only the smoke harness sets its own synthetic environment.

Hermes exposes a native tool with four actions (evidence/create/read/validate), not
the entire MCP, setup, launcher, import/export or migration. Create accepts only v1 state,
not free-form Markdown/legacy paths. Its structure is therefore more restrictive than the
source Markdown alternative. The document retains equivalent rendering plus a single
host-authored provenance line. The test explicitly excludes it from the byte-exact comparison.
The manifest's origin field retains the original schema: session provenance
is in the document protected by the same hash. Model-authored state != certified fact.

Session evidence: SQLite mode=ro, query_only, read snapshot, budget of 2s,
256 messages plus sentinel, maximum 8KiB per field,96KiB of serialized evidence.
Reads only the current host session, not parents, reasoning/attachments/external DBs.
Over-limit fields are omitted whole (not truncated through a private key).
R1: the (active=1 OR compacted=1) filter precedes ORDER/LIMIT; rows withdrawn by
undo/edit/regenerate are not current evidence. active/compacted/lifecycle distinguish
active conversation from compacted_history, which does not prove current requirements/tests.
Incompatible schema: fail-closed, no indiscriminate reading of all rows.
For content and tool_calls, recursive decoding includes string arguments and JSON
embedded in stdout/fences/prose at any level before the shared redactor.
Left-to-right scan with JSONDecoder.raw_decode: complete values consumed
without splitting internal quotes/braces; no prefix allowlist or regex for JSON.
Per-field budget:16 levels/512 nodes, in addition to the SQL 8KiB limit.
JSON error or exhausted budget omits the ENTIRE field, without escaped fallback;
structured_field_omitted and truncated signal the loss. Prose/code with ambiguous/non-JSON
braces, brackets or double quotes may be omitted ENTIRELY even without
secrets: disclosed conservative loss, potentially including useful checks/paths.
The skill requires recording the gap, not promoting absence to success, and supplementing
only with available current observations. Valid JSON preserves non-sensitive data and
external text, but normalizes JSON whitespace/escapes; no byte-exact transcript promise.
This is not a new general secret detector:
the shared redactor remains unchanged and does not recognize every possible secret in prose.
The tail may lose early goals or decisions; even an untruncated tail may
exclude in-flight turns or compressed history. These losses are explicit, not
filled with invented information. The model must use current conversation/repo
with source labels and state unknown where data is unavailable.

Request_id is required and stable for retries: deterministic UUID per project,
session and request; different content/name is a conflict, no overwrite.
Cross-project refs and different profiles are not read implicitly. A new session
may read the exact ref in the same project/profile without being the origin session.

## Verified runtime/API

Official docs read: https://hermes-agent.nousresearch.com/docs/llms.txt and
https://hermes-agent.nousresearch.com/docs/developer-guide/plugins . The web extractor
returned partial content; signatures were confirmed in the installed code:
hermes_cli/plugins.py:456-502 (register_tool),
hermes_cli/plugins_content.py:23-52 (register_skill), model_tools.py:827-839 (session_id),
tools/registry.py:909-934 (dispatch), hermes_state_sessions.py:459-467 and
hermes_state_messages.py:389+ (synthetic SessionDB).

Verified runtime: Hermes0.22.2, commit d923a5eb487a17c0a68801bba9ef0f56c81040a8.
VersionInfo reports dirty=True: installed Hermes checkout already modified; it was not
changed by this product. The evidence concerns that local runtime, not a
pristine upstream release or other operating systems.

Real smoke: PluginManager discovery/import/register + real SessionDB + registry.dispatch,
with two synthetic sessions, compressed continuation, create/read/validate, retry and
manual read from the second session. No FakeContext and no model inference.
Network sockets disabled in the smoke. Row snapshots and synthetic DB SHA256
identical before/after the tool. No user transcripts or credentials were read.

## Repeatable results and failure classification

Canonical logs retained privately in the historical review workspace's evidence/:

- native-red.txt: exit2, server.hermes_handoff import missing before implementation.
- baseline-final.txt: exit1,1379passed14skipped3failed, original suite with correct cwd.
- regression-standard.txt: exit1,1388passed14skipped, same three failures, first9 native cases.
- native2.txt: exit0,134passed, core/redaction/store+first9 native cases.
- baseline-harness.txt: exit0,1382passed14skipped, same core HEAD code loaded from local Git.
- regression-harness.txt: exit0,1399passed14skipped, including17 new native cases.
- doctor-final.txt, validate-final.txt and smoke-final.txt: checks on the final package,
  to be read with dist-final's MANIFEST.json (final handoff records exit codes).

Three standard environment failures, identical before/after (no regression):
1. test_codex_app_server.py:143: <workspace>/t/test_default_socket_uses_codex0/app-server-control/app-server-control.sock
   (regression uses /u/ instead of /t/, same length).
2. test_codex_app_server.py:164: <workspace>/tmp/codex-home-<random8>/.codex/app-server-control/app-server-control.sock.
3. test_telemetry_cli.py:1213: <workspace>/t/test_nonregular_config_is_reje1/.config/session-handoff/telemetry.json
   (regression /u/). OSError AF_UNIX path too long occurs at fixture bind, before the adapter.

The scripts/test_hermes_regression.py runner uses HOME/TMPDIR in the workspace OUTSIDE Git,
leaf tmp_path='t' and a short temporary prefix, keeping tests/assertions/call paths unchanged.
Final baseline and regression share the same environment/harness. In --baseline mode
it loads only the changed shared module (handoff_state) from HEAD, excluding the native file;
all other upstream files are unchanged. No test was fixed just to make it pass.
The 14 skips remain skips: they are not live certifications of optional clients/benchmarks.

Invalid intermediate attempts preserved, not used for comparison:
- baseline-pytest.txt from an archive copy without Git and with long tmp:32fail31error; no patch then.
- baseline-short.txt: wrong cwd/insufficient HOME isolation and 3 long sockets.
- native1.txt:45pass2fail, differential test assertion error that did not remove
  the provenance line; corrected full-content comparison without that line.
- baseline-shortnames.txt: tmp under the Git fork grouped different projects under the same
  anchor; not a valid regression. Entire .l lab moved to workspace/diagnostic-shortnames.
- smoke1.txt: automatic runtime bootstrap under a new synthetic home installed
  dependencies only in that workspace and reran the script, refused because the directory
  already existed. Not used as success. HERMES_DISABLE_LAZY_INSTALLS=1 now prevents
  bootstrap; smoke2 passed before the final strengthening of reads from a new session.

## Rework R1 and cross-checks

The first delivery did NOT pass review: Una observed a synthetic API_TOKEN leak
inside escaped function.arguments and returned withdrawn instructions/tests;
the ruff CI check also failed with two F401 errors. The previous HANDOFF.md claim of
no linter was false: ruff.toml and .github/workflows/ci.yml:67-68 configure it.
Correction limited to the Hermes boundary, no shared-redactor refactor.

Evidence in workspace/evidence: r1-red.txt (9fail on previous code), smoke-r1-red.txt
(exit1 on frozen package, both flaws confirmed through real runtime),
regression-r1.txt (exit0,1410pass14skip:28 new cases versus the original baseline,
including 11 in R1), ruff-r1.txt (exit0). smoke-r1-check.txt exit0 checks JSON/arguments,
malformed data, depth/node limits on content/tool_calls, compaction+undo,
no row or DB byte mutation; fixture generation through real SessionDB APIs.
Final doctor/validate/smoke round: *-r1-final.txt with exit codes in final-checks-r1.json.
R1 package in dist-r1-final, complete manifest/overlay in review-r1. Previous dist-final and
review preserved for comparison. The new Una review remains independent.

## Rework R2 — last authorized cycle

R2 review reproduced residual F1: the same escaped JSON leaked the marker
under stdout/fences and inside a JSON output field. R1 was therefore insufficient;
this was not a problem with the shared redactor, which remains UNCHANGED. F2 lifecycle and
ruff, by contrast, were independently verified correct by Una.

R2 changes only the Hermes boundary and related tests/instructions/reports. It detects
JSON values embedded in strings at every level, not just at the beginning, retaining
the same budgets and fail-closed omission (including ambiguity/malformed data). Scrub of
the complete reassembled text also preserves the API_TOKEN="valore" check in prose.

Actual evidence in workspace/evidence:
- r2-red.txt:9failed1passed on R1 code, before the fix (10 new cases).
- smoke-r2-red.txt:exit1 on R1 package with real SessionDB+PluginManager+dispatch;
  stdout/fence/nested_output/multiple/layers leaks reproduced, omissions absent.
- baseline-r2.txt:exit0,1382passed14skipped; regression-r2.txt:exit0,1420passed14skipped,
  identical harness/environment. Focus focused-r2.txt:exit0,163passed; ruff-r2.txt:exit0.
- smoke-r2-check.txt:exit0 on the new package outside checkout, fixture through real
  SessionDB APIs:3 bypasses, levels/multiples, quoted assignment, nonsecret unchanged,
  malformed/nodes/depth omitted and flagged, F2 and DB bytes/rows unchanged.
- una-probe-r2-check.json/txt:exit0, Una R2 cross-check repeated without weakening
  fixtures/assertions; only paths and CLI parameterization changed in workspace runner
  repeat_una_probe_r2.py. NOT equivalent to a new independent Una review.

Final round on the updated documented package: *-r2-final.txt and
final-checks-r2.json. Dist/manifest:dist-r2-final; complete overlay/hashes:review-r2.
Previous dist-final/review and dist-r1-final/review-r1 deliveries are preserved.
This is the second and LAST authorized rework: residual issues in review3 require
escalation, not a third autonomous cycle.

## Still unverified / gates (unchanged)

Live LLM generation quality, success of a real task after resume, user data,
Desktop integration, migration, macOS and all Hermes versions other than the stated
runtime are neither verified nor promised. No real installation, commit, push,
publish or deploy. Independent Una review and the final user gate remain required.

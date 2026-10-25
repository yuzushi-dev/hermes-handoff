# Hermes Handoff 0.3.0 — candidate readiness

Status: source repository available for review and development; plugin release and catalog listing pending. The native candidate passed independent local review; that is not plugin release, installation or catalog approval. Command outputs, archive/member hashes and delivery reports are separately retained private evidence, not files or accessible evidence links in this source repository. All `artifacts/` references and execution results below describe that private development history; they are not instructions to find those files here. Earlier candidate2 results remain explicitly historical.

## Scope and distribution

- Native Hermes CLI, tool/hook/skill, Desktop SDK route/sidebar and dashboard plugin API.
- Explicit regular-file packaging allowlist. README and its final media/rights/text alternative travel together.
- No source npm package installation, upstream postinstall/telemetry/setup, self-updater, core patch or credential store is included.
- Original session-handoff MIT license and copyright are retained. The archived upstream README describes the original product only; its historical relative links refer to that upstream checkout.
- Original cover/poster/video use the same engraved technical design. Editable brag/Hyperframes sources, font/GSAP licenses and QC are retained in the media deliverable, outside this source repository. The owner explicitly authorized MIT for the project's original images and video and approved the graphics and video. See [media credits](../assets/media-credits.md); original software copyright/license and third-party licenses/attributions are unchanged. Source publication does not authorize a plugin release or catalog submission.

## Approval boundary and runtime coupling

The CLI child strips inherited `HERMES_YOLO_MODE`, `HERMES_NONINTERACTIVE`, `HERMES_TUI_TOOLSETS`, source-session and kanban context; it explicitly selects the bound profile and retains normal profile policy. No broader toolsets or approval flags are passed. Profile configuration and the parent process environment are not modified.

Preflight still imports `agent.coding_context.coding_selection`, `toolsets.resolve_toolset`, `hermes_cli.tools_config._get_platform_tools` and `agent.skill_utils.parse_config_string_list`. The tested runtime's normal CLI/Desktop policy uses these resolvers. Public `ctx.register_*`, `ctx.llm`, dashboard and Desktop SDK surfaces provide extension/dispatch but no equivalent complete effective-tool-policy query was found. Replacing that policy with a homemade tool list would weaken fail-closed behavior; the four imports therefore remain disclosed, not suppressed. Seek a supported host policy-inspection API or an explicit maintainer ruling before catalog admission.

Test target: installed Linux Hermes 0.22.2, source `d923a5eb48`. Other runtimes/platforms and real cross-profile/bot workflows are not certified. The manifest intentionally makes no unverified `requires_hermes` floor claim; the installed schema supports that field, but a tested version is not proof of the earliest compatible release.

## Required local checks

1. RED→GREEN approval-environment tests for both inherited flags, default/explicit-A CLI paths, preserved profile config and normal policy.
2. Focused contracts, compatible upstream regression, Desktop SDK UI contracts, lint and diff checks.
3. Fresh bundle/member/hash audit, README parity, relative audience-link/media audit, no forbidden files or secret-shaped credential literals.
4. Hermes doctor and standard validator against a synthetic home and built bundle. Read warnings as well as check results.
5. Catalog gate `hermes plugins validate PLUGIN --install-deps`. Read stderr and JSON: an exit-zero standard validation after `dependency preparation failed` is NOT a passed dependency gate. Do not repair or mutate the installed Hermes PM environment to force a green result.
6. CLI/writer loopback scripted-provider smokes. Real Desktop only through the approved user+PID namespace/private `/proc` driver; STOP if isolation fails. Synthetic fixtures do not certify arbitrary model quality/obedience.
7. Actual media cover/contact-frame inspection, ffprobe and full decode; no claim of human real-time viewing of all frames.

## Catalog preparation, not submission

Historical candidate2 checks: 209 focused contracts, 1466 regression tests
(14 skipped), seven SDK UI contracts, lint/diff, native/writer/consent-denied and
CLI default/explicit-A/restricted-policy smokes passed. Five real Desktop scenarios
passed in the approved user/PID namespace with private `/proc` and loopback fixtures.
The first attempt used an old developer `.venv` lacking MCP and failed policy
smokes; rerunning with the already-installed managed Hermes dependency interpreter
passed without changing core, test assertions or the real installation.

Historical candidate2 doctor and standard validation passed; the private-import warning remains.
That candidate's separate `--install-deps` attempt in an OS read-only host sandbox returned
exit zero and JSON `ok: true`, but stderr reported `dependency preparation failed:
pm-runtime: not installed or outdated and lazy installs are disabled`.
That historical attempt did NOT pass the dependency gate. No host PM repair was attempted.
Current isolated preparation evidence and its exact bundle identity are recorded in
`artifacts/v0.3.0-ready-fixes/`; do not infer its result from the historical exit code.
Local candidate verification is not publication/catalog approval.

Current local fixes: the Desktop parent/workspace negatives were reproduced RED
before the fix, then 215 focused contracts, 1472 regression tests (14 skipped),
seven SDK contracts and all five isolated real Desktop scenarios passed. Genuine
PM preparation succeeded in a read-only-host/scratch-writable user/PID namespace
with private `/proc`. Warm `validate --install-deps` returned `ok: true` with no
preparation-failed diagnostic and empty stderr, even with lazy installs disabled.
The exact final bundle is rechecked separately; see the ready-fixes report for
argv, interpreter, isolation, stdout/stderr, hashes and earlier failed attempts.

Sources consulted:
- https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission
- https://raw.githubusercontent.com/NousResearch/hermes-agent/main/plugin-catalog/README.md

Policy basis: NousResearch/hermes-agent revision `571a5911ae6aaa05ef3df53bf0f6720c4556c24a`. Its catalog README and submission guide agree on 17 admission rules; the deployed guide is concordant. The earlier fifteen-versus-six-rule disagreement is historical, not a current release gate. Rule 10 concerns dependency-release quarantine, NOT the age of the plugin release commit; there is no two-week plugin pin-maturity requirement. Rule 9 treats undocumented internal imports as warnings, not automatic rejection. Keep all four imports disclosed and compatibility restricted; any maintainer ruling occurs during authorized catalog review, not local validation.

A historical non-submittable catalog template is retained only with the private candidate evidence, not here. This dedicated repository contains the native source tree, not the legacy session-handoff checkout or its private history. A future catalog submission must pin the final reviewed public commit and disclose the compatibility warnings; source availability is not submission or maintainer acceptance.

## Remaining owner / maintainer gates

- Independent local review of the native candidate passed; public-source preparation is checked separately. No additional runtime/media certification is implied.
- Only source repository publication is in scope. Plugin release, release assets, tags, catalog submission and real-profile installation remain pending. MIT for original images/video and aesthetic acceptance were approved; third-party licenses/attributions remain unchanged.
- Validate the exact public source revision before relying on it; future catalog pins and any plugin release require their own approval.
- Runtime private-import disclosure/API seam and successful dependency preparation against the final immutable target; warnings are not approval and do not replace the dependency gate.
- Apply the pinned concordant admission policy; screenshots and all risk disclosures in a separately authorized catalog PR, followed by maintainer review.
- Source availability does not imply a real-profile installation, live/paid inference, plugin release, release asset upload, tag, catalog submission or deployment.

# Substantive Work Protocol

This is the canonical planning and execution workflow for substantive work in a
repo that vendors `agent-protocols/`.

Use it for any non-trivial feature, fix, refactor, migration, or cross-repo
change.

If the workstream is intentionally proposal-only and stops before
implementation, use the [Proposal protocol](proposal-protocol.md). Proposal
capture does not automatically require the full substantive artifact set.

## When To Use This

This protocol is the default when any of these are true:

- the change has non-local effects across modules (file count alone is not a trigger)
- the work has meaningful product, runtime, or security risk
- the work needs more than one reviewable implementation slice
- the work crosses repos or ownership boundaries
- the user asked for an epic, rollout, or non-trivial implementation plan

For tiny, single-slice changes that do not meet the bar above, use the
[Minor work protocol](minor-work-protocol.md) instead. For substantive work,
use this protocol unless there is a very good reason not to.

## Core Rules

1. Every new feature, functionality change, or fix starts on its own branch.
2. Keep the integration branch worktree clean and up to date with origin before
   creating the branch. The examples in this package assume `main`; if the repo
   uses another trunk branch, record that explicitly in the plan and the
   checks.
3. Every substantive branch should have its own dedicated worktree. Do not
   implement multiple active substantive streams in the same checkout. Record
   the branch/worktree binding in the plan manifest and prove it with
   `git_branch_worktree` before treating the branch as runnable or ready. Set
   `current = true` when the gate is supposed to validate the checkout from
   which the phase checker is running; registration of the right branch in a
   different worktree is inventory evidence, not proof that the current source
   is the reviewed source.
4. If the work spans repos, create a matching branch pair and keep each repo in
   its own worktree.
5. Use gated phases at real dependency, review, or acceptance boundaries. A
   single implementation slice can use one execution phase; do not invent phases
   solely for planning, documentation updates, or status reporting.
6. Only one phase may be actively implemented at a time.
7. Do not advance until the current phase exit gate passes.
8. Do not call work complete from narrative judgement alone. Completion must be
   backed by the phase checker and the documented gate.
9. Merge to the repo’s primary integration branch only after acceptance and
   final-green closure unless the documented deployment topology can create the
   acceptance artifact only from that integration branch. In that case, follow
   the controlled integration rollout below and keep the result unaccepted
   until the post-merge gates pass.
10. Treat live git and worktree state as authoritative. Durable docs should
   mirror that state, not override it.
11. Proposal-only slices need only the durable artifacts that will still be
    useful after review. Use the proposal protocol to decide what survives,
    and keep temporary ledgers or inventories disposable by default.
12. Before changing an existing code surface, add or identify meaningful
    passing behavioral tests for that surface and run them before the edit.
    Re-run those tests after the edit and at the relevant phase gate before
    proceeding.
13. For greenfield code, use test-driven development: write a meaningful test
    that fails for the missing behavior, add the implementation, then prove
    the same test passes. Do not weaken the test to fit incomplete or buggy
    code.
14. Before opening a PR, merging, or treating the branch's final commit as
    complete, run a full-diff code review gate. When the toolchain supports it,
    run that review in a fresh independent review context, preferably via a
    subagent. Look especially for side effects on adjacent code paths, data
    contracts, runtime configuration, migrations, permissions, public APIs, and
    user-visible workflows. If the review identifies a plausible side effect,
    add or run the narrow automated test, integration check, or documented
    manual validation needed to prove the risk is mitigated. Do not guess that
    side effects are safe.
15. For implementation work, a final `ready for review`, `complete`, or
    equivalent result requires a clean git checkpoint: `git status
    --porcelain --untracked-files=all` must be empty, `HEAD` must be ahead of
    the recorded baseline, and the final answer or completion record must
    include branch, commit, pushed: yes/no, and worktree_clean: true/false.
    A dirty worktree at final response is a failed gate, not a degraded
    completion.

## Behavioral Acceptance And Green Revocation

Keep these evidence states separate. Passing one state does not imply any later
state:

1. **Implementation verified**: source-level tests and review pass.
2. **Artifact published**: the intended commit was packaged and is available.
3. **Deployment applied**: the live runtime resolves to the intended immutable
   artifact. For mutable or semantic image tags, compare the tag's current
   registry digest with the runtime's resolved digest.
4. **Runtime operational**: infrastructure health and basic smoke checks pass.
5. **Behavior accepted**: the requested behavior passes through the actual
   user or service path at the highest practical boundary.

Treat this as an ordered, cumulative ladder for every runtime surface in the
requested scope. A later state cannot be green while an earlier applicable
state is pending, red, or unknown. Mark a state not applicable only with a
recorded reason, such as a documentation-only change with no published or
deployed artifact; a runtime change cannot skip artifact or deployment
identity as not applicable.

Use `fixed`, `working`, `healthy`, `complete`, or an equivalent unqualified
behavioral claim only when the requested scope has reached **Behavior
accepted**. Before then, report the exact attained state, such as "published,
not deployed" or "deployed and operational; authenticated acceptance
outstanding."

Static document checks such as `text_present`, `text_absent`, `path_exists`, or
`regex_present` can prove only properties of that local document or tree. They
must not be used as deployment, runtime-health, external-state, or behavioral
acceptance evidence. For those gates, run a command that queries the current
authoritative system and compares immutable identity; fail when credentials or
the authoritative system are unavailable. Wrapping a static file, hard-coded
success value, or cached response in a `command` check does not make it live
evidence. A live command must fail on unavailable or mismatched authoritative
state and report the identities and timestamps it actually compared.

For user-visible or cross-service changes:

- Trace every acceptance fixture to the canonical contract shape used by the
  real consumer. Prefer a captured, sanitized production-like response or an
  established canonical fixture, and record its provenance. An invented
  helper fixture must not be the sole promotion gate.
- Exercise the actual consumer component, route, command, or service seam.
  Array order, coordinate arithmetic, mocked adapters, and helper-unit tests
  are supporting evidence; they do not alone prove the rendered page or
  cross-service workflow.
- If authentication, external state, specialized hardware, or another boundary
  makes final acceptance manual, encode that manual acceptance boundary in the
  plan and keep behavioral status pending until it is explicitly satisfied.
- Behavioral evidence must be captured after the currently selected artifact
  reached the real runtime. Record the immutable runtime fingerprint, the
  deployment time, the separate browser or service session-start time, the
  observation time, and the record-update time. Require the session to start
  strictly after the latest deployment change, and require session start,
  observation, then record update in that order. Reject equality at the
  deployment boundary because it cannot prove the new runtime was available.
  For browser checks, start a new session or force a full reload and record the
  client build identity when the application exposes one.
- For deployments selected by a mutable tag, **Runtime identity** requires both
  the selected tag-to-digest resolution and the live runtime-to-digest
  resolution. A successful update status without digest equality is not a
  deployment green. Tie behavior evidence to that proven live identity. If the
  mutable tag moves after identity or behavior was accepted, that movement
  revokes **Deployment applied** and every downstream state until digest
  equality and the affected downstream gates are established again.
- When the artifact format exposes source provenance, compare its embedded
  source revision with the intended commit rather than trusting catalog text or
  a tag alone. For behavior exercised through a public URL, also prove the
  current domain, route, and integration resolve to the inspected runtime; a
  healthy unreferenced function is not user-path deployment evidence.

Any credible reproduction that contradicts an accepted result immediately
revokes the prior behavioral green. Mark the affected gate red, preserve the
reproduction as a failing test at the real boundary when practical, identify
why the earlier evidence missed it, and rerun every downstream gate after the
correction. Do not dismiss the contradiction as cache, environment, or user
error without direct evidence.

### Non-circular deployment topology

Before implementation, record how the intended artifact can reach the highest
practical acceptance boundary. Prefer a preview, staging, test, canary, or
other reversible pre-merge deployment when the repository supports one.

If repository automation can build or deploy the real acceptance artifact only
from the primary integration branch, a merge may be used as a **controlled
integration rollout** after the required operator and repository approvals.
That merge is a deployment prerequisite; it does not prove acceptance or
completion. Keep deployment identity, runtime operation, behavior acceptance,
and overall completion pending until the exact merged artifact is deployed and
the cumulative gates pass. Record the rollback or revert path before merging,
and use it if post-merge acceptance fails.

Do not weaken the consumer boundary, substitute helper-level evidence, or call
the work complete merely to avoid a required post-merge check.

## Lifecycle States

Use these meanings consistently:

- Pending means a proposal record is ready on `main`, but substantive implementation has not begun.
- Active means substantive implementation has begun and is not yet complete.
- Completed implementation means the work landed on `main`, so the proposal is no longer active.
- Discarded or superseded means the outcome was captured durably and the live
  branch or worktree should be removed instead of lingering as ambiguous truth.

## Artifact Economy

Keep one concise plan and one adjacent `.plan.toml` in `docs/plans/` for the
workstream. Reuse them across follow-up fixes, reviews, and resumptions within
that scope. One orchestration repo owns cross-repo plans; other repos need only
a pointer if local discoverability requires one. Do not create a plan family per
worker, turn, review round, or deployment of the same slice.

The plan records the goal, baseline, branch/worktree binding, effective policy,
write scope, acceptance boundary, phase order and unresolved decisions. The
manifest owns executable checks; refer to them instead of copying commands and
results into multiple documents. Put a compact closeout in the plan with result,
revision, evidence locator and remaining limitations. Separate logs, ADRs,
mirrors or per-phase notes require distinct lasting information and a reader.

Use the [Plan protocol](plan-protocol.md) only for placement/schema questions,
the [Proposal protocol](proposal-protocol.md) when implementation is deferred,
and the [Temp doc protocol](temp-doc-protocol.md) when creating temporary notes.
Scratch command output can stay in a task-scoped untracked temporary directory;
do not create a repo document merely to delete it at closeout. Keep secrets,
private operational state and original transcripts out of public Git.

## Context And Evidence Reuse

Resolve repository instructions and matching local overlays before selecting
exactly one base protocol. Explicit user instructions and applicable authorized
local overrides take precedence within their scope; retain unaffected gates.
Record the effective policy in the existing plan/handoff. Skills are adapters,
not additional independent workflows.

Read the selected base once per unchanged working context. Load other protocols,
large contracts, logs and historical plans only for the action or section needed.
After resumption, recheck instruction identity, current source and affected external
state; unchanged content need not be pasted or read in full again. A summary may
route to evidence but cannot replace a required gate.

Run a check at the boundary it proves. Reuse the result only while its relevant
inputs, source identity, environment and authority remain unchanged and its
freshness contract permits it. Changed inputs, failures, credible contradictions
or expired external observations require the affected checks again. A previous
unit test result never substitutes for current deployment identity, permissions,
liveness or user acceptance. Report commands once with concise results; keep full
logs outside the prompt and inspect failures selectively.

## Phase Structure

Each phase should be small enough to fit in one working context window and one
reviewable change slice.

For each phase record goal, write scope and exit checks. Add dependencies,
negative assertions, or document updates when applicable; omit empty template
fields. The plan may reference the manifest for checks instead of duplicating it.

### Checks

Checks prove that the phase landed. Examples:

- targeted tests
- focused validation commands
- file or route existence checks
- content assertions in docs or config

For phases that change code, checks should include both the pre-change
behavioral baseline and the post-change validation for the surfaces being
touched. Existing behavior needs passing regression coverage before the edit;
greenfield behavior needs a failing test first and the same test passing after
implementation.

### Negative Assertions

Negative assertions prevent partial migration from being presented as complete.
Examples:

- an old compatibility surface is no longer authoritative
- an obsolete path is gone
- a stale branch name is no longer documented as current

Require absence checks for removals, replacements and migrations. Additive work
does not need an invented negative assertion.

## Standard Execution Loop

1. Inspect current integration state, sync with origin when policy expects it,
   and create dedicated branch/worktree bindings. Preserve others' dirty work.
2. Create or update the single plan/manifest and prove each binding with
   `git_branch_worktree` before implementation. Run the repo-state audit when
   available; retain a compact summary rather than loading the whole inventory.
3. Load the active phase and relevant code. Establish the required pre-change
   behavioral baseline, or a failing test for greenfield behavior.
4. Implement the slice and update its required documentation. Run targeted tests
   and the phase checker against this final phase state. Rerun affected gates
   after subsequent edits; an unchanged documentation/status update alone is not
   a reason to rerun unrelated tests.
5. Advance only when the phase is green, subject to applicable local delivery
   order. At closeout remove this task's temporary residue and perform the final
   full-diff review below. Capture findings in the existing plan or review system.
6. Use the [Pull request protocol](pull-request-protocol.md) when opening a PR.
   Merge after acceptance/final gates, or use the documented controlled
   integration rollout when acceptance requires a merge. Reuse valid review
   evidence across PR preparation; opening a PR is not another review round.

## Repo-State Audit

When `agent-protocols/scripts/repo_state.py` is available, use it as the first
git-state classifier before making branch, worktree, pruning, deletion, or
cleanup decisions:

```bash
python3 agent-protocols/scripts/repo_state.py --repo . --json
```

"First" means after reading the applicable repo instructions and identifying
the work scope, but before manual `git worktree prune`, branch deletion,
checkout-directory deletion, or cleanup classification.

Use `--apply-safe-cleanup` only after a plain audit has shown deterministic safe
actions and cleanup is in scope. It must not be used to resolve dirty
worktrees, unmerged branches, ahead branches, active review branches, secrets,
migrations, production state, or any ambiguous path.

Run a second plain audit before closeout when the phase changes branch or
worktree state, or when the work includes cleanup.

## Temp Artifact Cleanup Gate

Run this gate after implementation, validation evidence, and durable docs are
in place, but before PR, merge, final code review, or final git checkpoint.

Inspect only the temporary locations and artifacts created or owned by this
workstream. Preserve unrelated active notes. For each owned temporary artifact:

- promote durable findings into `docs/plans/`, `docs/proposals/`, `docs/adr/`,
  `docs/history/`, a completion log, or the commit message
- keep only active notes that are still needed for an ongoing unclosed branch
- delete scratch inventories, draft ledgers, temporary JSON outputs, editor
  lock files, generated test remnants, and placeholder example plans that are
  not meant to survive

At closeout, this task should leave no disposable residue. If a temp artifact must remain, record why it is
still active in the plan, completion log, or final result.

## Final Code Review Gate

Run this gate after implementation and required docs updates are in place, but
before opening a PR, merging, or reporting the branch's final commit as the
complete reviewable result.

When the toolchain supports it, run the review in a fresh independent review
context, preferably via a subagent. Give the reviewer the diff, relevant
protocols, test evidence, and acceptance criteria, but not the implementer's
defensive rationale. The implementing agent still owns follow-up fixes,
validation, and final responsibility for the branch.

If a fresh independent review context is unavailable, record why it is
unavailable and perform the best available independent-style full-diff review
before proceeding.

The review must inspect the full branch diff against the recorded baseline and
ask where the change could have side effects beyond the directly edited lines.
Pay special attention to:

- adjacent call sites and shared helpers
- data contracts, schemas, migrations, and persisted formats
- runtime configuration, environment variables, feature flags, and deployment
  wiring
- permissions, authentication, billing, privacy, and security boundaries
- public APIs, CLI commands, scheduled jobs, and background workers
- user-visible flows, browser behavior, and mobile-specific layouts

For each plausible risk, prove the mitigation before proceeding:

- add or update a focused automated test when the risk is code-testable
- run the existing regression, integration, or contract test that covers the
  side effect
- perform a narrow manual validation only when automation is not practical, and
  record why that manual check is the right evidence

If the review finds a real defect or an unproven risk, return to the relevant
implementation phase. Resolve each credible side-effect risk with added or
rerun tests, or record why it is not applicable. Do not proceed to PR, merge, or
final branch checkpoint on "looks safe" reasoning alone.

After addressing review feedback, review the changed portion and its affected
interfaces when the criteria below apply. Necessary follow-up validation belongs
to the authorized task; ask only when it expands scope, permissions or material
cost. Do not restart full review of unchanged scope by default.

Run another review when any of these are true:

- review fixes materially changed production behavior, public contracts, schemas,
  migrations, auth/security/billing/privacy boundaries, deployment/runtime
  config, scheduled jobs, or background workers
- the fix touched files outside the originally reviewed diff or materially
  increased the diff size or scope
- the first review found a high-severity defect, multiple credible side-effect
  risks, or a systemic test gap
- acceptance criteria changed, or failing checks required non-trivial fixes
- meaningful uncertainty remains about correctness, security, data integrity, or
  user-visible behavior

It is usually good enough to stop without another review when all of these are
true:

- review feedback was resolved with small local edits, docs clarification, test
  evidence, or rerun checks only
- no new production behavior, public contract, storage shape, security boundary,
  deployment wiring, or user-visible flow changed after the review
- targeted tests, phase gates, and required manual validations are green
- remaining risks are documented as mitigated, accepted, or not applicable
- another review would mainly reread an unchanged diff

## Final Git Checkpoint

Before reporting implementation work as `ready for review`, `complete`,
`passed`, or an equivalent terminal state, prove the branch contains the
reviewable result.

The final checkpoint requires:

- `git status --porcelain --untracked-files=all` is empty in the implementation
  worktree
- `HEAD` is ahead of the baseline branch or commit recorded in the plan and
  manifest
- the branch is still bound to its registered implementation worktree when the
  branch remains active for review, testing, or runtime selection
- the final answer, job result, or completion log states `branch`, `commit`,
  `pushed: yes/no`, and `worktree_clean: true/false`

If durable source, doc, schema, or config changes remain uncommitted at final
response time, the result is `failed_gate`. Do not report dirty implementation
work as ready for review, and do not downgrade it to a degraded completion.

Non-mutating exploratory work does not need a git checkpoint. If exploratory or
proposal-only work creates durable repo artifacts, those artifacts must be
committed or explicitly discarded before the work can be reported as complete.

The final implementation or closeout phase should normally include both:

```toml
[[phases.implementation.checks]]
id = "repo-clean"
type = "git_clean"
repo = "."

[[phases.implementation.checks]]
id = "head-ahead-of-baseline"
type = "git_head_ahead"
repo = "."

[[phases.implementation.checks]]
id = "branch-worktree-bound"
type = "git_branch_worktree"
repo = "."
current = true
```

## Browser And Mobile Verification

Visual UI work must declare browser verification requirements. Mobile-sensitive
work must also require a narrow viewport check.

Evidence should record the route, viewport, browser/tool, target visibility,
and any captured artifact path when available. If verification cannot run, the
work may still finish, but it must finish as `degraded_verification`.

## Clean Git Closeout

When the operator asks to "clean git", do not treat that as generic pruning.
Treat it as a reconciliation pass that must end every non-main branch in one of
these dispositions:

1. merge to `main`, push, then remove the related branch and worktree
2. promote pending proposal artifacts onto `main` without leaving a live
   implementation branch behind
3. keep the branch active because substantive implementation is still in
   progress
4. discard or supersede the branch after recording the decision durably

Use the reconciliation inventory first:

```bash
python3 agent-protocols/scripts/workstream.py reconcile --json
```

The reconciliation output should compare every live branch and dirty worktree
against `main`, summarize the remaining path-level deltas, and recommend which
disposition each stream should take.

Completed or proposal-ready work should be promoted into `main` rather than
left on side branches. Historical or safety refs should remain exceptional and
explicitly named as preserved history, not as default residue from ordinary
closeout.

A clean closeout should leave the integration worktree back on a clean
`main`, with obsolete branch worktrees removed instead of lingering as
ambiguous truth.

Once the branch result is committed on `origin/main` and the remote checkpoint
exists, delete the local branch and remove its dedicated worktree unless there
is an explicit reason to preserve them.

If follow-up work is needed later, create a new branch from `main` or from the
relevant merge commit instead of treating the old implementation branch as
durable infrastructure.

## Map Refresh At Closeout

If a substantive workstream changes any surface described by the published
maps, update the published system, documentation, and test-coverage maps before
calling the workstream accepted or complete.

That usually means the repo-local `docs/system-map.md`,
`docs/documentation-map.md`, and `docs/test-coverage-map.md`, plus any relevant
`docs/cross-repo/*` or sibling product-map variants.

Do not churn the maps for work that clearly does not change any mapped surface.

## Naming And Namespace Conventions

Use one stable feature or initiative slug across branches, worktrees, plan
basenames, and temp docs when the workstream has a clear center of gravity.

Recommended patterns:

- branches:
  - `feature/<feature-slug>/<slice>-YYYY-MM-DD`
  - `docs/<feature-slug>/<slice>-YYYY-MM-DD`
- worktree directories:
  - `<repo>-<feature-slug>-<slice>`
- temp docs:
  - `docs/temp/<feature-slug>/<topic>-YYYY-MM-DD.md`

Examples:

- `feature/agent-protocols/temp-doc-governance-2026-03-30`
- `docs/agent-protocols/temp-doc-governance-2026-03-30`
- `docs/temp/agent-protocols/topology-clarification-2026-03-29.md`

This reduces branch and worktree sprawl by making related slices visually
group together instead of creating many flat one-off names.

## Current-State Ledger

If the repo keeps a live current-state audit, keep one generated repo-local
ledger such as `docs/live-workstream-status.md`.

Do not collapse live mutable branch state into the canonical planning protocol.
The plans landing page, plans index, and live-state ledger have different jobs.

That generated ledger should always be derived from git and worktree
inspection, not hand-maintained from narrative memory.

Pending proposals should appear there as pending proposals. Branchless plan
manifests should appear as branchless plan manifests: manifest-backed plan
families whose recorded branch is not currently present locally, but which are
not automatically proposals.

Active implementation work should appear as live branches. Completed
implementation should stop being represented as a live workstream once the
branch cleanup is finished.

## Archive And History

Keep these roles distinct:

- `docs/plans/archive/` for historical, promoted, superseded, or parked plan
  families, including their manifests, completion logs, and phase notes
- `docs/history/` for factual ledgers, preserved audits, migration notes,
  branch snapshots, and postmortems

Use `archive` when the artifact is still fundamentally a plan family. Use
`history` when the artifact is a factual record of what happened.

## Context Hygiene

For large streams, the active context should be:

- the current phase doc
- the current manifest
- only the code and specs needed for that phase
- only the review or ledger sections that the phase must update

Do not keep the entire epic live in context if the current phase can be proven
with a smaller working set.

## Checker Contract

Use the canonical checker:

```bash
python3 agent-protocols/scripts/check_gated_plan.py path/to/work.plan.toml --phase phase_name
```

Supported check types are illustrated in:

- [gated-phase-manifest.example.toml](examples/gated-phase-manifest.example.toml)

## Minimal Manifest Shape

The manifest is TOML so it can be parsed with the Python standard library.

Use:

- top-level `title`
- optional `branch`
- optional `root_dir`
- ordered `phase_order`
- one `[phases.<name>]` table per phase
- `depends_on` where needed
- one or more `[[phases.<name>.checks]]`

Supported check types:

- `path_exists`
- `path_absent`
- `text_present`
- `text_absent`
- `regex_present`
- `regex_absent`
- `command`
- `git_clean`
- `git_head_ahead`
- `git_merged_into`
- `git_ref_equals`
- `git_branch_absent`
- `git_branch_worktree`
- `worktree_absent`

`git_branch_worktree` accepts optional `current = true`. Use it for active
implementation, validation, and pre-merge closeout gates so a checker invoked
from a sibling checkout cannot receive a false green merely because the
intended branch is registered elsewhere. Leave it false only for deliberate
cross-worktree inventory checks.

## Branch Rule

This rule is mandatory for substantive work:

- do not continue new implementation on whatever branch happened to be checked
  out when the request arrived
- do not treat a dirty `main` worktree as the normal staging ground for new
  implementation
- create a fresh dedicated branch for the new workstream
- keep the integration branch worktree clean and reasonably up to date with the
  remote integration branch
- create a dedicated worktree for that branch instead of reusing a checkout
  that already mixes multiple streams
- add a manifest `git_branch_worktree` check that names the branch, and add a
  `path` or product-surface `contains` assertion when the branch must be
  runnable by repo tooling; set `current = true` for gates executed from that
  implementation checkout
- if the work spans repos, create a matching branch pair
- keep a stable integration worktree available for bootstrap paths, pulls,
  merges, pushes, and reconciliation

Planning-system changes are not exempt.

## Merge Rule

The intended lifecycle is:

1. branch from the integration baseline
2. implement behind gated phases
3. run every acceptance gate available before integration
4. either accept a reversible pre-merge deployment and merge back to the
   integration baseline, or invoke the documented controlled integration
   rollout when the acceptance artifact can only be created after merge
5. push the promoted result until the branch outcome is present on `origin/main`
   when the repo policy expects a remote checkpoint
6. when controlled integration rollout is required, deploy the exact merged
   artifact, prove cumulative deployment identity through behavior acceptance,
   and revert or roll back through repository controls if those gates fail
7. only after the applicable acceptance gates pass, report the work complete
   and remove the branch worktree and local branch unless explicitly preserved
8. if future work is needed, branch again from `main` or from the merge commit
   instead of reviving the old implementation branch

If a workstream is parked, superseded, or intentionally left partial, record
that in the durable plan instead of silently leaving the branch as ambiguous
truth.

## Acceptance manifest validation

The checker validates all phases before executing commands. Every phase needs at least one check; phase order must include every phase exactly once with dependencies before dependents. Missing dependencies, cycles and duplicate identifiers fail closed. Existing manifests with empty placeholder phases must add meaningful checks or remove those phases before upgrading.

For unittest command acceptance, use `min_tests = 1`, `max_skipped = 0`, and `max_expected_failures = 0`. This opt-in contract rejects exit-zero commands without the required executed tests. It checks test-run evidence, not the substantive quality of the tests or deployed behavior. Other test runners require their own evidence adapters.

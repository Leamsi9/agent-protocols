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
3. Every substantive branch has its own dedicated worktree. Keep independent
   streams isolated and record the branch/worktree binding in the plan. Verify
   the current checkout against live Git state; an optional `git_branch_worktree`
   check can automate this with `current = true`.
4. If the work spans repos, keep each repo in its own branch/worktree and use one
   canonical plan owner.
5. Use gates at consequential dependency, review, publication or acceptance
   boundaries. Ask whether a competent engineer needs the evidence before that
   action. Do not add gates merely because a process step is recoverable or a
   previous task used one.
6. One concise plan is sufficient by default. Phases, machine-readable manifests,
   receipts and checkers are optional tools when a real boundary benefits from
   them, not prerequisites for every edit, handoff or status update.
7. Respect actual dependencies and writer ownership. Independent slices need not
   wait on an artificial single-active-phase rule.
8. Back completion claims with relevant evidence. A checker is one way to record
   that evidence; a concise plan with commands, results and limitations suffices.
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
12. Choose tests by behavioral risk and the cheapest reliable level. Use
    integration tests for application interactions, focused unit/property tests
    for important logic and edge cases, and E2E tests for critical user journeys.
    Do not mandate per-function tests or fixed test ratios. Preserve meaningful
    existing regressions and derive expected outcomes from requirements, not
    the current implementation.
13. Use test-first when it clarifies a contract or reproduces a defect; neither
    existing nor greenfield code requires blanket test-first sequencing or a
    passing baseline before editing. Run risk-based pre-change checks where
    useful. After implementation, run the relevant behavioral checks and required
    phase gates; do not weaken tests to fit incomplete or buggy code.
14. Independently review the full substantive diff and resolve credible side-effect
    risks. Follow the repository's review order; absent an authorized override,
    review before publication or merge. A source handoff may be committed for
    review without claiming review or acceptance has already happened.
15. Leave a reviewable source checkpoint and identify relevant uncommitted work.
    Preserve unrelated files. Commit before publication where the repository's
    release tooling requires it; ordinary progress needs no clean-tree certificate.

## Verification and reporting

Choose checks that answer the actual engineering question. A source test,
successful build, deployed artifact, healthy service and working user interaction
establish different things; report what was actually observed without promoting
one into another. There is no required ladder of evidence states or receipt
collection. Use the existing plan, review or deployment record when a result is
useful to retain.

For UI or service changes, exercise the affected consumer at a practical boundary.
A helper-only test or mocked response cannot establish live behavior. Where live
acceptance requires unavailable access or hardware, state that limitation in plain
language. Do not invent a completion status to represent it.

Check installed identity when a deployment or stale-version concern makes it
relevant. Mutable image tags may require comparing resolved digests; a documentation
edit does not. Choose observations and records in proportion to the real risk,
without turning direct checks into a new certificate framework.

A reproduced defect changes the assessment: repair or roll back as appropriate,
retain a useful regression, and rerun affected checks. Reuse unaffected results.
Do not blame caches, users or environment without a basis, or rerun every later
check merely because a prior step changed.

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

Keep one concise plan per workstream by default. Reuse it across implementation,
follow-up fixes, review, publication and refresh; these are not separate planning
workstreams. One orchestration repo owns cross-repo plans; other repos need only
an optional pointer. Do not create a plan family per worker, turn or review round.

Record the goal, baseline, branch/worktree, effective policy, scope, acceptance
boundary, selected validation, outcome and remaining limitations. Commands and
concise results can live here. Add an adjacent `.plan.toml` only when executable
checks at a real dependency or acceptance boundary help. Separate logs, receipts,
ADRs or notes need distinct lasting information and a reader, or an explicit local
requirement; they are not generic completion prerequisites.

Use the [Plan protocol](plan-protocol.md) only for placement/schema questions,
the [Proposal protocol](proposal-protocol.md) when implementation is deferred,
and the [Temp doc protocol](temp-doc-protocol.md) when creating temporary notes.
Scratch command output can stay in a task-scoped untracked temporary directory;
do not create a repo document merely to delete it at closeout. Keep secrets,
private operational state and original transcripts out of public Git. Preserve
source/provenance for migrations and imported evidence.

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

## Optional Phase Structure

Use phases only for real dependencies or acceptance boundaries. If used, keep each
phase a reviewable slice. The risk-based testing paragraphs below retain the
0.0.21 policy: "required phase gates/checks" means gates selected for an actual
boundary by the plan or applicable local policy, not mandatory phases for all work.

For each phase record goal, write scope and exit checks. Add dependencies,
negative assertions, or document updates when applicable; omit empty template
fields. The plan may reference the manifest for checks instead of duplicating it.

### Checks

Checks prove that the phase landed. Examples:

- targeted tests
- focused validation commands
- file or route existence checks
- content assertions in docs or config

For phases that change code, select checks by behavioral risk at the cheapest
reliable level described in core rule 12. Record the risks and why the selected
checks cover them. Use pre-change checks or test-first where they clarify the
contract, reproduce a defect, or establish a useful baseline; neither is a
blanket prerequisite to editing. Preserve meaningful regressions and validate
the changed behavior after implementation and at the relevant phase gate.
Cheaper tests do not replace actual-consumer behavioral acceptance, independent
review, or required phase checks.

### Negative Assertions

Negative assertions prevent partial migration from being presented as complete.
Examples:

- an old compatibility surface is no longer authoritative
- an obsolete path is gone
- a stale branch name is no longer documented as current

Require absence checks for removals, replacements and migrations. Additive work
does not need an invented negative assertion.

## Execution

Inspect the baseline and dedicated checkout, then update the existing plan.
Implement the bounded change and select validation by the risk-based rules above.
Run relevant checks after the change; repeat only for changed inputs, failures or
stale evidence. Record concise results, not per-step proof documents.

At the repository's review boundary, obtain independent full-diff review and
resolve findings. Remove owned temporary residue and commit the clean source
result. Use the [Pull request protocol](pull-request-protocol.md) when opening a
PR. Publication, refresh and acceptance remain part of the same workstream;
report only the state actually attained. Follow local delivery order and preserve
required user approvals without inventing approvals for routine recoverable steps.

## Working-tree and temporary-file hygiene

Inspect the checkout and artifacts affected by the task. Use direct Git checks
for a targeted operation; the repo-state classifier is available when a broader
inventory helps resolve ambiguity. Ordinary work does not require a global audit
before or after cleanup.

Remove disposable files and processes this task created when they are no longer
useful. Preserve unrelated work and useful source. Keep a finding in the existing
plan or commit only when it helps future work; do not promote scratch inventories
into permanent documents merely because they were generated.

## Final Code Review Gate

Substantive source requires independent full-diff review at the repository's
chosen boundary, before publication or merge by default. Explicit user instructions
and authorized local delivery overrides control timing. Record findings in the
existing plan or review system; no separate review plan or proof document is needed.

Use a fresh independent context with the diff, relevant policy, acceptance criteria
and test evidence. A contributing implementer cannot certify independent review.
If independent review is unavailable, report it pending; self-review can support a
source handoff but cannot satisfy the independent-review requirement.

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
rerun tests, or record why it is not applicable. Do not cross the applicable
review/acceptance boundary on "looks safe" reasoning alone. A clean source checkpoint for handoff does not claim review acceptance.

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

## Source checkpoint

Keep source changes reviewable and identify the commit when handing them over.
Report material uncommitted work honestly; do not discard it to obtain a clean
status. A deployment tool may require a clean committed checkout. This is not a
universal final-answer gate or a requirement to print branch/status certificates.

## Browser And Mobile Verification

Check affected UI interactions in a browser; use a narrow viewport when mobile
behavior matters. State meaningful limitations plainly when that check cannot
run. Keep useful results in the existing workstream; screenshots, detailed
observation logs and a special degraded status are not mandatory.

## Clean Git Closeout

Clean the scope requested by the user. One finished worktree does not require
reconciling every branch, promoting unrelated proposals, pushing all work, or
moving the integration checkout to another branch. Use Git-managed removal for
clean delivered worktrees; retain branches when useful. Ancestry is not sufficient
for cherry-picked delivery, so compare patches when that matters.

Preserve dirty, active or undelivered work unless its disposal is authorized.
Resolve material ambiguity before removal, applying existing user authorization
without inventing a new approval step. Summarize useful removals or unresolved
work; no mandatory disposition ledger or cleanup certificate is required.

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

- the current plan section
- the current manifest, if used
- only the code and specs needed for that phase
- only the review or ledger sections that the phase must update

Do not keep the entire epic live in context if the current phase can be proven
with a smaller working set.

## Checker Contract

When using a manifest, run the canonical checker at the boundary it represents:

```bash
python3 agent-protocols/scripts/check_gated_plan.py path/to/work.plan.toml --phase phase_name
```

Supported check types are illustrated in:

- [gated-phase-manifest.example.toml](examples/gated-phase-manifest.example.toml)

## Minimal Manifest Shape

Optional manifests retain the existing TOML schema and checker behavior; no
migration is required for valid existing manifests. TOML can be parsed with the
Python standard library.

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
- verify the branch/worktree binding with live Git; when automating this in a
  manifest, use `git_branch_worktree` with `current = true` for the active checkout
- if the work spans repos, create a matching branch pair
- keep a stable integration worktree available for bootstrap paths, pulls,
  merges, pushes, and reconciliation

Planning-system changes are not exempt.

## Merge Rule

The intended lifecycle is:

1. branch from the integration baseline
2. implement and validate the bounded change
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

## Optional acceptance manifest validation

These rules apply only when a manifest is used. The checker validates all phases before executing commands. Every phase needs at least one check; phase order must include every phase exactly once with dependencies before dependents. Missing dependencies, cycles and duplicate identifiers fail closed. Existing manifests with empty placeholder phases must add meaningful checks or remove those phases before upgrading.

For unittest command acceptance, use `min_tests = 1`, `max_skipped = 0`, and `max_expected_failures = 0`. This opt-in contract rejects exit-zero commands without the required executed tests. It checks test-run evidence, not the substantive quality of the tests or deployed behavior. Other test runners require their own evidence adapters.

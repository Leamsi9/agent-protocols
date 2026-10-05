# Risk-based testing policy

Update upstream package policy to choose tests by behavioral risk and the
cheapest reliable level, retaining meaningful regressions, requirements-derived
expectations, actual-consumer acceptance, independent review and phase gates.

Baseline: `d5e078515f65da2c816dc05f0c2fc28b289fabfb`; version: `0.0.21`.
Branch: `feature/managed-9b955912-7089-5174-a8e4-125192743d8d`.
Worktree: the dedicated managed checkout with the same branch suffix; the
adjacent manifest proves the current branch/worktree binding.

Effective policy: the explicit user testing-policy override supersedes blanket
TDD and passing-baseline prerequisites. The substantive protocol and
`skills/gated-phase-execution/SKILL.md` apply with the worker's bounded scope.
No delegation, publication, merge, deployment, mode or role changes are authorized
here. Independent exact full-diff review is owned by Main after implementation.

Write scope: the two work protocols, VERSION and this plan/manifest. Inspection
found no contradictory enforcement in canonical docs, examples or the checker;
those surfaces need no edits. Local consumer overlays remain untouched.

## Phases and acceptance

1. **Upstream source:** reconcile substantive rules 12/13, Checks and execution
   loop, minor rules 6/7, and bump the version. The manifest checks source
   consistency, checker regressions and binding. Manually inspect the full diff
   for preserved acceptance/review gates. Source validation alone is not review
   approval or publication. Main must obtain independent review of the exact
   full diff before publication or proceeding downstream.
2. **Dependent Leam refresh:** after review-approved upstream publication, Main
   installs the exact source into a dedicated consumer worktree, records source
   commit/version/lock provenance, and verifies package identity and preserved
   local overlays. Preserve unrelated dirty/conflicted root work and active jobs.
   Leam's canonical parent ticket owns executable refresh evidence, required
   runtime/actual-consumer checks and user acceptance. The local manifest keeps
   this phase blocked until orchestration supplies its authoritative gates; a
   static upstream file must never certify downstream acceptance. Preserve the
   designated Deployer and existing modes/pauses.

## Validation and handoff

The risk is contradictory policy or weakened gates. Text inspection and absence
checks cover the removed mandates; existing checker tests cover manifest gate
semantics. No implementation-mirroring policy tests are added. Commands live in
the adjacent manifest; run its `upstream` phase for this worker's source checks.

Validation: upstream phase passed (including two checker regression tests, no
skips); the dependent refresh phase failed closed as intended. Implementer
full-diff inspection found acceptance and review gates preserved. This is not
independent review; the worker is explicitly prohibited from delegating it.

Implementation status: source edits validated; independent review, publication,
Leam refresh and user acceptance pending. Final source revision and command
results are reported in the worker handoff. No runtime deployment, QA/UAT or
consumer refresh is claimed. No task-owned temporary artifacts remain.

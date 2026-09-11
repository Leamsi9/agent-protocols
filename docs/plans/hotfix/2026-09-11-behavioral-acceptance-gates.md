# Behavioral acceptance and false-green gates

- Goal: prevent build, deployment, proxy-test, or runtime-health evidence from
  being reported as user-visible acceptance before the real behavior has been
  exercised.
- Baseline: `origin/main` at `d0cb948`.
- Branch: `fix/behavioral-acceptance-gates-2026-09-11`.
- Write scope: the canonical substantive-work protocol, its plan family, and
  plan index only.
- Production boundary: documentation/process change only; no product runtime,
  deployment, or environment mutation.

## Diagnosis

Two MatterPD regressions were repeatedly marked green because separate layers
of evidence were collapsed into one status. A Lambda could be healthy while
still running an older image than its selected semantic tag, and isolated
coordinate tests could pass while modeling a hierarchy different from the
canonical response consumed by the page. A user's deployed-path reproduction
therefore contradicted the claimed result.

## Phases

### Branch setup

Create the dedicated worktree and this fail-closed plan family.

### Protocol update

Define distinct implementation, publication, deployment, runtime-identity,
and behavioral-acceptance states. Require canonical contract-shaped fixtures
and a test at the actual consumer boundary for user-visible behavior. Make any
credible user reproduction revoke prior green evidence immediately, and
prohibit "fixed", "healthy", or equivalent behavioral claims while a required
authenticated/manual acceptance boundary is outstanding.

### Validation

Run the manifest checks, review the full diff independently, and leave a clean,
pushed source checkpoint suitable for an upstream PR. Consumer refreshes are a
separate, explicit follow-up after upstream acceptance.

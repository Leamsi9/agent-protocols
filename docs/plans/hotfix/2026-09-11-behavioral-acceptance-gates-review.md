# Behavioral acceptance gates independent-review correction

- Goal: make the behavioral evidence ladder cumulative and prevent its merge
  rule from becoming circular in repositories that deploy only integration
  commits.
- Baseline: reviewed source commit `ce0f46b`.
- Branch: `fix/behavioral-acceptance-gates-review-2026-09-11`.
- Write scope: the canonical substantive-work protocol and this plan family.
- Runtime boundary: documentation and process only; no product code,
  deployment, or environment mutation.

## Review findings

The reviewed rules directly prevent both known MatterPD false greens: mutable
deployment tags require registry-to-runtime digest equality, and helper-only
fixtures cannot prove user-visible behavior. Two generic gaps remained. The
evidence states were described as separate but not explicitly cumulative, and
the unconditional pre-merge acceptance rule could be circular where only the
integration branch can produce a deployable acceptance artifact.

## Phases

### Branch setup

Create a separate review-fix branch and worktree from the reviewed commit so
the upstream review target remains untouched.

### Protocol correction

Make every applicable evidence state cumulative, invalidate downstream greens
when a mutable tag moves, and define a controlled integration rollout for
deployment topologies that cannot support pre-merge acceptance. A merge used
for that rollout remains pending rather than being treated as acceptance.

### Validation

Run the complete protocol test suite, all manifest gates, diff checks, and a
full consistency review. Leave a clean, pushed checkpoint for the parent to
evaluate; do not merge or deploy it.

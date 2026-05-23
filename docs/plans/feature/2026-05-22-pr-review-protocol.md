# PR Review Protocol Update

Status: active
Branch: `main`
Baseline: `origin/main`
Worktree: `/home/ismael/Github/agent-protocols`

## Goal

Add a reusable final code-review gate to the substantive and minor work
protocols, focused on side-effect risk and evidence-backed validation. Add an
invocable pull request protocol with a standardized PR description format.

## Scope

Package-owned files:

- `substantive-work-protocol.md`
- `minor-work-protocol.md`
- `merge-to-main-protocol.md`
- `pull-request-protocol.md`
- `scripts/install.py`
- `README.md`
- `VERSION`
- tests under `tests/`

Workstream files:

- this plan
- `docs/plans/feature/2026-05-22-pr-review-protocol.plan.toml`
- `docs/plans/plans-index.md`

No consumer repo refresh is part of this slice unless requested separately.

## Phases

### setup

Goal: prove this is a branch-owned worktree and establish the durable plan.

Exit gate: branch/worktree binding and plan artifacts pass the manifest.

### protocol_updates

Goal: add the side-effect-focused final code review gate to the substantive and
minor protocols, prefer a fresh independent review context when supported, and
add the invocable PR protocol.

Exit gate: both work protocols require side-effect review before PR or final
branch checkpoint, the review gate prefers a fresh independent context when
supported, and the PR protocol documents the required sections.

### packaging

Goal: make the PR protocol available to consumers through the normal package
surface.

Exit gate: installer vendoring and README/version metadata include the new
protocol.

### validation

Goal: run focused and full package validation.

Exit gate: installer tests, full unit tests, script compilation, and the phase
checker pass.

### closeout

Goal: commit the package change and leave the branch in a clean reviewable
state.

Exit gate: `HEAD` is ahead of `origin/main` and the worktree is clean.

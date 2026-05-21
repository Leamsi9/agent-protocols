# Plans Index

This directory stores durable plan families for the consuming repo.

The canonical reusable planning guidance lives in:

- [Agent protocols plan protocol](../../plan-protocol.md)

Live branch and worktree state is tracked separately in:

- [Live workstream status ledger](../live-workstream-status.md)

## Taxonomy

Use these stable subdirectories:

- `feature/` for product or engineering feature plans
- `sync/` for upstream sync or convergence plans
- `hotfix/` for urgent corrective plans
- `proposals/` for proposal-only plan families
- `archive/` for parked, superseded, promoted, or historical plan families
- `cross-repo/` as an orchestrator-only extension for canonical plan families
  whose completion or acceptance depends on coordinated work across 2+ repos

Within `docs/plans/proposals/`, use explicit status buckets when helpful:

- `active/`
- `pending/`
- `blocked/`
- `in-progress/`

Those buckets are optional. Compact proposal records can also live directly
under `docs/plans/proposals/` when status folders would add noise.

A `.plan.toml` manifest is a phase-gate artifact paired with a durable plan. It
is not the same thing as a proposal log. Proposal logs are optional repo-owned
surfaces, not required companions for every proposal.

## Durable Plan Surfaces

### `feature/`

- [Example workstream](feature/example-workstream.md)
- [Citation verification protocol extraction, 2026-05-09](feature/2026-05-09-citation-verification-protocol.md)
- [PR review protocol update, 2026-05-22](feature/2026-05-22-pr-review-protocol.md)

### `sync/`

- [Minor work protocol package sync, 2026-04-29](sync/2026-04-29-minor-work-protocol-package-sync.md)
- [Closeout git gate package sync, 2026-05-02](sync/2026-05-02-closeout-git-gate-package-sync.md)
- [Protocol quality gate unification, 2026-05-02](sync/2026-05-02-protocol-quality-gate-unification.md)
- [Git cleanup skill package sync, 2026-05-03](sync/2026-05-03-git-cleanup-skill-package-sync.md)

### `hotfix/`

None.

### `proposals/`

None.

### `archive/`

None.

### `cross-repo/`

- [Cross-repo extension README](cross-repo/README.md)

# Live Workstream Status

This ledger is the repo-local mutable current-state surface for active
workstreams, manifest-backed pending proposals, and other manifest-backed plan
families. Compact proposal records without manifests remain valid durable docs
but may not appear in this generated ledger.

## Definitions

- A manifest is a `.plan.toml` phase-gate file paired with a durable plan.
- Manifests are not proposals by default.
- Pending proposals are branchless plan families whose plan records
  `Proposal state: pending`.
- Branchless Plan Manifests are manifest-backed plan families whose recorded
  branch is not currently present locally and that are not classified as
  pending proposals.

Refresh this ledger with:

- `python3 scripts/workstream.py sync-index --confirm`

<!-- BEGIN GENERATED WORKSTREAM STATE -->
## Generated Status Snapshot

This section is generated from live git and worktree state by the agent-protocols workstream script.

_Last generated: 2026-05-09T00:58:10.676729+00:00_

### Summary
| Repo | Main | Non-main branches | Attached worktrees | Dirty worktrees |
| --- | --- | --- | --- | --- |
| agent-protocols | main | 2 | 3 | 1 |

### Active, Promotable, And Diverged Branches
| Repo | Branch | Class | Worktree | State | Ahead | Behind | Plan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent-protocols | feature/citation-check-protocol-2026-05-09 | active | agent-protocols-citation-check-protocol-2026-05-09 | clean | - | - | [2026-05-09-citation-verification-protocol.md](/home/ismael/Github/.worktrees/agent-protocols-citation-check-protocol-2026-05-09/docs/plans/feature/2026-05-09-citation-verification-protocol.md) |

### Historical And Merged-Stale Branches
| Repo | Branch | Class | Worktree | State | Ahead | Behind | Plan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent-protocols | feat/ies-suggestion-foundations-2026-03-30 | merged_stale | agent-protocols-ies-suggestion-foundations | dirty | - | - | - |

### Pending Proposals Without Live Branches
None.

### Branchless Plan Manifests
| Branch | Class | Status | Proposal State | Plan |
| --- | --- | --- | --- | --- |
| chore/minor-work-protocol-package-sync-2026-04-29 | branchless_plan | completed | none | [2026-04-29-minor-work-protocol-package-sync.md](/home/ismael/Github/.worktrees/agent-protocols-citation-check-protocol-2026-05-09/docs/plans/sync/2026-04-29-minor-work-protocol-package-sync.md) |
| feature/agent-protocols/temp-doc-governance-2026-03-30 | branchless_plan | in progress | none | [agent-protocols-temp-doc-governance-2026-03-30.md](/home/ismael/Github/.worktrees/agent-protocols-citation-check-protocol-2026-05-09/docs/plans/cross-repo/feature/agent-protocols-temp-doc-governance-2026-03-30.md) |
| feature/closeout-git-gate-2026-05-02 | branchless_plan | unknown | none | [2026-05-02-closeout-git-gate-package-sync.md](/home/ismael/Github/.worktrees/agent-protocols-citation-check-protocol-2026-05-09/docs/plans/sync/2026-05-02-closeout-git-gate-package-sync.md) |
| feature/git-cleanup-skill-2026-05-03 | branchless_plan | unknown | none | [2026-05-03-git-cleanup-skill-package-sync.md](/home/ismael/Github/.worktrees/agent-protocols-citation-check-protocol-2026-05-09/docs/plans/sync/2026-05-03-git-cleanup-skill-package-sync.md) |
| feature/protocol-quality-gate-unification-2026-05-02 | branchless_plan | unknown | none | [2026-05-02-protocol-quality-gate-unification.md](/home/ismael/Github/.worktrees/agent-protocols-citation-check-protocol-2026-05-09/docs/plans/sync/2026-05-02-protocol-quality-gate-unification.md) |
<!-- END GENERATED WORKSTREAM STATE -->

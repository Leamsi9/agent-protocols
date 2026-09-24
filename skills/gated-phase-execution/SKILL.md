---
name: gated-phase-execution
description: Use for substantive implementation that needs durable phase gates or coordinated cross-repository work. Ordinary minor edits and proposal-only capture use their repository protocols directly.
---

# Gated Phase Execution

Resolve repository instructions and its local trigger index before planning.
Apply matching authorized overlays, then the substantive base from the package
location supplied by the environment or repository. Package-source checkouts use
`substantive-work-protocol.md`; consumers normally use
`agent-protocols/substantive-work-protocol.md`. Do not reread unchanged policy or
load every linked protocol. This skill adds no separate execution workflow.

Use one plan and adjacent manifest per workstream, including scoped follow-ups.
The plan records decisions and effective policy; the manifest owns checks. Reuse
an existing suitable branch/worktree on resumption. New substantive work uses a
dedicated branch/worktree; place linked checkouts in workspace `.worktrees/`,
never tracked `.github/`. Cross-repo work has one plan owner and separate worktrees.

Load only the active phase and relevant evidence. Honor local delivery order and
parallelism overrides. Run the applicable checker after the slice and its docs
are ready, then repeat only for changed inputs or stale evidence:

```bash
python3 agent-protocols/scripts/check_gated_plan.py path/to/work.plan.toml --phase phase_name
# Package source: python3 scripts/check_gated_plan.py ...
```

Never replace a failing check with a narrative completion claim. Keep substantive
independent review and final clean checkpoint requirements from the base. Do not
create a review worker, mirror, ledger or new plan merely to satisfy this adapter.

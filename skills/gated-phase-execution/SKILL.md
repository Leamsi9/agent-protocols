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

Use one concise plan per workstream, including scoped fixes, reviews and refresh.
A manifest is optional when executable checks help at a real dependency or
acceptance boundary. This adapter adds no per-step phase, receipt or proof-file
requirement. Explicit user instructions and authorized local overrides take
precedence within scope; retain unaffected requirements.

Reuse a suitable branch/worktree on resumption. New substantive work uses a
dedicated branch/worktree; place linked checkouts in workspace `.worktrees/`,
never tracked `.github/`. Cross-repo work has one plan owner and isolated checkouts.
Load only the current plan section and relevant evidence. Honor local review and
delivery order; the generic default is independent review before publication.

If a manifest is selected, run its applicable checks at the boundary it represents:

```bash
python3 agent-protocols/scripts/check_gated_plan.py path/to/work.plan.toml --phase phase_name
# Package source: python3 scripts/check_gated_plan.py ...
```

Existing valid manifests remain compatible. Repeat checks for changed inputs or
stale evidence, not each recoverable step. Never replace a failing check with a
completion claim. Keep the base's risk-based tests, actual-consumer acceptance,
privacy, independent review and clean committed source requirements. Record concise
results in the existing plan; no separate review plan or ledger is needed.

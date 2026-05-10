# Citation Substance Review Protocol

Status: active
Branch: `feature/citation-substance-review-2026-05-10`
Baseline: `origin/main`
Worktree: `/home/ismael/Github/.worktrees/agent-protocols-citation-substance-review-2026-05-10`

## Goal

Make the citation-verification package explicit about agent-led scholarly
judgement for source-content relevance. The package should keep deterministic
gates for coverage and schema enforcement, while giving assistants a reusable
rubric for deciding whether a cited source substantively supports its invocation
context.

## Scope

Package-owned files:

- `citation-verification-protocol.md`
- `scripts/citation_check_content_support.py`
- `tests/test_citation_tools.py`
- `skills/citation-substance-review/SKILL.md`
- `scripts/install.py`
- `README.md`
- `VERSION`

Consumer refreshes are out of scope for this package branch. They happen only
after the package change is merged to `main`.

## Phases

### setup

Goal: prove this is a branch-owned substantive worktree with durable plan
artifacts.

Exit gate: the branch/worktree binding, plan, and manifest all pass.

### protocol

Goal: document the agent substance-review rubric, support-type vocabulary, and
rich content-support ledger fields.

Exit gate: the protocol describes direct, contextual, method, partial,
misplaced, unsupported, and blocked support, and the skill adapter exists.

### tooling

Goal: add deterministic schema enforcement for rich content-support ledgers
without breaking existing basic ledgers.

Exit gate: focused tests prove basic compatibility, substance-schema failure on
incomplete rows, and substance-schema success on complete rows.

### packaging

Goal: make the skill adapter and updated citation tooling available through the
normal package installer.

Exit gate: README and installer vendoring include the new skill and all tests
pass.

### closeout

Goal: commit the package change and leave the branch clean.

Exit gate: `HEAD` is ahead of `origin/main` and the worktree is clean.

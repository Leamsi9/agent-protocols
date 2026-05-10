# Text Authorship Integrity Protocol

Status: active
Branch: `feature/text-authorship-protocol-2026-05-10`
Baseline: `origin/main`
Worktree: `/home/ismael/Github/.worktrees/agent-protocols-text-authorship-2026-05-10`

## Goal

Add a reusable, repo-agnostic protocol for reviewing scholarly prose in light of
modern AI-text detection research without turning the package into a detector
evasion or "humanizer" toolkit. The package should help assistants preserve
human authorship, source-grounded reasoning, transparent provenance, and
document-specific voice, while treating commercial and open detectors as
diagnostic signals rather than dispositive proof.

## Scope

Package-owned files:

- `text-authorship-integrity-protocol.md`
- `scripts/text_authorship_audit.py`
- `tests/test_text_authorship_audit.py`
- `skills/text-authorship-integrity/SKILL.md`
- `scripts/install.py`
- `README.md`
- `VERSION`

Consumer refresh into the manuscript repo is handled after the package branch is
green.

## Phases

### setup

Goal: prove this is a branch-owned substantive worktree with durable plan
artifacts.

Exit gate: the branch/worktree binding, plan, and manifest all pass.

### protocol

Goal: document the authorship-integrity workflow, detector-state assumptions,
allowed and disallowed revision actions, and ledger expectations.

Exit gate: the protocol rejects detector evasion, requires provenance review,
and describes detector outputs as diagnostic review signals.

### tooling

Goal: add a deterministic local audit script that flags formulaic or
provenance-thin passages for human review without claiming to classify AI
authorship.

Exit gate: focused tests prove paragraph extraction, marker scoring, baseline
comparison, and TOML ledger output.

### packaging

Goal: make the new protocol, script, and skill adapter available through normal
package vendoring.

Exit gate: README, installer vendoring, package version, unit tests, and Python
compilation are green.

### closeout

Goal: commit the package change and leave the branch clean.

Exit gate: `HEAD` is ahead of `origin/main` and the worktree is clean.

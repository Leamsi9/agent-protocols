# Pull Request Protocol

Use this protocol when an operator asks to draft, open, review, or revise a PR
description, or when another agent protocol says to prepare a PR.

This protocol governs the PR body. Use the
[Merge to main protocol](merge-to-main-protocol.md) for branch promotion and
merge mechanics.

## Required Preparation

Finish the selected base protocol's cleanup, validation and review gates before
opening the PR. Reuse evidence for the same diff and applicable environment; do
not repeat those gates solely to write a PR body. If the diff or relevant evidence
changed, rerun only affected checks/review under that base protocol. Explain
unresolved limitations without implying acceptance.

## Format

Follow the repository PR template when present. Otherwise a small change needs
only the concrete problem/result and validation. For substantive changes use
these sections when they help reviewers: Issue or Feature, Implementation
Rationale, Risks and Mitigations, Tests. Omit empty or redundant sections; include
material risks and limitations regardless of the layout.

### Issue or Feature

Describe the bug behavior or the intended feature behavior.

For a bug, state the externally observable failure and the expected behavior.
For a feature, state the intended capability and the behavioral acceptance
outcome. Keep implementation details out of this section unless they are
needed to identify the affected behavior.

### Implementation Rationale

For a bug fix, explain the technical cause of the problem and why the solution
addresses it.

For a feature, explain the technical requirements and how the implementation
meets them. Name important changed modules, contracts, migrations, jobs, or
runtime surfaces when that helps reviewers understand the approach.

### Risks and Mitigations

List the meaningful risks and side effects considered, especially risks to
adjacent code paths, data contracts, runtime configuration, permissions, public
APIs, and user-visible workflows.

For each risk, include the mitigation. When the mitigation is a test or
validation command, refer to the command and result recorded once under `Tests`.

If there are no meaningful risks beyond a docs-only or local-only edit, say so
explicitly and name the boundary that makes the risk local.

### Tests

List the tests, checks, and manual validations run for the PR. Include command
names and results.

If a normally relevant check was not run, say `Not run` and give the reason.
Do not omit skipped checks silently.

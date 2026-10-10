# Delegated Work Protocol

This protocol wraps delegated sandbox jobs for a repo that vendors
`agent-protocols/`. It governs only behavior that is unique to delegated
sandbox execution.

Delegated work is not a third category of work. Any delegated job that performs
coding work or mutates repo files must adopt either the
[Substantive work protocol](substantive-work-protocol.md) or the
[Minor work protocol](minor-work-protocol.md) before editing files.

Use the minor protocol only when all of its criteria are true. Use the
substantive protocol for everything else, including any change that crosses
repos or ownership boundaries, touches a public surface, changes a schema or
contract, needs multiple reviewable slices, or carries meaningful product,
runtime, or security risk. If the job is non-mutating research or exploration,
record that as `protocol_adopted: non_mutating`.

## Scope And Cost

Use delegation for a bounded independent task or a required independent review,
not to satisfy a worker count or duplicate an existing check. A read-only reviewer
can adopt `non_mutating` and use the parent's plan/evidence; it does not need a new
branch, manifest, completion log or implementation protocol run. The parent retains
responsibility for the substantive gate and accurate child quality reporting.

Pass the effective policy, source identity, acceptance criteria and relevant paths.
Do not copy the whole conversation, historical backlog or already available logs
by default. Preserve any preflight or quality evidence required by local policy.

## Handoff And Evidence

Before editing, confirm the bounded assignment, selected base protocol, effective
local overrides, baseline/source identity, branch/worktree and write ownership.
Carry the configured model/effort, permissions, dependencies and acceptance criteria
when the repository uses them. Verify these facts from the available authoritative
runtime and Git state; prompt text alone is not proof of runtime enforcement.
Stop on conflicting ownership or uncertain effects rather than launching a duplicate.

Use the parent's plan and existing transport receipt or job result. The generic
package does not require a new preflight report, injected gate receipt, child plan,
quality log or machine-readable manifest. A consuming runtime may require such
records at its dispatch/authority boundary; preserve that local contract and report
missing evidence honestly. Do not invent successful receipts.

For substantive mutation, use a dedicated registered branch/worktree. Audit ambiguous
Git state before cleanup; delegation grants no cleanup or publication permission.
Read-only review needs no implementation branch or separate plan.

## Completion And Follow-Up

Return the scoped result, source identity, checks and limitations in the existing
handoff or job result. Mutating source handoffs require the base protocol's clean
committed checkpoint. Distinguish source validation from independent review,
publication, deployment and actual-consumer acceptance. Missing browser verification
or failed checks remain visible; do not present them as passed.

The parent retains responsibility for integration and accurate quality reporting.
Preserve each child's unresolved failure or limitation rather than hiding it behind
a successful aggregate. Existing runtime states such as `passed`,
`degraded_preflight`, `degraded_workers`, `degraded_verification` and `failed_gate`
remain compatible, but this package does not require a separate quality log.

Resumed or follow-up workers inherit the same scope and policy unless explicitly
changed. Recheck changed source, ownership and authority; reuse unchanged evidence.
Necessary fixes and review remain in the same workstream. Neither delegation nor
this adapter creates permission to dispatch more workers.

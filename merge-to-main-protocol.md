# Merge To Main Protocol

This protocol keeps production and mainline changes inspectable, auditable, and
reversible.

## Rule

Agents must not push directly to `main`.

All substantive or production-affecting changes must be promoted to `main` by a
GitHub pull request, even when the agent is asked to create and accept the PR.

## Required Flow

1. Start from a clean branch or worktree based on current `origin/main`.
2. Commit the scoped change on the branch.
3. Run the final code review gate from the applicable substantive or minor
   work protocol, resolving any side-effect risk with tests or documented
   validation before PR.
4. Draft the PR body with the [Pull request protocol](pull-request-protocol.md).
5. Push the branch and open a pull request to `main`.
6. Let GitHub Actions run for the branch or PR when configured.
7. Merge with GitHub PR tooling after checks pass or after recording why checks
   are unavailable.
8. Prefer guarded CLI merges with the full `headRefOid`, for example
   `gh pr merge --merge --delete-branch --match-head-commit <headRefOid>`.
9. Verify the post-merge `main` workflow or deployment when the repo has CI/CD
   on `main`.
10. Leave a rollback path in the PR description or in a follow-up rollback PR
   for production changes.

## Emergency Exception

Direct pushes to `main` are allowed only when the user explicitly requests an
emergency direct push and the final report records:

- the reason PR flow was bypassed
- the exact commit or commits
- the verification performed
- the rollback command or rollback PR path

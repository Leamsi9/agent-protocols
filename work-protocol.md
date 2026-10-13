# Work protocol

Deliver useful, small, reversible changes. Spend care where a concrete risk
exists and nowhere else. The repository's `AGENTS.md` adds local facts and
takes precedence; the user's explicit instructions take precedence over both.

## Flow

1. **Take one piece of work.** Read the parts of `AGENTS.md` and the code your
   task touches. Work on a branch in its own worktree, created from the current
   main branch.
2. **Plan in proportion.** A few lines in the ticket, PR or commit message are
   usually enough. Write a separate plan only when the user asks for one or the
   work spans several releases; keep it current and short.
3. **Build in small increments.** Each increment should be usable or at least
   harmless on its own, so it can ship without waiting for the rest.
4. **Test by risk.** Test what could plausibly break, at the cheapest level
   that would catch it. Exercise user-facing behaviour through its real
   consumer (browser, API, CLI) when that is practical. Keep useful regression
   tests; derive expectations from requirements, not from current behaviour.
5. **Integrate on main.** Rebase or merge onto the current main branch and
   resolve conflicts there. Main is the only line that gets released.
6. **Release through the repository's one release path**, then review and
   check the released result. Problems found afterwards become ordinary work;
   a serious live failure is fixed forward or rolled back immediately.
7. **Report plainly:** what changed, what you checked and how, and what you did
   not check.

## Where extra care is required

Apply proportionate safeguards to these concrete risks, and to similar ones you
recognise:

- **Concurrent writers.** One owner per worktree, ticket or data store at a
  time.
- **Destructive or irreversible changes.** Back up first and get explicit
  approval for data deletion, destructive migrations, force pushes or replacing
  a running installation.
- **Credentials and private data.** Keep them out of Git, logs and prompts.
- **External actions that must not repeat** (messages, payments, calendar
  writes). Use a request identifier so a retry cannot perform the action twice;
  when the outcome is unknown, find out before retrying.
- **Outward-facing actions** (publishing, sending, pushing). Confirm unless the
  user has authorised them.

## Keep the system small

- Add a new persisted state, status, record type, approval step or checking
  tool only when the user asks for that mechanism or one of the risks above
  requires it. Prefer the states and operations that already exist.
- When the user asks for an outcome ("stop that job", "it's ready", "drop
  this"), carry out the outcome. Do not turn the word into a new concept in
  the system.
- When an edge case seems to need another field or rule, look first for a
  simpler model that removes the edge case.
- Prefer deleting code, text and configuration to adding them.
- Git history is the archive. Keep handoffs, logs and superseded instructions
  out of files that agents read as current guidance.

## Working with other agents

- Give a delegate the task, the acceptance check and the relevant paths. Do
  not forward transcripts or copies of policy.
- An independent reviewer (not the author) reads the diff and reports findings
  in plain language. When review happens relative to release is set by
  `AGENTS.md`.
- A running session keeps the instructions it started with. After governing
  instructions change, restart the sessions whose work depends on the change;
  other sessions continue.

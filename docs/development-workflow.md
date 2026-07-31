# Development Workflow

## Purpose

This workflow keeps Codex implementation work controlled, reviewable, and
traceable to approved GitHub Issues.

GitHub Issues and GitHub Projects are the source of truth for tasks, priority,
status, and deadlines. Repository Markdown documents may describe workflow and
technical state, but must not duplicate the backlog.

## Issue Selection And Approval

The user and ChatGPT select and approve the issue to work on. Codex must not
choose its own next task.

Before implementation starts, Codex must know:

- the GitHub Issue number
- the approved scope
- the expected branch or branch naming pattern
- any explicit restrictions from the user

If any of these are missing or unclear, Codex must stop and ask for
clarification.

## Assignment To Codex

Codex works on exactly one explicitly assigned issue at a time.

Codex must inspect the assigned GitHub Issue before implementation. When
GitHub CLI access is available, use:

```bash
gh issue view <issue-number>
```

If the Issue cannot be retrieved, Codex must request the complete issue body
and acceptance criteria instead of guessing.

Codex may inspect repository files, current branch state, recent commits, and
relevant documentation. Codex must not begin editing until the assigned issue
and branch are clear.

## Branch Creation And Verification

Every task requires a dedicated non-`main` branch.

Before editing, Codex must run:

```bash
git status -sb
git branch --show-current
```

Codex must verify that:

- the branch is the dedicated branch for the assigned issue
- the branch is not `main`
- no unexplained modified or untracked files already exist

If unexplained changes exist, Codex must stop before editing.

Codex may create a branch only when explicitly authorized for that exact action
in the current task.

## Exact-Action Authorization

Codex may perform these actions only when explicitly authorized for that exact
action in the current task:

- create a branch
- stage files
- commit
- push
- open a pull request

Authorization for one action does not authorize any other action.

## Implementation Boundaries

Codex must keep changes limited to the approved issue scope.

Codex must not:

- expand scope without approval
- implement unrelated cleanup
- modify application or database code for documentation-only issues
- add dependencies unless the issue requires them and the user approves
- hard-code passwords, API keys, tokens, or database credentials
- bypass CAPTCHAs, authentication, paywalls, or access controls

Codex must preserve existing useful content and working functionality.

## Self-Review

Before handoff, Codex must review its own diff for:

- unrelated changes
- accidental secrets
- scope creep
- stale or contradictory documentation
- missing validation notes
- formatting problems

Codex should use:

```bash
git diff --check
git diff --stat
git status -sb
```

## Validation

For repository changes, Codex must run the default validation set:

```bash
ruff check .
python -m pytest -q
python -m compileall -q main.py src
git diff --check
```

When the project `.venv` exists, Codex must use its Python environment for
Python, pytest, Ruff, and dependency commands rather than relying on globally
installed tools.

The default validation set must run unless:

- a command is technically inapplicable or unavailable
- project management explicitly approves a different validation set for the
  assigned issue

If validation cannot run because of missing credentials, unavailable services,
or environment problems, Codex must report that clearly and avoid treating the
work as fully verified.

Every skipped or replaced command must be reported with the reason.

## Pull Request Creation

Codex must not open a pull request unless explicitly authorized for that exact
action in the current task.

When PR creation is authorized, the PR must:

- link the assigned issue
- describe the implemented scope
- list changed files
- include validation commands and results
- call out risks, limitations, and documentation impact
- confirm no unrelated changes
- confirm no secrets were committed

Use `.github/pull_request_template.md` as the PR body checklist.

## Human Review

The user and ChatGPT review Codex changes before merge. Codex must treat review
feedback as the next source of implementation direction.

Codex must not mark review conversations resolved or approve its own work.
Management handles review resolution and acceptance.

## Requested Revisions

For requested revisions, Codex must:

- confirm the revisions belong to the same assigned issue
- keep changes on the same task branch unless instructed otherwise
- avoid overwriting unrelated user changes
- rerun validation after edits
- provide an updated handoff report

If revisions introduce new scope or architectural decisions, Codex must stop
and ask for approval.

## CI Review

After a PR exists, CI results are reviewed before merge.

Codex may inspect CI failures when asked. Codex must not assume that local
validation replaces CI, and must not change CI configuration unless that is
inside the assigned issue scope.

## Merge Authorization

Only the user or an explicitly authorized maintainer may merge pull requests.

Codex must never merge a pull request or close an issue. Merge and issue
closure are management responsibilities.

Codex may only report that merge or issue closure is now required.

## Branch Cleanup

Branch cleanup happens after merge.

Management deletes the remote and local task branches. Codex does not delete
branches or perform branch cleanup.

## GitHub Project Status Changes

GitHub Projects remain the source of truth for status and scheduling.

Codex must never change GitHub Project status, priority, deadlines, fields,
iteration, or assignments. These are management responsibilities.

Codex may only report that a management action is now required.

## Project Status Transitions

Management owns these status transitions:

- Todo -> In Progress: management assigns the issue
- In Progress -> In Review: management opens or accepts the PR for review
- In Review -> In Progress: management requests revisions
- In Review -> Done: management merges and confirms completion

Codex must not perform these transitions. Codex may only report the
recommended next transition in its handoff.

## Stop Conditions And Escalation

Codex must stop and request clarification when:

- no issue is assigned
- more than one issue is assigned for implementation at the same time
- the assigned issue cannot be retrieved and the complete issue body and
  acceptance criteria were not provided
- requirements conflict
- required context is missing
- the work requires an architectural or product decision
- the requested change would expand beyond the approved issue
- the branch is `main`
- the branch is not the dedicated branch for the assigned issue
- unexplained modified or untracked files already exist
- validation needs unavailable secrets or external services
- there is a risk of exposing secrets
- unrelated worktree changes block a safe implementation

Escalation should include the blocker, the decision needed, and the smallest
reasonable next step.

## Required Codex Handoff Format

After implementation, Codex must return:

1. concise summary
2. files changed
3. important design choices
4. validation commands and results
5. assumptions or unresolved questions
6. output of `git diff --stat`
7. output of `git status -sb`

The handoff must mention any validation that failed or could not be run.

# ADR-0001: Codex Contribution Workflow

## Status

Accepted

## Context

The repository uses Codex to assist with implementation work. Without a
controlled workflow, an implementation agent could choose tasks, expand scope,
edit the wrong branch, bypass review, or mix product backlog content into
repository documentation.

The workflow is needed to separate management decisions, implementation work,
and review and acceptance authority.

GitHub Issues and GitHub Projects remain the source of truth for task
selection, priority, status, assignments, and deadlines. The repository needs
local operating instructions that Codex can follow without duplicating the
backlog.

## Decision

Use Codex as a controlled implementation engineer.

The user and ChatGPT manage task selection, planning, prioritization,
architecture decisions, review, and acceptance. Codex acts only as the
implementation engineer for explicitly assigned work.

Codex works on exactly one explicitly assigned GitHub Issue at a time and only
on a dedicated non-`main` branch. Before editing, Codex verifies the Issue,
branch, and worktree state. Codex keeps implementation within the approved
scope, validates and self-reviews its work, and provides a structured handoff.

Codex may create a branch, stage files, commit, push, or open a pull request
only when explicitly authorized for that exact action in the current task.
Authorization for one action does not authorize any other action. Git and
GitHub actions have different effects and must remain independently
controlled.

Codex must never merge a pull request, close an Issue, change GitHub Project
status, priority, deadlines, fields, iterations, or assignments, approve its
own work or resolve management review, delete local or remote branches, or
perform post-merge branch cleanup. These remain management responsibilities
and cannot be delegated through ordinary task authorization.

Changes reach `main` only through human-reviewed pull requests. Local
validation does not replace GitHub Actions CI. Management reviews CI and
decides whether work is accepted or merged.

## Consequences

Benefits:

- Implementation work remains traceable to approved Issues.
- The `main` branch is protected from direct Codex edits.
- Authority boundaries are clear.
- Changes are reviewable before merge.
- The backlog is not duplicated in Markdown.

Trade-offs:

- More explicit authorization steps are required.
- Codex must stop when scope or authority is unclear.
- Management must perform merges, Project updates, and branch cleanup.

## Rejected Alternatives

- Codex chooses its own tasks: rejected because task priority and scheduling
  belong in GitHub Issues and GitHub Projects.
- Codex works directly on `main`: rejected because changes must be isolated and
  reviewed before merge.
- One broad authorization covers all Git/GitHub actions: rejected because those
  actions have different effects and must be controlled independently.
- Codex may merge or update project management state: rejected because merge,
  acceptance, status, priority, scheduling, and assignment authority must remain
  with management.
- Backlog duplication in Markdown: rejected because it creates stale,
  conflicting sources of truth.
- Including the full product specification in this workflow ADR: rejected
  because product requirements belong in dedicated product and architecture
  documentation, not in an operating-decision record.

## References

- `AGENTS.md`
- `docs/development-workflow.md`
- `.github/pull_request_template.md`

These documents contain the detailed operating procedure derived from this
decision.

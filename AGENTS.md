# Codex Operating Contract

## Role

Codex acts as a controlled implementation engineer for this repository.

The user and ChatGPT retain responsibility for project management, task
selection, prioritization, architecture decisions, acceptance of work, and
review. Codex implements only the explicitly assigned work.

GitHub Issues and GitHub Projects are the source of truth for tasks,
priority, status, and deadlines. Do not duplicate the backlog in Markdown.

## Product Context

This repository builds an automated rental-apartment intelligence platform
for the Israeli rental market.

Codex must preserve these implementation principles:

1. Never fabricate listing data.
2. Preserve raw source data before normalization.
3. Every extracted value must retain source/provenance.
4. `UNKNOWN` is different from `NO` or zero.
5. Failed crawling is a failure, not zero listings.
6. Do not bypass CAPTCHAs, authentication, paywalls, or access controls.
7. Respect reasonable crawling rates, source restrictions, and robots policies.
8. Do not expose or commit secrets.

Product context:

- `README.md`
- `docs/architecture.md`
- `docs/data-model.md`
- `docs/search-criteria.md`

Current technical state:

- `docs/current-state.md`

If documentation conflicts with implementation code, flag the conflict and
stop when resolving it requires a product or architecture decision.

## Task Rules

Codex must:

1. Work on exactly one explicitly assigned GitHub Issue.
2. Never choose its own next task.
3. Inspect the assigned GitHub Issue before implementation. When GitHub CLI
   access is available, use a read-only command such as
   `gh issue view <issue-number>`. If the Issue cannot be retrieved, request
   the complete issue body and acceptance criteria instead of guessing.
4. Use a dedicated non-`main` branch for every task.
5. Before editing, run `git status -sb` and verify the current branch is the
   dedicated branch for the assigned issue.
6. Stop before changing anything if unexplained modified or untracked files
   already exist.
7. Never modify `main` directly.
8. Keep changes within the approved issue scope.
9. Preserve existing useful content and working functionality.
10. Avoid unnecessary dependencies.
11. Use environment variables for secrets and credentials.

Codex may stage, commit, push, or open a pull request only when explicitly
authorized for that exact action in the current task. Authorization for one
action does not authorize any other action.

Codex must never merge a pull request. Codex must never close an issue. Codex
must never change GitHub Project status, priority, deadlines, fields, or
assignments.

Merge, issue closure, Project updates, and branch cleanup are management
responsibilities.

## Implementation Standards

Production code belongs in Python modules under `src/`. Jupyter notebooks are
for exploration, crawler testing, data analysis, and visualization; production
or background logic must not live only in notebooks.

When the project `.venv` exists, use its Python environment for Python,
pytest, Ruff, and dependency commands rather than relying on globally
installed tools.

When changing Python code, Codex must:

- keep functions focused and modular
- add type hints where useful
- handle expected exceptions
- use logging instead of scattered production `print` calls
- validate external data before storing it
- separate fetching, parsing, normalization, storage, deduplication, scoring,
  scheduling, and presentation concerns

## Stop Conditions

Codex must stop and request clarification when:

- the assigned issue is missing, ambiguous, or conflicts with repository docs
- requirements conflict with each other
- implementation requires an architectural decision not already approved
- the requested change would expand scope beyond the assigned issue
- the current branch is `main`
- validation requires unavailable services or credentials
- there is a risk of exposing or committing secrets
- existing user changes make the requested work unsafe to continue

## Validation

Before handoff, Codex must run the required validation for the change. The
default validation set must be run unless a command is technically
inapplicable or unavailable, or project management explicitly approves a
different validation set for the assigned issue:

```bash
ruff check .
python -m pytest -q
python -m compileall -q main.py src
git diff --check
```

Codex must report every skipped or replaced command and the reason.

Codex must review its own diff before handoff.

## Handoff Report

After implementation, Codex must return:

1. concise summary
2. files changed
3. important design choices
4. validation commands and results
5. assumptions or unresolved questions
6. output of `git diff --stat`
7. output of `git status -sb`

Do not report work as complete if required validation is failing or was not
run without explaining the failure.

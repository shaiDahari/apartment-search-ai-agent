# Current State

## Implemented Technical Capabilities

- Python project structure with production modules under `src/`.
- Repository Python target: Python 3.12.
- Project Python environment: local `.venv`.
- When `.venv` exists, repository commands should use that environment.
- Jupyter notebook area for exploration under `notebooks/`.
- Canonical Phase 1 `ApartmentListing` domain model in `src/domain/listing.py`.
- Unit test coverage for the current listing model in `tests/test_listing.py`.
- Ruff configuration in `pyproject.toml`.
- GitHub Actions CI workflow in `.github/workflows/ci.yml`.

## Canonical ApartmentListing Domain Model

The current `ApartmentListing` model uses Pydantic and validates the Phase 1
canonical listing fields defined in `docs/data-model.md`.

Implemented behavior includes:

- required source identity fields
- required original listing URL and raw title
- required extraction timestamp
- optional Phase 1 listing attributes
- positive numeric validation for rent, rooms, and area
- uppercase three-letter currency validation
- rejection of unexpected fields
- validation on assignment
- whitespace stripping for string fields

## Tests And CI

- 9 unit tests are passing for the current domain model.
- Ruff linting is configured.
- GitHub Actions CI runs Ruff, pytest, and Python syntax validation on pushes
  and pull requests targeting `main`.

## Known Local Development Environment

- These details describe the user's current local machine and are not
  guaranteed or provisioned by the repository.
- MySQL 8.0.46.
- Host: `127.0.0.1`.
- Port: `3307`.
- MySQL Workbench connection name: `Apartment Search`.
- Database credentials must remain outside source control.

## Current Persistence Milestone

The current persistence milestone is preparing the repository for database
persistence work. MySQL is available locally, but application persistence code
is not yet implemented in this repository. The repository does not currently
provision, initialize, or verify the local MySQL server.

## Active Issue

- Current assigned work: Issue #11, Establish Codex contribution workflow.
- GitHub Issues and GitHub Projects are authoritative. Future Codex sessions
  must verify the current assignment from GitHub rather than treating this file
  as task authorization.

## Next Approved Checkpoint

After Issue #11 is completed and reviewed, persistence is the currently planned
next checkpoint. This is management context, not a Codex assignment. Codex must
wait for a separately approved GitHub Issue before starting that work. GitHub
Projects supersede this statement if planning changes.

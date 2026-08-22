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

- 10 unit tests are passing for the current listing model.
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
- Project schema: `apartment_search_ai_agent`.
- Application account: `'apartment_app'@'127.0.0.1'`.
- Application account privileges: `SELECT`, `INSERT`, `UPDATE`, and `DELETE`
  on `apartment_search_ai_agent.*`.
- MySQL Workbench application connection name: `Apartment Search App`.
- Application-user validation confirms `DATABASE()` returns
  `apartment_search_ai_agent` and `CURRENT_USER()` returns
  `apartment_app@127.0.0.1`.
- Local `.env` exists on the user's machine and is ignored by `.gitignore`.
- Database credentials must remain outside source control.

## Current Persistence Milestone

Phase 1 apartment-listing persistence design is documented in
`docs/persistence-design.md`.

Local MySQL schema and application-user setup instructions are documented in
`docs/database-setup.md`. MySQL is configured locally for the user's current
machine. SQLAlchemy database connection configuration is implemented in
`src/database/config.py`, but application persistence, database tables, and
ORM models are not yet implemented in this repository. The repository does
not currently provision, initialize, or verify the local MySQL server, schema,
user, privileges, or `.env` file.

## Planning Authority

GitHub Issues and GitHub Projects are authoritative for active work,
priorities, status, assignments, deadlines, and next checkpoints. This file
records durable repository state and known development context; it is not task
authorization.

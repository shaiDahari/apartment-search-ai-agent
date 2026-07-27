# Rental Agent Project Instructions

## Purpose
Build and maintain an automated rental-apartment intelligence platform for the Israeli rental market.

The system must:
- collect rental listings from multiple public sources
- normalize listing data
- preserve raw source data
- detect duplicates
- track listing changes over time
- analyze prices and total housing costs
- score apartments according to user requirements
- surface only relevant high-quality matches
- run automatically without requiring manual searches

## Working Environment
- OS: WSL Linux
- Editor: VS Code
- Python environment: `.venv`
- Python is the primary implementation language
- Jupyter notebooks are used for exploration, testing, data analysis, and visualization
- production/background logic must live in `.py` modules, not notebooks
- database target: MySQL

## Project Structure
- `notebooks/` — experiments, crawler testing, data exploration
- `src/` — production Python code
- `data/` — temporary/local data files
- `docs/` — project requirements, architecture and data specifications

## Core Engineering Rules
1. Never fabricate listing data.
2. Every extracted value must retain its source/provenance.
3. UNKNOWN is different from NO or zero.
4. Preserve raw values before normalization.
5. Separate fetching, parsing, normalization, storage, deduplication and scoring.
6. Prefer reusable modules over large scripts.
7. Do not place production logic only inside Jupyter notebooks.
8. Never hard-code passwords, API keys or database credentials.
9. Use environment variables for secrets.
10. Do not bypass CAPTCHAs, authentication, paywalls or access controls.
11. Respect reasonable crawling rates and source restrictions.
12. Failed crawling must be reported as a failure, not interpreted as zero listings.

## Codex Behavior
Before making significant architectural changes:
- inspect the existing repository
- read relevant files in `docs/`
- preserve existing working functionality
- explain significant assumptions
- avoid unnecessary dependencies

When adding or changing Python code:
- keep functions focused and modular
- add type hints where useful
- handle expected exceptions
- use logging instead of scattered print statements in production code
- validate external data before storing it

## Source of Truth
Detailed business requirements must live in:

`docs/search-criteria.md`

System architecture must live in:

`docs/architecture.md`

Canonical listing fields and database/data-model rules must live in:

`docs/data-model.md`

If these documents conflict with implementation code, flag the conflict instead of silently guessing.
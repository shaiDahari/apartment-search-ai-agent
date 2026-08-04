# Apartment Search AI Agent

An autonomous apartment-search platform under development, designed to collect, structure, analyze, rank, and continuously monitor apartment listings from multiple sources.

The project combines software engineering, data engineering, web data acquisition, analytics, automation, and DevOps practices into a single end-to-end system.

> **Status:** Foundation and architecture phase.
> The repository targets Python 3.12. The canonical Phase 1 `ApartmentListing` model is implemented in `src/domain/listing.py`, 10 unit tests currently pass, and Ruff plus GitHub Actions CI are configured.
> Database persistence, crawlers, scoring, UI, containers, and deployment are not yet implemented.

---

## Why This Project

Apartment listings are fragmented across multiple platforms and often contain incomplete, inconsistent, duplicated, or difficult-to-compare information.

The goal of this project is to build a system that performs the repetitive search and analysis work automatically.

Instead of returning a large list of links, the platform is intended to:

- collect listings from multiple sources
- preserve original source data
- normalize inconsistent listing information
- identify duplicate properties
- track changes over time
- calculate relevant costs
- evaluate apartments against configurable criteria
- rank the strongest matches
- identify missing or conflicting information
- continuously monitor the market for new opportunities

---

## Target Architecture

```text
Public Listing Sources
        |
        v
   Source Crawlers
        |
        v
 Raw Listing Data
        |
        v
 Parsing & Normalization
        |
        v
 Validation & Enrichment
        |
        v
   Deduplication
        |
        v
      Database
        |
        v
 Analysis & Scoring
        |
        +-------------------+
        |                   |
        v                   v
   Web Dashboard          Alerts
```

The system is designed so that data acquisition, processing, storage, analysis, scheduling, and presentation remain separate components.

---

## Configured Technology Stack

These dependencies and tools are configured for the project or its development environment. They do not all represent implemented application capabilities yet.

### Core

- Python
- Pandas
- Requests
- BeautifulSoup
- lxml

### Data & Persistence Dependencies

- SQLAlchemy
- PyMySQL

These packages are available for future persistence work, but repository database persistence is not implemented yet.

### Automation

- APScheduler
- python-dotenv

### Development & Analysis

- Jupyter
- IPython kernel
- pytest
- Ruff
- VS Code
- WSL

### Version Control

- Git
- GitHub
- GitHub CLI
- GitHub Actions CI

---

## Planned Engineering Stack

The following technologies and capabilities are part of the intended architecture but are **not yet implemented**:

- MySQL database integration and provisioning
- Streamlit
- Docker
- Docker Compose
- deployment automation
- structured application logging
- health checks
- production scheduling
- public web deployment

They will be introduced incrementally as the corresponding components are implemented.

---

## Repository Structure

```text
.
├── AGENTS.md
├── README.md
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── main.py
│
├── .github/
│   ├── pull_request_template.md
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── architecture.md
│   ├── current-state.md
│   ├── data-model.md
│   ├── development-workflow.md
│   ├── persistence-design.md
│   ├── decisions/
│   │   └── ADR-0001-codex-contribution-workflow.md
│   └── search-criteria.md
│
├── notebooks/
│   └── 00_environment_check.ipynb
│
├── src/
│   ├── analysis/
│   ├── crawlers/
│   ├── database/
│   ├── deduplication/
│   ├── domain/
│   ├── processing/
│   └── scheduler/
└── tests/
    └── test_listing.py
```

### Directory Responsibilities

`src/crawlers/`
Source-specific listing acquisition and parsing.

`src/processing/`
Normalization, validation, cleaning, and transformation.

`src/deduplication/`
Cross-source duplicate detection and canonical property resolution.

`src/database/`
Database models, connections, persistence, and query logic.

`src/analysis/`
Apartment scoring, pricing analysis, comparison, and opportunity detection.

`src/scheduler/`
Automated execution and recurring data collection.

`notebooks/`
Exploratory development, crawler experiments, data inspection, analysis, and visualization.

`docs/`
Detailed system specifications that do not belong in the main README.

`.github/`
GitHub Actions workflow and pull request template.

`tests/`
Automated tests for implemented Python modules.

---

## Data Engineering Principles

The platform is being designed around the following rules:

- preserve raw source data before normalization
- retain provenance for extracted information
- treat `UNKNOWN` differently from `NO` or `0`
- preserve conflicting values instead of silently overwriting them
- separate fetching, parsing, normalization, storage, and analysis
- distinguish crawler failure from zero search results
- avoid hard-coded credentials and secrets
- keep source-specific logic isolated
- make processing reproducible
- maintain listing and price history
- avoid presenting inferred values as confirmed facts

Detailed rules are defined in [`docs/data-model.md`](docs/data-model.md).

---

## Current Implemented Model

`ApartmentListing` is the current canonical Phase 1 domain model. It is implemented in `src/domain/listing.py`, its rules are documented in [`docs/data-model.md`](docs/data-model.md), and its current behavior is covered by 10 unit tests in `tests/test_listing.py`.

The Phase 1 apartment-listing persistence design is documented in [`docs/persistence-design.md`](docs/persistence-design.md).

---

## Development Workflow

Production code belongs in Python modules under `src/`.

Jupyter notebooks are used for:

- experimenting with data sources
- inspecting HTML and structured responses
- validating parsers
- examining DataFrames
- testing normalization logic
- exploratory data analysis
- developing scoring models
- visualization

Working logic that becomes part of the platform will be moved from notebooks into reusable Python modules.

Development work is linked to an approved GitHub Issue, implemented on a dedicated non-`main` branch, and merged to `main` through reviewed pull requests. Detailed agent instructions are in [`AGENTS.md`](AGENTS.md), and the contribution procedure is in [`docs/development-workflow.md`](docs/development-workflow.md).

---

## Getting Started

Python 3.12 is required.

### 1. Clone the repository

```bash
git clone https://github.com/shaiDahari/apartment-search-ai-agent.git
cd apartment-search-ai-agent
```

### 2. Create an isolated Python environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Runtime dependencies only:

```bash
python -m pip install -r requirements.txt
```

Development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` includes `requirements.txt`, so development setup only needs the development install command.

### 4. Optional: register the Jupyter environment

```bash
python -m ipykernel install \
  --user \
  --name apartment-search-ai-agent \
  --display-name "Python (apartment-search-ai-agent)"
```

### 5. Local validation

Run these commands from the activated project `.venv`:

```bash
ruff check .
python -m pytest -q
python -m compileall -q main.py src
git diff --check
```

Local validation does not replace GitHub Actions CI.

Tests and validation commands are executable. No complete end-to-end apartment-search service or pipeline exists yet. Runtime instructions will be added when an executable application pipeline is implemented.

---

## Documentation

Project specifications are maintained separately from the README:

- [`docs/search-criteria.md`](docs/search-criteria.md) — apartment-search requirements and filtering criteria
- [`docs/data-model.md`](docs/data-model.md) — canonical listing structure and data-quality rules
- [`docs/persistence-design.md`](docs/persistence-design.md) — Phase 1 apartment-listing persistence design
- [`docs/architecture.md`](docs/architecture.md) — system and DevOps architecture
- [`docs/current-state.md`](docs/current-state.md) — current repository capabilities and known development context
- [`docs/development-workflow.md`](docs/development-workflow.md) — Codex contribution workflow
- [`docs/decisions/`](docs/decisions/) — architecture decision records
- [`AGENTS.md`](AGENTS.md) — repository-level instructions for coding agents

---

## Roadmap

### Phase 1 — Foundation

- [x] isolated Python environment
- [x] repository structure
- [x] Jupyter development environment
- [x] project documentation
- [x] Git repository
- [x] public GitHub repository
- [x] core data-processing dependencies
- [x] canonical Python data model
- [x] automated unit tests
- [x] Ruff linting
- [x] GitHub Actions CI

### Phase 2 — Data Pipeline

- [ ] first listing-source crawler
- [ ] raw data persistence
- [ ] normalization pipeline
- [ ] validation layer

### Phase 3 — Storage & Intelligence

- [ ] MySQL integration
- [ ] listing history
- [ ] price history
- [ ] duplicate detection
- [ ] apartment scoring
- [ ] comparable-property analysis

### Phase 4 — Automation

- [ ] recurring crawler execution
- [ ] change detection
- [ ] opportunity detection
- [ ] alert generation
- [ ] structured logging

### Phase 5 — Web Application

- [ ] Streamlit dashboard
- [ ] interactive filtering
- [ ] ranked results
- [ ] listing detail views
- [ ] downloadable datasets
- [ ] public deployment

### Phase 6 — DevOps

- [x] automated tests
- [x] GitHub Actions CI
- [ ] Dockerfile
- [ ] Docker Compose
- [ ] containerized database and services
- [ ] security/dependency checks
- [ ] CI/CD deployment workflow
- [ ] health checks

### Phase 7 — AI Agent Layer

- [ ] agent decision workflow
- [ ] structured tool usage
- [ ] search-result reasoning
- [ ] missing-information investigation
- [ ] natural-language result summaries
- [ ] user-feedback-driven ranking refinement

---

## Security and Responsible Data Collection

The project is intended to work only with legitimately accessible data sources.

The implementation will not be designed to bypass:

- authentication controls
- CAPTCHA challenges
- paywalls
- security mechanisms
- explicit access restrictions

Future crawlers must respect reasonable request rates, source restrictions, and robots policies.

Credentials and secrets must remain outside source control.

---

## Maintainer

**Shai Dahari**

This repository is being developed as a practical application and an engineering portfolio project demonstrating Python, data engineering, automation, software architecture, and DevOps practices.

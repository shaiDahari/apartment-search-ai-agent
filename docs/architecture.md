# System Architecture

## Objective
Run an automated rental-search platform continuously, without requiring manual searches.

## High-Level Flow

Sources
→ Crawlers
→ Raw Data
→ Normalization
→ Deduplication
→ Database
→ Scoring
→ Alerts / Dashboard

## Main Components

### 1. Crawlers
Location:
`src/crawlers/`

Responsibilities:
- collect listings
- preserve source URL
- preserve raw data
- handle source-specific parsing
- report failures

### 2. Data Processing
Location:
`src/processing/`

Responsibilities:
- normalize values
- validate fields
- clean text
- standardize prices, rooms, size, floors and addresses

### 3. Deduplication
Location:
`src/deduplication/`

Responsibilities:
- detect the same apartment across multiple sources
- create one canonical property record
- preserve all source listings

Canonical-property records and cross-source duplicate persistence are future
architecture goals. They are not part of Phase 1 apartment-listing
persistence.

### 4. Database
Target:
MySQL

Phase 1 responsibility:
- store the latest known state of each external listing in the single
  `apartment_listings` entity documented in
  [`docs/persistence-design.md`](persistence-design.md)
- enforce `listing_id` as internal persistence identity
- enforce `(source, source_listing_id)` as the unique external listing
  identity

Future responsibilities:
- listings
- canonical properties
- price history
- change history
- crawl history
- source status

Phase 1 does not implement database tables, ORM models, persistence code, or
history storage.

### 5. Analysis & Scoring
Location:
`src/analysis/`

Responsibilities:
- match scoring
- price analysis
- total monthly cost
- comparables
- opportunity detection

### 6. Scheduler
Responsibilities:
- run crawlers automatically
- trigger processing
- update the database
- detect changes
- generate alerts

### 7. Jupyter Notebooks
Location:
`notebooks/`

Use for:
- crawler development
- inspecting DataFrames
- testing parsing
- data exploration
- visualization
- scoring experiments

Notebooks are not the production runtime.

### 8. User Interface
Planned:
- web dashboard
- ranked apartment results
- filters
- listing history
- alerts

## Runtime

Development:
WSL + VS Code + Python `.venv`

Production target:
Always-on service, later deployable to a VPS/cloud server.

## DevOps & CI/CD

This project is also designed as a production-style DevOps portfolio project.

Planned practices and technologies:

- Git feature-branch workflow
- GitHub repository
- GitHub Actions CI/CD
- automated linting and testing
- dependency/security checks
- Docker containerization
- Docker Compose for local multi-service development
- environment-based configuration
- secrets management
- automated build pipeline
- deployment pipeline
- application logging
- health checks
- deployment of the public Streamlit application

Jenkins is intentionally not required; GitHub Actions will be the primary CI/CD platform.

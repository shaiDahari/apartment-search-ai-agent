# Local Database Setup

## Purpose

Document the local MySQL schema, application user setup, and Python database
connection configuration for this project. This setup supports future
persistence work without adding ORM models, schema files, migrations, or
table-creation behavior.

## Approved Local Settings

- Schema name: `apartment_search_ai_agent`
- Application user: `apartment_app`
- Host: `127.0.0.1`
- Port: `3307`
- Application-user account: `'apartment_app'@'127.0.0.1'`

The application user must not be `root` and must have access only to the
project schema.

## Environment Files

Real credentials belong only in local `.env`, which is ignored by Git and must
never be staged or committed.

The owner enters the real `MYSQL_PASSWORD` manually in `.env`:

```dotenv
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_DATABASE=apartment_search_ai_agent
MYSQL_USER=apartment_app
MYSQL_PASSWORD=<real-local-password>
```

Committed `.env.example` contains the same variable names with safe
placeholder values only.

## Python Application Configuration

The Python application reads these environment variables and uses SQLAlchemy
with the `mysql+pymysql` driver to build the database connection URL:

- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

Database configuration code lives in `src/database/config.py`.

Use the explicit factory functions to create reusable SQLAlchemy objects:

```python
from src.database.config import create_database_engine, create_session_factory

engine = create_database_engine()
SessionLocal = create_session_factory(engine=engine)
```

The factories load local `.env` values for development, validate required
configuration, and fail clearly when values are missing or invalid. Engine
creation is lazy and does not create database tables by itself.

Do not hard-code credentials in Python code. Do not print, log, or commit the
real `MYSQL_PASSWORD`.

## Pre-Change Inspection

Run these checks with a MySQL admin account before creating the schema or
changing any user or grants.

Inspect the schema:

```sql
SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME = 'apartment_search_ai_agent';
```

Inspect existing application-user accounts:

```sql
SELECT User, Host
FROM mysql.user
WHERE User = 'apartment_app';
```

If the schema already exists, report its current charset and collation and
stop for owner approval before changing it.

If any `apartment_app` account already exists, report the exact `User` and
`Host` account(s), including grants for each account, and stop for owner
approval before `ALTER USER`, `REVOKE`, or `GRANT` changes.

Do not assume that adding the approved `GRANT` removes existing privileges.

## Setup SQL

Create the project schema only after clean inspection or owner approval:

```sql
CREATE DATABASE apartment_search_ai_agent
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Create the intended application account only after clean inspection or owner
approval:

```sql
CREATE USER 'apartment_app'@'127.0.0.1'
  IDENTIFIED BY '<owner-entered-password>';
```

Grant least-privilege runtime access only:

```sql
GRANT SELECT, INSERT, UPDATE, DELETE
  ON apartment_search_ai_agent.*
  TO 'apartment_app'@'127.0.0.1';
```

Do not run `FLUSH PRIVILEGES`; `CREATE USER`, `ALTER USER`, and `GRANT` apply
directly.

Additional DDL privileges such as `CREATE`, `ALTER`, or `INDEX` must only be
added later if a separately approved schema or migration task requires them.

## Existing Account Handling

If `'apartment_app'@'127.0.0.1'` already exists, do not silently keep an
unknown password or privilege state.

Report the current account and grants:

```sql
SHOW GRANTS FOR 'apartment_app'@'127.0.0.1';
```

If the owner approves password rotation, use:

```sql
ALTER USER 'apartment_app'@'127.0.0.1'
  IDENTIFIED BY '<owner-entered-password>';
```

If any other `apartment_app` host account exists, report it separately and
wait for owner approval before changing it.

## Application-User Validation

Validate authentication with MySQL tooling:

```bash
mysql \
  --host=127.0.0.1 \
  --port=3307 \
  --user=apartment_app \
  --password \
  apartment_search_ai_agent
```

Inside the application-user session:

```sql
SELECT USER(), CURRENT_USER(), DATABASE();

SHOW GRANTS FOR 'apartment_app'@'127.0.0.1';

SHOW DATABASES;
```

Confirm that:

- authentication succeeds as `apartment_app`
- `DATABASE()` is `apartment_search_ai_agent`
- grants are limited to `SELECT`, `INSERT`, `UPDATE`, and `DELETE` on
  `apartment_search_ai_agent.*`
- `SHOW GRANTS` contains no privileges on unrelated application schemas
- system schemas such as `information_schema` may still be visible and do not
  indicate broader application-data privileges

Do not use a create/insert/drop-table validation test for Issue #5, because
the application user intentionally does not have DDL privileges.

## MySQL Workbench Validation

Preserve the existing admin/root Workbench connection.

Create a separate Workbench connection for the application user:

- Connection name: `Apartment Search App`
- Hostname: `127.0.0.1`
- Port: `3307`
- Username: `apartment_app`
- Default schema: `apartment_search_ai_agent`

Use the owner-entered password for this local connection. Do not store that
password in Git.

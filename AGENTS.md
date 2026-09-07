# Contributing to Open Food Facts Events

## Development setup

- Use Python 3.10 or newer.
- Install Poetry, then run `poetry install`.
- Set `ADMIN_USERNAME` and `ADMIN_PASSWORD` before importing the application.
- Run `make unit` for the unit tests.
- Run `make checks` for formatting, linting, and type checks.

The Docker Compose development environment is started with `make dev`. It
requires Docker and a local `.env` file with the database and authentication
settings. Never commit `.env` or credentials.

## Change expectations

Keep API behavior backwards compatible unless a change is explicitly
documented. Update the Poetry lockfile whenever dependencies change, and add
or update tests for behavior changes.

GitHub Actions should use maintained, versioned action references and the
smallest permissions required. Do not add tokens, passwords, or private keys
to source files, workflow logs, or examples.

# ADR 0001: Use Ruff for Python Linting and Formatting

## Status
Accepted

## Context
In a team environment, consistent code formatting and automated lint checks are essential to prevent styling debates during code reviews and catch common syntax/semantic errors before code is pushed.

Traditionally, Python projects combine multiple standalone tools:
- `flake8` for linting
- `black` for formatting
- `isort` for import sorting

Running three separate Python tools inside pre-commit hooks causes slow commit times (often several seconds per commit), which tempts developers to skip hooks using `--no-verify`.

## Decision
We choose **Ruff** as the unified Python linter and formatter for AgriVision.

## Consequences
### Positive:
- **Speed:** Written in Rust, Ruff runs in milliseconds (10-100x faster than traditional Python tools), providing near-instant pre-commit feedback.
- **Simplicity:** Replaces Flake8, Black, and isort with a single tool and consistent ruleset.
- **Standardized:** Widely adopted in modern Python ecosystems (FastAPI, Airflow, Pydantic).

### Negative / Trade-offs:
- Relatively newer than Flake8/Black, though mature enough for top-tier production environments.

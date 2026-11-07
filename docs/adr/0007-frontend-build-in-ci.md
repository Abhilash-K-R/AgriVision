# ADR 0007: Validate the Frontend in CI

## Status
Accepted

## Context
The frontend is independently built with TypeScript and Vite, but the CI
workflow only checked the Python backend. A broken frontend could therefore
be merged despite a green workflow.

## Decision
Add a frontend CI job that installs the lockfile-pinned npm dependencies and
runs `npm run build`. The production build includes the TypeScript compiler
check before bundling.

## Alternatives Considered

| Option | Trade-off |
|---|---|
| Keep backend-only CI | Faster, but leaves frontend build and type errors undetected. |
| Add a separate frontend test/lint toolchain now | Broader coverage, but adds dependencies and maintenance before tests or an ESLint config exist. |
| Build frontend in CI | Verifies types and production bundling with existing project tooling and no new test dependencies. |

## Consequences
- Frontend type errors and bundling failures block the CI job.
- Dedicated component tests and ESLint configuration remain future work.

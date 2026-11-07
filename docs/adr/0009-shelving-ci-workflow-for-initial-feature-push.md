# ADR 0009: Temporarily Shelve GitHub CI Workflow for Initial Remote Feature Push

## Status
Accepted

## Context
During the push of the AgriVision v1 feature branch (`feat/agrivision-v1`) to GitHub (`origin`), GitHub's server-side authorization check rejected the push because `.github/workflows/ci.yml` was included in the commit history, and the user's active Git Personal Access Token lacks the `workflow` OAuth scope.

While updating the token permissions or configuring SSH keys is the long-term solution (documented in ADR 0008), the team decided to prioritize unblocking the remote publishing of the core application codebase (FastAPI backend, React frontend, ML models, and documentation) immediately.

## Decision
1. Safely backup `.github/workflows/ci.yml` into `docs/ci-workflow.yml.backup` to preserve the CI pipeline configuration.
2. Add `.github/` to `.gitignore` so workflow files are shelved locally and not tracked in Git.
3. Publish `feat/agrivision-v1` containing all application code, models, tests, and documentation without workflow files in its commit tree.
4. Reinstate the GitHub Actions workflow in Phase 6 remote hardening once token permissions or SSH credentials are updated.

## Alternatives Considered

| Option | Trade-off |
|---|---|
| **Wait for token scope update** | Blocks all remote publishing and feature branch review until GitHub account settings are adjusted. |
| **Shelve CI workflow and gitignore `.github/` (Accepted)** | Unblocks immediate remote pushing and collaboration on the feature branch. Relies on passing local quality gates (Ruff, pytest, Vite build) in the interim. |

## Consequences
- The remote repository receives the complete working application codebase immediately.
- GitHub Actions will not run automated checks remotely until the workflow is re-introduced with an authorized token in Phase 6 hardening.
- Local pre-push quality gates (Ruff lint, pytest tests, Vite TypeScript production build) must be run locally prior to merging.


# ADR 0008: Resolving GitHub Workflow Permission for CI Push

## Status
Accepted

## Context
When pushing the feature branch containing the AgriVision v1 codebase (`feat/agrivision-v1`) to the remote GitHub repository (`origin`), GitHub's server-side authorization hook rejected the push with an error indicating missing `workflow` scope:
`refusing to allow an OAuth App / Personal Access Token to create or update workflow .github/workflows/ci.yml without workflow scope`

GitHub Actions workflow files (`.github/workflows/*.yml`) have direct access to repository runners, secrets, and deployment pipelines. To protect repositories from supply chain tampering, GitHub strictly requires personal access tokens (PATs) pushing workflow changes to have the explicit `workflow` scope.

## Decision
We retain `.github/workflows/ci.yml` as a non-negotiable component of our Phase 6 (Quality & CI) Definition of Done. We do not remove, rename, or omit the workflow file to bypass authorization checks. Instead, we resolve the issue at the authentication and credential level by updating the GitHub credential with the required `workflow` scope (or switching to SSH authentication).

## Alternatives Considered

| Option | Trade-off |
|---|---|
| **Remove / delete `.github/workflows/ci.yml`** | **Rejected.** While it bypasses the token check, it eliminates automated testing, violates the Definition of Done for Phase 6, and degrades software quality. In industry, bypassing security controls to force a push is a severe antipattern. |
| **Update PAT with `workflow` scope (Recommended for HTTPS)** | **Accepted.** Generates/updates a GitHub Personal Access Token with `repo` and `workflow` scopes and refreshes the local Git credential store. Preserves HTTPS remotes and respects GitHub's security boundary. |
| **Switch remote to SSH (`git@github.com:...`)** | **Viable alternative.** SSH keys attached to a GitHub account have full repository privileges by default without per-scope expiration. Requires generating an SSH keypair (`ssh-keygen`) and adding the public key to GitHub. |

## Consequences
- Continuous Integration remains intact, enforcing automated linting (Ruff), type checking (mypy), tests (pytest), and frontend bundling on GitHub.
- Local Git credentials must be refreshed with authorized permissions before pushing.
- No repository security standards or definitions of done are compromised.

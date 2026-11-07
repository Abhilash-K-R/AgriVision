# Progress

- **Phase 0 (Foundation)**:
    - Feature branch `feat/phase-0-foundation` created.
    - `.gitignore` configured.
    - `.env.example` contract defined.
    - Directory scaffolding created.
    - Pre-commit hook configuration using Ruff.
    - Developer onboarding guide in `README.md`.
    - ADR 0001 created.
- **Phase 1 (Requirements and Design)**:
    - PRD finalized (`docs/PRD.md`).
    - Disease classes chosen: Early Blight, Late Blight, Healthy (`docs/adr/0002-tomato-disease-classes.md`).
    - Model architecture chosen: MobileNetV2 with transfer learning (`docs/adr/0003-model-architecture.md`).
    - Backend framework chosen: FastAPI with async support (`docs/adr/0004-api-design.md`).
    - Frontend framework chosen: React (Vite) PWA (`docs/adr/0005-frontend-technology.md`).
    - ADRs and PRD verified and committed.
- **Phase 2 (Data Engineering)**:
    - Data preparation script created and verified (`ml/data_prep.py`).
    - Fixed random seed and leak-free splitting implemented.
    - Verified against project requirements (Phase 2 DoD met).
- **Phase 3 (Model Development)**:
    - MobileNetV2 transfer learning model trained.
    - Exported to ONNX format.
    - Model card documented.
    - Metrics (confusion matrix, precision/recall) verified.
- **Phase 4 (Backend)**:
    - FastAPI framework, configuration, and logging setup.
    - Inference engine integrated with ONNX Runtime.
    - API endpoints (`/predict`, `/health`, `/feedback`, `/history`) implemented.
    - DB models (SQLAlchemy/Neon) and session management.
    - Unit tests created.
    - DoD met: tests pass, input validation active, no hardcoded config.
- **Phase 5 (Frontend)**:
    - Created React Vite project in `frontend/` with Tailwind CSS.
    - Implemented mobile-first camera capture / file upload flow, result card, history view, about page.
    - API client with error handling, TypeScript types matching backend schemas.
    - PWA manifest and meta tags for offline basic use.
    - Real-phone usability testing has not been recorded; the DoD is not verified.
- **Phase 6 (Quality & CI)**:
    - Created `.github/workflows/ci.yml` with GitHub Actions pipeline running backend linting (Ruff), type checks (mypy), tests (pytest), and frontend build/type checks.
    - Updated `backend/pyproject.toml` with project dependencies, dev dependencies, and tool configurations.
    - Added backend smoke tests for health and missing-upload validation.
    - Created `backend/Dockerfile` for backend containerization, including the ONNX model artifacts.
    - Created `docker-compose.yml` for local development (backend, frontend, db).
    - Added rate limiting (slowapi) to `/predict` endpoint.
    - Current validation: backend Ruff, Python syntax compilation, backend tests (3 passed), mypy (8 source files), and frontend production build/type-check pass locally.
    - Frontend lint is not configured for ESLint 9. GitHub Actions has not run, so the Phase 6 DoD is not yet verified.
    - Docker Compose could not be validated locally because Docker is unavailable.
- Phase 6 Quality & CI remains in progress pending frontend lint policy and a green GitHub Actions run.

- **Phase 8 (Observability and real-world check)**:
    - Added structured logging middleware with request ID support in `backend/app/core/logging.py`.
    - Created `docs/runbook.md` with troubleshooting guide, common errors, log inspection instructions, and restart procedures.
    - Added prediction logging: request ID, confidence, disease class, and rejection status are logged for every prediction.
    - Every request gets a request ID that appears in its logs via `RequestIdMiddleware`.
    - Real-world farm-photo accuracy and production metrics have not been collected; the DoD is not met.

- **Phase 9 (Release)**:
    - Finalized `README.md` with installation instructions, quickstart, and contribution guidelines.
    - Updated `CHANGELOG.md` with entries for all phases (Foundation through Release) following Keep a Changelog format.
    - Created v1.0.0 release notes summarizing all completed work.
    - A release draft exists, but no tag, deployment, or live-link verification has been completed; the DoD is not met.

- Phase 8 observability code is present; its real-world validation remains open.
- Phase 9 release readiness remains open.

- **Overall Project Status**: feature branch `feat/agrivision-v1` has a local application commit. Production readiness and release are not verified.

## Current Git housekeeping
- Current branch: `feat/agrivision-v1`; tracking `origin/feat/agrivision-v1`.
- CI workflow shelved per user instruction and recorded in ADR 0009 (`docs/adr/0009-shelving-ci-workflow-for-initial-feature-push.md`):
  - `.github/workflows/ci.yml` safely backed up to `docs/ci-workflow.yml.backup`.
  - `.github/` added to `.gitignore`.
- Branch `feat/agrivision-v1` successfully published to GitHub: `origin/feat/agrivision-v1` (`9e5405d`).
- Upstream configured: `git push` and `git pull` now track `origin/feat/agrivision-v1` by default.
- All application code (FastAPI backend, React frontend, ONNX model weights, documentation) is live on GitHub.

## Frontend dependency-upgrade update (2026-11-07)
- Work is on feature branch `fix/typescript-package-upgrade-20261107195947`; no push or deployment was performed.
- TypeScript moved from 5.6.2 through 5.9.3 and 6.0.3 to 7.0.2. React 18 moved to 19, Vite 5 to 8, and compatible patch/minor updates were applied to the other scanned groups. Tailwind remains on 3.4.19 to preserve the existing browser floor after Tailwind 4's required migration failed.
- The post-upgrade TypeScript compile, local production build, and three route tests pass. Runtime comparison is inconclusive because its clean `npm ci` fails on a package-lock `picomatch` mismatch. The existing lint script also has no ESLint flat config and was already unconfigured before this upgrade.

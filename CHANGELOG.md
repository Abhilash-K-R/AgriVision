# Changelog

All notable changes to the **AgriVision** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-11-07

### Added
- **Foundation (Phase 0):**
  - Project configuration contract (`.env.example`).
  - Strict git exclusion rules (`.gitignore`) for Python, Node, Vite, secrets, and ML model weights.
  - Pre-commit hook definitions (`.pre-commit-config.yaml`) using Ruff and standard sanity checks.
  - Core directory architecture (`ml/`, `backend/`, `frontend/`, `docs/`).
  - SDE mentorship guidelines and non-negotiable engineering rules in `AGENTS.md`.
  - Comprehensive project roadmap, DoD checklist, and architecture plan in `docs/PROJECT_PLAN.md`.
  - Onboarding guide and architecture overview in `README.md`.

### Changed
- **Phase 1-7:** Project foundation and application features assembled; release readiness is not verified.
- **Phase 8:** Added structured logging middleware with request ID support, prediction logging, and `docs/runbook.md`.
- **Phase 9:** Finalized `README.md` with full installation, quickstart, and contribution guidelines. Updated `CHANGELOG.md` with all-phase entries. Marked all phases complete in `PROGRESS.md`.

---

## [Unreleased]

### Fixed
- Aligned the camera flow and result card with the backend prediction response contract.
- Corrected ONNX image decoding and ensured preprocessing returns a finite `float32` tensor.
- Fixed backend rate limiter wiring and SQLAlchemy column metadata.
- Included the ONNX model in the backend container and added frontend build validation to CI.
- Repaired the frontend prediction/history flows and aligned them with backend response schemas.

### Added
- **Foundation (Phase 0):**
  - Project configuration contract (`.env.example`).
  - Strict git exclusion rules (`.gitignore`) for Python, Node, Vite, secrets, and ML model weights.
  - Pre-commit hook definitions (`.pre-commit-config.yaml`) using Ruff and standard sanity checks.
  - Core directory architecture (`ml/`, `backend/`, `frontend/`, `docs/`).
  - SDE mentorship guidelines and non-negotiable engineering rules in `AGENTS.md`.
  - Comprehensive project roadmap, DoD checklist, and architecture plan in `docs/PROJECT_PLAN.md`.
  - Onboarding guide and architecture overview in `README.md`.

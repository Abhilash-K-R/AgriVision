# AgriVision: Project Plan

## Product
A web app where a farmer photographs a tomato leaf and gets the likely
disease, a confidence score, and simple care advice. Quality bar:
speed, mobile-first design, and clear results (inspired by apps like Plantix).

## v1 scope (IN)
Image upload or phone camera, prediction with confidence, rejection of
non-tomato or low-confidence images, care tips per disease, a "was this
correct?" feedback button, and prediction history.

## Non-goals for v1
Other crops, user accounts, payments, native mobile app.

## Success metrics
- Test accuracy and per-class precision/recall (reported honestly)
- API response time under about 2 seconds
- Live link works from another device and network
- Accuracy measured on REAL phone photos, not only the dataset

## Key risk (teach this early)
Public datasets like PlantVillage have clean lab backgrounds. Models score
high there but drop on real farm photos (the "domain gap"). Mitigations:
a confidence threshold, an out-of-scope rejection path, a feedback loop,
and a model card that states limitations openly.

## Architecture
React (Vite) -> FastAPI -> ONNX model runtime; Neon PostgreSQL stores
predictions and feedback. CI: GitHub Actions. Deploy: Vercel + Render.

## Phases and Definitions of Done (DoD)
Phase 0 Foundation: repo structure, AGENTS.md, README skeleton, .gitignore,
  .env.example, pre-commit hooks, branch and commit rules.
  DoD: a stranger can clone the repo and understand the plan in 5 minutes.
Phase 1 Requirements and design: PRD finalized, class list chosen (state how
  many classes and why), architecture diagram, first ADRs.
  DoD: every major choice has a written reason. **Verified:** docs/PRD.md and
  docs/adr/0002-0005 created with context, decisions, and trade-offs.
Phase 2 Data: download, explore, check class balance, split train/val/test
  BEFORE augmentation (avoid data leakage), fixed seed, data README.
  DoD: the split is reproducible from one command.
Phase 3 Model: baseline, then transfer learning (MobileNetV2), metrics file,
  confusion matrix, per-class precision/recall, export to ONNX, model card.
  DoD: results reproducible from one command; limitations documented.
Phase 3 Model: baseline, then transfer learning (MobileNetV2), metrics file,
  confusion matrix, per-class precision/recall, export to ONNX, model card.
  DoD: results reproducible from one command; limitations documented.
Phase 4 Backend: FastAPI /predict, /health, /feedback, /history; input
  validation (type, size), error handling, structured logs, config via env,
  tests.  DoD: tests pass; bad input returns clean errors, never crashes.
Phase 5 Frontend: upload and camera flow, loading and error states, result
  card, history page, tested on a real phone.
  DoD: a non-technical person can use it without help.
Phase 6 Quality: unit and integration tests, lint, type checks, CI pipeline
  that blocks bad merges.  DoD: CI is green on every pull request.
Phase 7 Production: Dockerfile, deployment, secrets, CORS, rate limiting,
  health checks, docs/runbook.md (what to do when it breaks).
  DoD: the live link works from a different device and network.
Phase 8 Observability and real-world check: request-ID logs, error tracking,
  feedback summary, test with real farm-style photos and record the true
  accuracy.  DoD: can answer "how is it doing in the real world?" with numbers.
Phase 9 Release: v1.0.0 tag, CHANGELOG, final README with screenshots and
  demo GIF, short retrospective.

## Repo structure
agrivision/
  AGENTS.md, README.md, CHANGELOG.md
  .agent/rules/, .agent/workflows/
  docs/ (PROJECT_PLAN.md, PROGRESS.md, LEARNING_LOG.md, architecture.md,
         runbook.md, model-card.md, adr/)
  ml/ (data prep, training, evaluation)
  backend/ (app/api, app/core, app/services, app/schemas, app/db, tests/)
  frontend/
  .github/workflows/ci.yml

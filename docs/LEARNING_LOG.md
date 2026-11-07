# AgriVision: Intern Learning Log

A living record of engineering concepts, definitions, architectural trade-offs, and interview-ready answers acquired during the project.

---

## Phase 0: Foundation & Engineering Rigor

### Concept 1: Pre-commit Hooks
- **Definition:** Client-side scripts that run automatically before a `git commit` is finalized to enforce quality checks, secret detection, and code styling.
- **Why it matters in industry:** Catches syntax errors, leaked secrets, and unformatted files locally before they ever pollute the git history or CI pipelines. Saves CI compute costs and avoids embarrassing review comments.
- **Sample Interview Answer:**
  > *"On our team, we configured pre-commit hooks using Ruff and standard sanity checks. This guaranteed that every commit met our formatting standards and prevented accidental leaks of private credentials before code could even leave an engineer's workstation."*

### Concept 2: The Environment Contract (`.env.example`)
- **Definition:** A git-tracked template file that specifies all configuration variables required by an application, populated with descriptive dummy values.
- **Why it matters in industry:** Production systems require configuration (database URLs, ports, CORS origins, model paths), but committing actual secrets (`.env`) leads to security breaches. An environment contract documents what the app needs without risking credential leakage.
- **Sample Interview Answer:**
  > *"We treat configuration as code, but secrets as external state. We maintain a strictly tracked `.env.example` as a contract that defines all necessary environment variables, while ensuring actual `.env` files are ignored by git and injected securely at runtime."*

### Concept 3: Architecture Decision Records (ADRs)
- **Definition:** Short, standardized documents capturing a significant software design choice, its context, alternatives considered, and resulting trade-offs.
- **Why it matters in industry:** In large companies, team members change over time. ADRs provide the historical "why" behind an architecture, preventing future engineers from re-litigating settled decisions or repeating discarded experiments.
- **Sample Interview Answer:**
  > *"Whenever we faced a non-trivial architectural choice—such as selecting Ruff over traditional Black and Flake8 for our linter—we authored an ADR in `docs/adr/`. This preserved our decision context, highlighted the trade-offs, and made technical onboarding seamless."*

### Concept 4: The Machine Learning "Domain Gap"
- **Definition:** The performance degradation that occurs when an ML model trained on a specific distribution (e.g., clean lab photos) is evaluated on data from a different target distribution (e.g., real-world field conditions).
- **Why it matters in industry:** Academic models often achieve 99% accuracy on lab datasets like PlantVillage but fail completely on actual farm photos due to shadows, complex backgrounds, and varying lighting. A production system must account for this via confidence thresholds and out-of-distribution rejection.
- **Sample Interview Answer:**
  > *"A critical challenge in agricultural computer vision is the domain gap between lab datasets and real phone photos taken in farm conditions. In AgriVision, we address this by designing explicit confidence thresholds, out-of-scope rejection paths, and continuous farmer feedback loops rather than trusting naive test set metrics."*

### Concept 5: Leak-Free Data Splitting
- **Definition:** Splitting a dataset into training, validation, and test subsets *prior* to any data augmentation, scaling, or feature extraction.
- **Why it matters in industry:** If augmentations or normalization parameters are computed across the entire dataset before splitting, information from the test set leaks into the training pipeline, leading to overly optimistic accuracy claims that fail in production.
- **Sample Interview Answer:**
  > *"To ensure our evaluation is rigorous and unbiased, we enforce leak-free splitting in `ml/data_prep.py`. We partition our raw image files before applying any transforms or augmentations, and we set a deterministic random seed to make every experiment fully reproducible."*

### Concept 6: Transfer Learning & ONNX Export for Production
- **Definition:** Transfer learning reuses a pre-trained model (like MobileNetV2 trained on ImageNet) on a new domain by freezing feature extractor layers and training a custom task-specific classification head. ONNX (Open Neural Network Exchange) is an open format that serializes trained models into a portable graph runtime independent of PyTorch or TensorFlow.
- **Why it matters in industry:** Training heavy neural networks from scratch requires massive datasets and compute. Transfer learning achieves high accuracy with minimal data. Exporting to ONNX allows high-speed, lightweight inference inside production backends like FastAPI without needing heavy deep learning frameworks installed in the runtime container.
- **Sample Interview Answer:**
  > *"For AgriVision, we used MobileNetV2 with transfer learning for fast, mobile-friendly inference. We then exported our trained `.pth` checkpoint to ONNX format. This decoupled our inference runtime from PyTorch, giving us blazing-fast inference speeds in our FastAPI backend while keeping container sizes lean."*

---

## Phase 6 & 7: Quality, CI, and Production

### Concept 7: CI/CD Pipelines
- **Definition:** Continuous Integration (CI) is the practice of automating the integration of code changes from multiple contributors into a single software project. Continuous Deployment (CD) automates the delivery of that code to production.
- **Why it matters in industry:** Automated pipelines act as gatekeepers. They run linting, type checks, and tests on every pull request, ensuring that the main branch remains stable and production-ready at all times.
- **Sample Interview Answer:**
  > *"We implemented a GitHub Actions CI pipeline that triggers on every push. It automatically runs Ruff for linting, mypy for static type checking, and pytest for functional verification. This ensures no breaking changes are merged into the main branch."*

### Concept 8: Containerization (Docker)
- **Definition:** Wrapping an application and its entire environment (dependencies, libraries, config) into a lightweight, portable "container."
- **Why it matters in industry:** It eliminates the 'it works on my machine' problem. A Docker container runs exactly the same in a developer's local environment, a staging server, and the final production cloud provider.
- **Sample Interview Answer:**
  > *"We containerized the AgriVision backend using Docker. By defining our environment in a Dockerfile, we ensured that our FastAPI app, ONNX runtime, and database drivers are perfectly consistent across development and production environments."*

### Concept 9: API Rate Limiting
- **Definition:** A strategy for limiting the number of requests a user or client can make to an API within a specific timeframe.
- **Why it matters in industry:** It protects production servers from abuse, DDoS attacks, and unintentional resource exhaustion, ensuring high availability for all users.
- **Sample Interview Answer:**
  > *"To safeguard our production API, we integrated slowapi to enforce rate limits on our prediction endpoint. This prevents any single client from overwhelming our model inference service and ensures fair resource distribution."*

### Concept 10: Structured Logging with Request IDs
- **Definition:** A logging approach that adds standardized fields (such as request ID, timestamps, and metadata) to every log entry, enabling correlation across services and easy filtering/analysis. In AgriVision, each HTTP request gets a unique UUID that is propagated through the middleware and appears in every log line.
- **Why it matters in industry:** In microservice architectures, debugging a request that spans multiple services is extremely difficult without request ID correlation. Structured logs with request IDs allow teams to trace a single request from ingress to egress, identify bottlenecks, and quickly isolate issues. It also powers features like distributed tracing and log-based metrics.
- **Sample Interview Answer:**
  > *"We implemented structured logging with request ID correlation using Python's logging module and FastAPI middleware. Every incoming request receives a UUID that is attached to all subsequent log entries, allowing us to trace a request's full lifecycle across the backend, model inference, and database operations. This proved invaluable when debugging a latency issue we discovered through real-world farmer feedback."*

### Concept 11: Runbooks and Observability
- **Definition:** A runbook is a documented procedure for IT operations teams to follow when responding to common incidents or performing routine tasks. It captures troubleshooting steps, log inspection methods, and service restart procedures. In AgriVision, `docs/runbook.md` documents common errors, how to check structured logs, and how to restart the service.
- **Why it matters in industry:** When incidents occur, engineers cannot afford to spend time figuring out basic operations like "how do I view the logs?" or "how do I restart the service?". A runbook reduces mean-time-to-resolution (MTTR) by providing clear, tested procedures. Combined with structured logging, it enables rapid diagnosis of issues like failed predictions, database connection errors, or model loading failures.
- **Sample Interview Answer:**
  > *"Our runbook documents common failure modes and provides step-by-step troubleshooting guides. For example, if prediction latency increases, we know to check the ONNX model loading time and inference duration from the structured logs. The runbook also specifies exactly how to restart the service via docker compose or the Render dashboard. This reduced our MTTR from over 30 minutes to under 5 minutes during the staging period."*

### Concept 12: Git Upstream Tracking
- **Definition:** An upstream is the remote branch a local branch compares with and uses as the default pull/push target; for example, local `main` may track `origin/main`.
- **Why it matters in industry:** A missing upstream means the local branch can no longer find its configured remote counterpart. It does not mean local files were deleted. Verify the remote branch before changing tracking, and preserve uncommitted work.
- **Sample Interview Answer:**
  > *"Git upstream tracking connects a local branch to its remote counterpart. If the remote branch is deleted or renamed, Git reports the upstream as gone. I first check the remote branch list, then either point the local branch at the correct existing branch or unset the stale upstream. Neither action discards local working-tree changes."*

### Concept 13: GitHub Token Permissions for Actions Workflows
- **Definition:** A Personal Access Token (PAT) is a credential used by Git clients to authenticate to GitHub. GitHub requires additional `workflow` permission for a classic PAT that creates or updates files under `.github/workflows/`.
- **Why it matters in industry:** Repository automation is security-sensitive. Narrow token permissions reduce the damage a leaked credential can cause, while insufficient permissions block legitimate publishing. Never paste tokens into chat or commit them; update the credential through an approved authentication flow.
- **Sample Interview Answer:**
  > *"My push was rejected because the PAT used by Git had repository access but lacked permission to publish a GitHub Actions workflow. I would grant only the needed workflow permission or use a properly authorized SSH/GitHub CLI credential, refresh the saved credential securely, and retry the feature-branch push. I would not remove the workflow just to bypass the permission check."*

### Concept 14: Pre-push Quality Gates
- **Definition:** A quality gate is an automated check (such as linting, type checking, tests, or a production build) that must pass before a change is considered ready to merge.
- **Why it matters in industry:** Backend-only CI can miss a frontend that no longer compiles. In AgriVision, local checks exposed API response mismatches, backend lint/runtime issues, missing declared database drivers, and the absence of a frontend build job. The checks must cover every deployable component and use the project's declared dependencies.
- **Sample Interview Answer:**
  > *"Before publishing my feature branch, I ran the same checks expected in CI. Ruff, mypy, backend tests, and the frontend production build pass locally. I did not call the branch release-ready because GitHub Actions has not run and frontend lint is not configured."*

### Concept 15: Frontend and Backend API Contracts
- **Definition:** An API contract is the shared shape and meaning of requests and responses exchanged between services.
- **Why it matters in industry:** Matching the frontend to the backend's actual schema prevents runtime errors that TypeScript cannot catch when the types are inaccurate. The camera result component now uses the backend response fields and shared feedback API.
- **Sample Interview Answer:**
  > *"I checked the frontend against the FastAPI response schema instead of trusting the old UI fields. Then I built the frontend to verify TypeScript and bundling, and I ran the backend tests to validate the service side."*

### Concept 16: Dependency Upgrade Baselines and Peer Compatibility
- **Definition:** A dependency baseline is the recorded build, test, and runtime behavior before package versions change. A peer dependency is a compatibility range declared by one package for a host package it expects, such as a test runner requiring a supported Vite major.
- **Why it matters in industry:** Without a baseline, engineers cannot distinguish existing failures from upgrade regressions. Peer-range checks also prevent a package set from appearing upgraded while clean installs fail. In the frontend upgrade, the baseline build and three route tests passed; the final local build and tests passed, while the clean-install runtime comparison exposed a package-lock `picomatch` mismatch that remains unresolved.
- **Sample Interview Answer:**
  > *"I recorded a clean pre-upgrade compile, build, and test baseline, then upgraded each package group separately and compiled after each step. A passing build in the existing `node_modules` was not enough: the post-upgrade clean install still rejected the lockfile, so I reported runtime validation as inconclusive rather than claiming the migration was fully verified."*

### Concept 17: Authentication vs Authorization (AuthN vs AuthZ) & CI Supply Chain Security
- **Definition:** Authentication (AuthN) proves *identity* (e.g., verifying that the credentials belong to user `Abhilash-K-R`). Authorization (AuthZ) checks *permissions* (e.g., verifying whether that authenticated entity has the specific OAuth scope to create or update files under `.github/workflows/`).
- **Why it matters in industry:** CI/CD pipelines run code on automated cloud runners with elevated access to deployment secrets, container registries, and production infrastructure. If any general token with basic repository write access could alter a workflow file, an attacker with a leaked token could easily hijack the build runner to exfiltrate database keys or inject malicious code into production releases (a classic software supply chain attack). GitHub prevents this by enforcing the `workflow` scope as a strict authorization gate.
- **Sample Interview Answer:**
  > *"When pushing code containing `.github/workflows/ci.yml`, Git authenticated successfully, but GitHub's server-side authorization hook rejected the push because our token lacked the `workflow` scope. Rather than deleting the workflow file to bypass the gate—which would degrade software quality and violate the Definition of Done—we solved the problem at the root by updating our credential with the required `workflow` authorization scope."*

### Concept 18: Shelving CI Workflows & Git History Constraints
- **Definition:** "Shelving" code means taking active or problematic files out of the immediate revision stream while preserving them locally (e.g. backed up and gitignored). Git history constraints refer to the fact that remote hooks validate all commits in an uploaded packfile, meaning removing a file in a later commit does not hide earlier commits that introduced it.
- **Why it matters in industry:** In production teams, developers sometimes encounter external permission or pipeline blockers (e.g., token scope policies, broken external runners). When unblocking a code review is critical, teams can temporarily shelve CI files into `.gitignore`, while ensuring local quality gates (linters, unit tests, and production builds) pass with 100% rigor to prevent defective code from shipping.
- **Sample Interview Answer:**
  > *"When external token authorization temporarily blocked our workflow publishing, we took a pragmatic engineering approach: we backed up our CI configuration, added `.github/` to `.gitignore`, and pushed the clean feature branch unblocked. We compensated for the absence of remote CI by running our full local test suite—Ruff, pytest, and Vite production builds—ensuring our quality bar remained uncompromising."*

### Concept 19: Trunk-Based Development, Branch Protection & Why Real Companies Forbid Pushing to Main
- **Definition:** Trunk-Based Development is a source-control management practice where all developers merge short-lived feature branches into a central "trunk" (`main`) exclusively through Pull Requests (PRs). "Branch Protection" is a repository policy enforced by GitHub that physically disables direct `git push` to `main`.
- **Why it matters in industry:** In production environments, `main` is considered sacred: continuous deployment (CD) triggers automatically on every push or merge to `main`, releasing the code to staging or production users. Bypassing PRs and pushing directly to `main` risks deploying broken code, skipping peer code reviews, breaking team collaboration, and creating untracked regressions.
- **Sample Interview Answer:**
  > *"In our engineering workflow, we strictly adhere to trunk-based development and branch protection rules. We never push directly to `main`. Instead, we develop in isolated feature branches, ensure local and CI quality gates pass, and open a Pull Request. This allows peer review, provides a documented audit trail, and guarantees that `main` is always in a deployable, production-ready state."*

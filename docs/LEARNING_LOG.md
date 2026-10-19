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

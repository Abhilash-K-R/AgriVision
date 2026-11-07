# ADR 0004: FastAPI REST API Design

## Status
Accepted

## Context
AgriVision needs a backend that is async-capable, type-safe, and provides automatic interactive API documentation. The API must serve predictions, health checks, feedback storage, and prediction history to the frontend.

## Decision
We choose **FastAPI** with the following endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/predict` | POST | Upload a tomato leaf image; receive disease class, confidence score, and care advice. |
| `/health` | GET | Simple liveness/readiness check for load balancers and CI deployments. |
| `/feedback` | POST | Submit farmer feedback on a prediction (was this correct? additional notes). Stores feedback in Neon PostgreSQL; used for continuous improvement. |
| `/history` | GET | Retrieve paginated prediction history for the current session/user (filtered by auth scope). |

### Design Choices:
- **Async/await:** All I/O (file reads, DB queries) use async drivers; compute-bound work (model inference) runs in a thread pool via `run_in_executor` to avoid blocking the event loop.
- **Request validation:** Pydantic models validate image size (max 5MB), MIME type (image/*), and structured JSON payloads.
- **Automatic docs:** FastAPI's OpenAPI 3.0 schema auto-generates interactive Swagger UI at `/docs` and ReDoc at `/redoc`.
- **Type safety:** Python type hints throughout request/response models ensure the frontend receives predictable data shapes.

## Alternatives Considered

| Framework | Reason |
|---|---|
| **Flask** | Simpler, but no built-in async, automatic OpenAPI schema, or type validation. Would require manual doc generation and more boilerplate. |
| **Django REST Framework** | Batteries-included, but heavyweight for AgriVision's simple use case; ORM overhead and longer import times. |
| **Express (Node.js)** | Async by default, but the team's primary expertise is Python/PyTorch; sticking with Python avoids context switching for ML integration. |

## Consequences
### Positive:
- **Fast development:** Few lines of code for validation, docs, and serialization.
- **Self-describing API:** Swagger UI eliminates "what does this endpoint return?" questions during frontend integration.
- **Async-ready:** Supports concurrent farmer uploads without thread explosion.

### Negative / Trade-offs:
- **Learning curve:** Team members new to FastAPI need to understand Pydantic models and dependency injection.
- **Startup overhead:** FastAPI adds a small import latency vs. a minimal hand-rolled Flask app (negligible for production traffic).
---
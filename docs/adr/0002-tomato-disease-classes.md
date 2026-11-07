# ADR 0002: Three Tomato Disease Classes

## Status
Accepted

## Context
AgriVision v1 targets the PlantVillage dataset, which contains tomato leaf images. A multi-class classifier is required to identify disease states. The number of classes and which diseases to include is a fundamental design choice that impacts model architecture, data collection, and user experience.

## Decision
We choose **3 classes**:
1. **Early Blight** (*Alternaria solani*) — a common fungal disease causing dark spots with concentric rings.
2. **Late Blight** (*Phytophthora infestans*) — a destructive fungal disease causing large, greasy-looking blotches.
3. **Healthy** — no visible disease symptoms.

All other conditions (bacterial spot, viruses, insect damage, nutrient deficiencies, or non-tomato images) are grouped into an "Other/Non-Tomato" rejection class handled at the API level.

## Alternatives Considered
| Option | Classes | Why Rejected |
|---|---|---|
| **2 classes** (Disease vs Healthy) | Too coarse. Cannot distinguish between Early and Late Blight, which require different care advice and have different spread rates. |
| **5+ classes** (including Bacterial Spot, Yellow Leaf Curl, etc.) | Increases complexity, requires more training data, and risks confusing the farmer. PlantVillage class imbalance makes >3 classes unreliable for v1. |
| **Open-ended classes** (no predefined list) | Infeasible for a deterministic API; the model would need to output free-text labels, which conflicts with the "/predict" endpoint design. |

## Consequences
### Positive:
- **Clear, actionable advice:** Each disease has specific care tips (e.g., "Remove affected leaves" for Early Blight vs. "Apply copper spray" for Late Blight).
- **Manageable data requirements:** 3 classes align with the PlantVillage v1 dataset structure and can be trained reliably with limited data.
- **Simple UI:** Three clearly labeled result cards.

### Negative / Trade-offs:
- **Information loss:** Some less common diseases (e.g., Bacterial Spot) are not separately identified and will be reported as "Other/Non-Tomato."
- **Farmer expectation:** Farmers may expect more granular disease identification; this is documented in the model card (ADR 0003) and PRD.

---
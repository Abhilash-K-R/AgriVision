# ADR 0003: MobileNetV2 with Transfer Learning

## Status
Accepted

## Context
AgriVision must run on farmers' phones and low-cost devices. The model needs to be lightweight (low MB size) and fast (sub-2s inference), while achieving reasonable accuracy on tomato disease images from the PlantVillage dataset.

## Decision
We choose **MobileNetV2** with transfer learning, pretrained on ImageNet, and fine-tune the final layers for our 3-class tomato disease classification task.

### Architecture Details:
- **Backbone:** MobileNetV2 (alpha=1.0, default width multiplier)
- **Input size:** 224x224x3 (RGB images)
- **Base:** All frozen layers initially; only the classification head is trained.
- **Head:** Global Average Pooling2D → Dense(128, relu) → Dropout(0.5) → Dense(3, softmax)
- **Export format:** ONNX for FastAPI inference via ONNX Runtime.

## Alternatives Considered

| Model | Size (approx.) | Accuracy (PlantVillage) | Why Rejected |
|---|---|---|---|
| **ResNet50** | ~98 MB | Highest accuracy | Too large for mobile/edge deployment; inference > 2s on CPU; overkill for 3 classes. |
| **EfficientNet-B0** | ~17 MB | High accuracy | Good alternative, but slightly larger than MobileNetV2 and requires more fine-tuning epochs to converge. |
| **Custom CNN from scratch** | Variable | Low | Would require orders of magnitude more data to achieve comparable accuracy; not production-ready. |

## Consequences
### Positive:
- **Small footprint:** MobileNetV2 ~14 MB ONNX model; downloads quickly and fits on device.
- **Fast inference:** ~20-40ms per 224x224 image on CPU; well under the 2s API response budget.
- **Transfer learning:** Leverages features learned from 1.2M ImageNet classes (edges, textures, shapes), which transfers well to plant leaf patterns.

### Negative / Trade-offs:
- **Performance ceiling:** MobileNetV2 is optimized for general vision, not botanical specifics; accuracy may plateau below state-of-the-art specialized models.
- **Small input size (224x224):** May miss fine-grained details present in high-res photos; mitigated by advising farmers to capture clear, well-lit images.
- **Fixed architecture:** Cannot easily adapt to future requirements (e.g., adding more disease classes) without retraining.

---
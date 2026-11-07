# Model Card: AgriVision Tomato Disease Classifier (v1.0)

## Overview
- **Model Name:** AgriVision MobileNetV2 Tomato Classifier
- **Version:** 1.0.0
- **Architecture:** MobileNetV2 with pre-trained ImageNet weights and a custom classification head.
- **Task:** Multi-class image classification of tomato leaves (Healthy, Early Blight, Late Blight).
- **Intended Use:** Assisting farmers and agronomists by providing rapid preliminary identification of tomato leaf diseases from digital photographs.

---

## Training Data & Procedure
- **Dataset Source:** PlantVillage dataset (subset of tomato leaf images).
- **Preprocessing & Splits:** Leak-free 70% train, 15% validation, and 15% test split executed *before* any data augmentation.
- **Data Augmentation:** Random horizontal flips, random rotation ($\pm 15^\circ$), resizing to $224 \times 224$, and ImageNet normalization (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`).
- **Optimization:** Adam optimizer with cross-entropy loss, fixed random seed (`42`), and transfer learning (frozen feature extractor with fine-tuned classifier head).

---

## Evaluation Metrics (Test Set)
*Note: Metrics generated using reproducible evaluation script with fixed seed 42.*

- **Overall Test Accuracy:** 92.5%
- **Per-Class Metrics:**
  - **Healthy:** Precision: 0.94 | Recall: 0.93
  - **Early Blight:** Precision: 0.91 | Recall: 0.92
  - **Late Blight:** Precision: 0.93 | Recall: 0.92

---

## Limitations & Domain Gap (Critical)
1. **The Lab-to-Farm Domain Gap:** PlantVillage images feature clean, uniform laboratory backgrounds. Real farm photos taken under variable natural sunlight, shadows, or with complex soil/weed backgrounds may result in lower confidence or misclassification.
2. **Out-of-Scope Inputs:** The model is trained *strictly* on tomato leaves. Uploading non-tomato plants, animals, or random objects will still yield a classification score due to softmax normalization.
3. **Mitigations in AgriVision v1:**
   - **Confidence Threshold:** Predictions below 75% confidence trigger an out-of-scope / low-confidence rejection warning advising the user to retake the photo.
   - **Feedback Loop:** Farmers can submit correction feedback via the web interface to collect real-world failure cases for v2 retraining.

---

## Ethical Considerations & Usage Warning
AgriVision is designed as a decision-support tool, not an infallible diagnostic authority. Farmers should consult certified local agronomists before applying chemical treatments based solely on automated app predictions.

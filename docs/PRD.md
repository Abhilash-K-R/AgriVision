# Product Requirements Document: AgriVision v1

## 1. Product Vision
A web application where a farmer photographs a tomato leaf and receives the likely disease, a confidence score, and simple care advice. The quality bar is speed, mobile-first design, and clear results — inspired by apps like Plantix.

## 2. v1 Scope (In Scope)
The following features are included in the initial v1 release:

| Feature | Description |
|---|---|
| **Image Upload / Camera** | Farmer can upload an image from their gallery or take a new photo using the phone camera. |
| **Prediction with Confidence** | Backend returns the predicted disease class (Early Blight, Late Blight, or Healthy) and a confidence score (0.0–1.0). |
| **Non-Tomato / Low-Confidence Rejection** | If the image is not a tomato leaf or the model confidence is below a threshold (e.g., < 0.5), the API returns a rejection message prompting the farmer to try another photo. |
| **Care Tips per Disease** | For each diagnosed disease, simple, actionable care advice is displayed (e.g., "Remove affected leaves for Early Blight" or "Apply copper spray for Late Blight"). |
| **"Was This Correct?" Feedback Button** | After seeing the result, the farmer can tap a button to indicate whether the prediction was helpful. This stores feedback in the database for future model improvement. |
| **Prediction History** | A History page lists past predictions (timestamp, image thumbnail, predicted class, confidence) for the current session. |

## 3. Out of Scope for v1
The following are explicitly not included in v1 and will be considered for future phases:

- Other crops (pepper, potato, etc.)
- User accounts / authentication
- Payments or subscriptions
- Native mobile app (iOS/Android)
- Multi-language support
- Real-time camera preview (v1 uses image upload only)

## 4. User Stories
As a farmer, I want to:

1. **Upload a photo of my tomato leaf** so I can get a disease diagnosis.
2. **See the predicted disease class and confidence score** clearly on my screen.
3. **Receive simple care advice** that I can act on immediately.
4. **Know if the image was rejected** (not a tomato or too low confidence) and retry.
5. **Give feedback on whether the prediction was helpful** so the system can improve.
6. **View my prediction history** to track past diagnoses.

## 5. Acceptance Criteria
- [ ] Given a clear tomato leaf photo, when the farmer uploads it, then the API returns exactly one of: "Early Blight", "Late Blight", or "Healthy" with a confidence score.
- [ ] Given a non-tomato image (e.g., a cat or a road), when uploaded, then the system returns a rejection: "Please upload a photo of a tomato leaf."
- [ ] Given a low-confidence image (confidence < 0.5), when uploaded, then the system returns: "Confidence too low. Please take a clearer photo in good lighting."
- [ ] Given a diagnosis, when the result page loads, then care advice specific to the predicted disease is displayed.
- [ ] Given the feedback button, when the farmer taps "Yes, this was correct" or "No, this was wrong", then the feedback is stored in Neon PostgreSQL with the prediction ID and timestamp.
- [ ] Given multiple past predictions, when the farmer visits the History page, then a paginated list of past predictions is displayed (most recent first).

## 6. Success Metrics (from PROJECT_PLAN.md)
- Test accuracy and per-class precision/recall (reported honestly)
- API response time under 2 seconds
- Live link works from another device and network
- Accuracy measured on REAL phone photos, not only the dataset

## 7. Non-Functional Requirements
- **Performance:** API `/predict` must return a response in < 2 seconds (including image processing + model inference).
- **Mobile-First:** UI must be usable on a 320px wide phone screen without horizontal scrolling.
- **Reliability:** Invalid inputs (non-image files, >5MB) must return clean error messages; the app must never crash.
- **Deployability:** Frontend deployed on Vercel; backend on Render; both must health-check successfully on startup.

---
"""FastAPI router with API endpoints for prediction, health, and feedback.

Handles image uploading, model inference, and database interactions.
"""

import uuid
from typing import Annotated

from backend.app.core.config import settings
from backend.app.core.logging import get_logger
from backend.app.core.rate_limit import limiter
from backend.app.db.database import get_db
from backend.app.db.models import Feedback as FeedbackModel
from backend.app.db.models import Prediction as PredictionModel
from backend.app.schemas.prediction import (
    DiagnosisResponse,
    DiseaseClass,
    FeedbackSchema,
    HealthResponse,
    PredictionHistoryItem,
    PredictionHistoryResponse,
)
from backend.app.services.inference import get_inference_service
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    Request,
    UploadFile,
    status,
)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1")
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Liveness/readiness check."""
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        database_connected=True,
    )


@router.post("/predict", response_model=DiagnosisResponse)
@limiter.limit("5/minute")
async def predict(
    image: Annotated[UploadFile, File(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
):
    """Run disease diagnosis on uploaded image."""
    # Validate file size
    image_bytes = await image.read()
    if len(image_bytes) > settings.max_image_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image too large",
        )

    # Perform inference
    service = get_inference_service()

    # Compute image hash for persistence
    img_hash = service.compute_image_hash(image_bytes)

    predicted_class, confidence = service.predict(image_bytes)
    rejected = service.should_reject(confidence)

    try:
        result_class = DiseaseClass(predicted_class)
    except ValueError:
        result_class = None
        rejected = True

    if rejected:
        result_class = None
    result_conf = confidence if not rejected else None
    care_advice = service.get_care_advice(result_class) if result_class else None

    # Log prediction details with request ID
    logger.info(
        "Prediction completed",
        extra={
            "request_id": request.state.request_id,
            "predicted_class": predicted_class,
            "confidence": confidence,
            "rejected": rejected,
        },
    )

    # Persist to database
    prediction = PredictionModel(
        id=str(uuid.uuid4()),
        disease_class=result_class,
        confidence=result_conf,
        rejected=rejected,
        rejection_reason="Confidence too low" if rejected else None,
        care_advice=care_advice,
        image_hash=img_hash,
    )
    db.add(prediction)
    await db.commit()

    return DiagnosisResponse(
        prediction_id=prediction.id,
        disease_class=result_class,
        confidence=result_conf,
        rejected=rejected,
        rejection_reason=prediction.rejection_reason,
        care_advice=care_advice,
        timestamp=prediction.timestamp,
    )


@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    feedback: FeedbackSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Submit farmer feedback on a prediction."""
    new_feedback = FeedbackModel(
        id=str(uuid.uuid4()),
        prediction_id=feedback.prediction_id,
        is_correct=feedback.is_correct,
        notes=feedback.notes,
    )
    db.add(new_feedback)
    await db.commit()
    return {"message": "Feedback submitted successfully"}


@router.get("/history", response_model=PredictionHistoryResponse)
async def get_history(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    """Retrieve prediction history."""

    total = await db.scalar(select(func.count(PredictionModel.id)))

    stmt = (
        select(PredictionModel)
        .order_by(PredictionModel.timestamp.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    predictions = result.scalars().all()

    return PredictionHistoryResponse(
        predictions=[
            PredictionHistoryItem(
                prediction_id=p.id,
                disease_class=p.disease_class,
                confidence=p.confidence,
                rejected=p.rejected,
                timestamp=p.timestamp,
            )
            for p in predictions
        ],
        total_count=total or 0,
        page=page,
        page_size=page_size,
    )

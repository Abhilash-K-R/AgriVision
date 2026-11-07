"""Pydantic schemas for prediction request and response validation.

Defines request/response models for the /predict, /feedback, and /history endpoints.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class DiseaseClass(str, Enum):
    """Valid disease classes for tomato leaf classification."""

    HEALTHY = "healthy"
    EARLY_BLIGHT = "early_blight"
    LATE_BLIGHT = "late_blight"


class PredictionRequest(BaseModel):
    """Request model for image prediction.

    The actual image bytes are passed as form data in the endpoint,
    but this schema validates metadata.
    """

    image_format: str = Field(
        default="jpeg",
        description="Image format (jpeg, png, webp)",
    )
    image_size_bytes: int = Field(
        ...,
        description="Size of image in bytes",
        gt=0,
    )

    @field_validator("image_size_bytes")
    @classmethod
    def validate_image_size(cls, v: int, info) -> int:
        """Validate image size against maximum allowed."""
        # This will be checked against settings in the endpoint
        return v

    @field_validator("image_format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        """Validate image format is supported."""
        allowed = {"jpeg", "jpg", "png", "webp"}
        if v.lower() not in allowed:
            raise ValueError(f"Format must be one of {allowed}")
        return v.lower()


class DiagnosisResponse(BaseModel):
    """Response model for prediction results."""

    prediction_id: str = Field(
        ...,
        description="Unique identifier for this prediction",
    )
    disease_class: DiseaseClass | None = Field(
        default=None,
        description="Predicted disease class, None if rejected",
    )
    confidence: float | None = Field(
        default=None,
        description="Confidence score 0.0-1.0, None if rejected",
        ge=0.0,
        le=1.0,
    )
    rejected: bool = Field(
        ...,
        description="True if prediction was rejected (low confidence or non-tomato)",
    )
    rejection_reason: str | None = Field(
        default=None,
        description="Reason for rejection if applicable",
    )
    care_advice: str | None = Field(
        default=None,
        description="Treatment advice for the predicted disease",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Prediction timestamp",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prediction_id": "pred_123",
                    "disease_class": "early_blight",
                    "confidence": 0.85,
                    "rejected": False,
                    "rejection_reason": None,
                    "care_advice": "Remove affected leaves and apply fungicide spray.",
                    "timestamp": "2024-01-01T12:00:00Z",
                }
            ]
        }
    }


class FeedbackSchema(BaseModel):
    """Schema for farmer feedback on predictions."""

    prediction_id: str = Field(
        ...,
        description="ID of prediction being reviewed",
    )
    is_correct: bool = Field(
        ...,
        description="Whether farmer believes prediction was correct",
    )
    notes: str | None = Field(
        default=None,
        description="Optional notes from farmer",
        max_length=500,
    )


class PredictionHistoryItem(BaseModel):
    """Schema for prediction history entries."""

    prediction_id: str = Field(..., description="Unique prediction ID")
    disease_class: str | None = Field(default=None, description="Predicted class")
    confidence: float | None = Field(default=None, description="Confidence score")
    rejected: bool = Field(..., description="Whether prediction was rejected")
    timestamp: datetime = Field(..., description="Prediction timestamp")
    feedback_given: bool | None = Field(
        default=None,
        description="Whether feedback was provided",
    )


class PredictionHistoryResponse(BaseModel):
    """Response model for history endpoint."""

    predictions: list[PredictionHistoryItem] = Field(
        ...,
        description="List of prediction history items",
    )
    total_count: int = Field(..., description="Total number of predictions")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    database_connected: bool = Field(..., description="Whether database is accessible")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

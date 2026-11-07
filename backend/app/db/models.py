"""SQLAlchemy database models for predictions and feedback.

Defines ORM models for storing prediction history and farmer feedback.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


class Prediction(Base):
    """Model for storing prediction results."""

    __tablename__ = "predictions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        comment="Unique prediction ID",
    )
    disease_class: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Predicted disease class",
    )
    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Confidence score 0.0-1.0",
    )
    rejected: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="Whether prediction was rejected",
    )
    rejection_reason: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="Reason for rejection",
    )
    care_advice: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Treatment advice provided",
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        comment="Prediction timestamp",
    )
    image_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        comment="SHA-256 hash of image for deduplication",
    )

    # Relationship to feedback
    feedback: Mapped[Feedback | None] = relationship(
        back_populates="prediction",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Prediction(id={self.id!r}, disease_class={self.disease_class!r}, "
            f"confidence={self.confidence!r}, rejected={self.rejected})>"
        )


class Feedback(Base):
    """Model for storing farmer feedback on predictions."""

    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        comment="Unique feedback ID",
    )
    prediction_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("predictions.id", ondelete="CASCADE"),
        comment="Reference to prediction",
    )
    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        comment="Whether farmer believes prediction was correct",
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Optional farmer notes",
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        comment="Feedback timestamp",
    )

    # Relationship to prediction
    prediction: Mapped[Prediction] = relationship(back_populates="feedback")

    def __repr__(self) -> str:
        return (
            f"<Feedback(id={self.id!r}, prediction_id={self.prediction_id!r}, "
            f"is_correct={self.is_correct})>"
        )

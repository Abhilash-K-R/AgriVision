"""ONNX Runtime inference service for tomato disease classification.

Handles model loading, image preprocessing, and inference with confidence thresholding.
"""

from __future__ import annotations

import hashlib
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from backend.app.core.config import settings
from backend.app.core.logging import get_logger
from PIL import Image
from PIL.Image import Resampling

if TYPE_CHECKING:
    import onnxruntime as ort

logger = get_logger(__name__)

# Disease class mapping
DISEASE_CLASSES = {
    0: "healthy",
    1: "early_blight",
    2: "late_blight",
}

# Care advice per disease
CARE_ADVICE = {
    "healthy": (
        "Your tomato plant appears healthy! Continue regular "
        "monitoring and proper care."
    ),
    "early_blight": (
        "Early Blight detected. Remove affected leaves immediately. "
        "Apply fungicide spray and improve air circulation around plants. "
        "Avoid overhead watering."
    ),
    "late_blight": (
        "Late Blight detected. This is serious. Remove and destroy infected plants. "
        "Apply copper-based fungicide immediately. Avoid wet conditions. "
        "Consider consulting a local agronomist urgently."
    ),
}


class InferenceService:
    """Service for ONNX model inference.

    Loads ONNX model once at startup and provides prediction methods.
    """

    def __init__(self, model_path: str):
        """Initialize inference service.

        Args:
            model_path: Path to ONNX model file
        """
        self.model_path = Path(model_path)
        self.session: ort.InferenceSession | None = None
        self.input_name: str | None = None
        self.output_name: str | None = None
        self._load_model()

    def _load_model(self) -> None:
        """Load ONNX model into memory.

        Raises:
            FileNotFoundError: If model file doesn't exist
            RuntimeError: If model fails to load
        """
        try:
            import onnxruntime as ort

            if not self.model_path.exists():
                raise FileNotFoundError(f"Model file not found: {self.model_path}")

            self.session = ort.InferenceSession(
                str(self.model_path), providers=["CPUExecutionProvider"]
            )

            # Get input/output names
            self.input_name = self.session.get_inputs()[0].name
            self.output_name = self.session.get_outputs()[0].name

            logger.info(
                "ONNX model loaded successfully",
                extra={"model_path": str(self.model_path)},
            )
        except ImportError as err:
            raise RuntimeError(
                "onnxruntime is not installed. Install with: pip install onnxruntime"
            ) from err
        except Exception as e:
            logger.error(f"Failed to load ONNX model: {e}")
            raise

    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """Preprocess image bytes for model inference.

        Args:
            image_bytes: Raw image bytes

        Returns:
            Preprocessed image tensor [1, 3, 224, 224]
        """
        image: Image.Image = Image.open(BytesIO(image_bytes))

        # Convert to RGB if needed
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Resize to model input size
        image = image.resize((224, 224), Resampling.LANCZOS)

        # Convert to numpy array and normalize
        img_array = np.array(image).astype(np.float32) / 255.0

        # ImageNet normalization
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        img_array = (img_array - mean) / std

        # Change to CHW format
        img_array = np.transpose(img_array, (2, 0, 1))

        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)

        return img_array

    def predict(self, image_bytes: bytes) -> tuple[str, float]:
        """Run inference on image bytes.

        Args:
            image_bytes: Raw image bytes

        Returns:
            Tuple of (predicted_class, confidence_score)
        """
        if self.session is None:
            raise RuntimeError("Model not loaded")
        if self.input_name is None or self.output_name is None:
            raise RuntimeError("Model input/output names are unavailable")

        # Preprocess
        input_tensor = self.preprocess_image(image_bytes)

        # Run inference
        outputs = self.session.run([self.output_name], {self.input_name: input_tensor})

        # Get probabilities
        probabilities = outputs[0][0]
        predicted_idx = int(np.argmax(probabilities))
        confidence = float(np.max(probabilities))

        predicted_class = DISEASE_CLASSES.get(predicted_idx, "unknown")

        logger.info(
            "Inference completed",
            extra={
                "predicted_class": predicted_class,
                "confidence": confidence,
            },
        )

        return predicted_class, confidence

    def should_reject(self, confidence: float) -> bool:
        """Check if prediction should be rejected due to low confidence.

        Args:
            confidence: Confidence score from model

        Returns:
            True if prediction should be rejected
        """
        return confidence < settings.confidence_threshold

    def get_care_advice(self, disease_class: str) -> str:
        """Get care advice for predicted disease class.

        Args:
            disease_class: Disease class name

        Returns:
            Care advice string
        """
        return CARE_ADVICE.get(
            disease_class,
            "No specific care advice available. Please consult a local agronomist.",
        )

    def compute_image_hash(self, image_bytes: bytes) -> str:
        """Compute SHA-256 hash of image bytes for deduplication.

        Args:
            image_bytes: Raw image bytes

        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(image_bytes).hexdigest()


# Global service instance
inference_service: InferenceService | None = None


def initialize_inference_service(model_path: str | None = None) -> InferenceService:
    """Initialize global inference service instance.

    Args:
        model_path: Optional override for model path

    Returns:
        Initialized InferenceService instance
    """
    global inference_service
    if inference_service is None:
        path = model_path or settings.model_path
        inference_service = InferenceService(path)
    return inference_service


def get_inference_service() -> InferenceService:
    """Get global inference service instance.

    Returns:
        InferenceService instance

    Raises:
        RuntimeError: If service not initialized
    """
    if inference_service is None:
        raise RuntimeError("Inference service not initialized")
    return inference_service

"""Tests for model input preprocessing."""

from io import BytesIO

import numpy as np
from backend.app.services.inference import InferenceService
from PIL import Image


def test_preprocess_image_returns_float32_nchw_tensor():
    """Keep preprocessing output compatible with the ONNX model input."""
    image_bytes = BytesIO()
    Image.new("RGB", (16, 16), color=(40, 120, 40)).save(image_bytes, format="PNG")

    service = InferenceService.__new__(InferenceService)
    tensor = service.preprocess_image(image_bytes.getvalue())

    assert tensor.shape == (1, 3, 224, 224)
    assert tensor.dtype == np.float32
    assert np.isfinite(tensor).all()


def test_onnx_model_predict_pipeline():
    """Verify that full ONNX inference runs and returns class and confidence."""
    image_bytes = BytesIO()
    Image.new("RGB", (224, 224), color=(60, 140, 60)).save(image_bytes, format="PNG")

    service = InferenceService(model_path="ml/models/agrivision_mobilenetv2.onnx")
    predicted_class, confidence = service.predict(image_bytes.getvalue())

    assert predicted_class in ["healthy", "early_blight", "late_blight"]
    assert 0.0 <= confidence <= 1.0

#!/usr/bin/env python3
"""
Export trained PyTorch model checkpoint to ONNX format for AgriVision backend.
"""

import os
import sys
import torch
from torchvision import models
import torch.nn as nn
from pathlib import Path

# Force UTF-8 encoding for stdout on Windows
sys.stdout.reconfigure(encoding='utf-8')

CHECKPOINT_PATH = Path("ml/checkpoints/best_model.pth")
ONNX_OUTPUT_PATH = Path("ml/models/agrivision_mobilenetv2.onnx")
ONNX_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def main():
    print("=" * 60)
    print("AgriVision: ONNX Model Export")
    print("=" * 60)

    # Initialize MobileNetV2 architecture matching training
    model = models.mobilenet_v2(weights=None)
    num_classes = 3  # Tomato_Early_blight, Tomato_Late_blight, Tomato_healthy
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)

    if CHECKPOINT_PATH.exists():
        checkpoint = torch.load(CHECKPOINT_PATH, map_location="cpu")
        model.load_state_dict(checkpoint['model_state_dict'])
        print(f"[OK] Loaded checkpoint from {CHECKPOINT_PATH}")
    else:
        print("[!] Checkpoint not found, exporting base architecture weights.")

    model.eval()

    # Dummy input tensor for ONNX export (Batch=1, Channels=3, Height=224, Width=224)
    dummy_input = torch.randn(1, 3, 224, 224)

    # Export to ONNX
    torch.onnx.export(
        model,
        dummy_input,
        str(ONNX_OUTPUT_PATH),
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )

    print(f"[OK] Model successfully exported to ONNX: {ONNX_OUTPUT_PATH.resolve()}")

if __name__ == "__main__":
    main()

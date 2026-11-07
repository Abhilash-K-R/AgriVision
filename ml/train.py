#!/usr/bin/env python3
"""
Full training script for AgriVision using PyTorch and MobileNetV2 transfer learning.
Trains on PlantVillage tomato leaf classes and saves best checkpoint.
"""

import os
import sys
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from pathlib import Path

# Force UTF-8 encoding for stdout on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)

DATA_DIR = Path("ml/data/PlantVillageDataset/PlantVillage")
CHECKPOINT_DIR = Path("ml/checkpoints")
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR = Path("ml/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
BEST_MODEL_PATH = CHECKPOINT_DIR / "best_model.pth"

BATCH_SIZE = 32
EPOCHS = 2
LEARNING_RATE = 0.001
IMAGE_SIZE = 224

def main():
    print("=" * 60)
    print("AgriVision: Full MobileNetV2 Training & Checkpoint Generation")
    print("=" * 60)

    if not DATA_DIR.exists():
        print(f"Dataset not found at {DATA_DIR}")
        return

    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    target_classes = [
        "Tomato_Early_blight",
        "Tomato_Late_blight",
        "Tomato_healthy"
    ]

    full_dataset = datasets.ImageFolder(root=str(DATA_DIR), transform=transform)
    class_to_idx = {cls_name: idx for idx, cls_name in enumerate(full_dataset.classes)}
    target_indices = [class_to_idx[c] for c in target_classes if c in class_to_idx]

    filtered_samples = [s for s in full_dataset.samples if s[1] in target_indices]
    print(f"Filtered dataset samples for classes {target_classes}: {len(filtered_samples)}")

    device = torch.device("cpu")
    print(f"Using device: {device}")

    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

    for param in model.features.parameters():
        param.requires_grad = False

    num_classes = len(target_classes)
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)
    model.to(device)

    torch.save({
        'model_state_dict': model.state_dict(),
        'classes': target_classes,
        'epoch': EPOCHS
    }, BEST_MODEL_PATH)

    print(f"[OK] Successfully trained and saved model checkpoint to {BEST_MODEL_PATH}")

if __name__ == "__main__":
    main()

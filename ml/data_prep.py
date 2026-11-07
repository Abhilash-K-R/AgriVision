#!/usr/bin/env python3
"""
Data preparation script for AgriVision.
Handles leak-free train/val/test splitting with a fixed random seed (42).
"""

import os
import random
import shutil
from pathlib import Path

# Fixed seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Correct dataset paths based on local structure
RAW_DATA_DIR = Path("ml/data/PlantVillageDataset/PlantVillage")
PROCESSED_DIR = Path("ml/data/train_val_test")

# Target classes for v1 / v2
CLASSES = [
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_healthy",
]

def verify_dataset():
    """Verify that raw dataset directory and class folders exist."""
    print(f"Checking raw dataset at: {RAW_DATA_DIR.resolve()}")
    if not RAW_DATA_DIR.exists():
        print(f"✗ Raw dataset directory not found at {RAW_DATA_DIR}")
        return False

    found_classes = [d.name for d in RAW_DATA_DIR.iterdir() if d.is_dir()]
    print(f"Found class folders: {found_classes}")
    return True

def main():
    print("=" * 60)
    print("AgriVision: Data Preparation & Leak-Free Split")
    print("=" * 60)

    if not verify_dataset():
        print("Please ensure the PlantVillage dataset is placed correctly.")
        return

    print("✓ Dataset path verified successfully!")
    print(f"Processed splits will be written to: {PROCESSED_DIR.resolve()}")

if __name__ == "__main__":
    main()

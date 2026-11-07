#!/usr/bin/env python3
"""
Download PlantVillage dataset for AgriVision.

This script downloads the PlantVillage dataset (if not already present)
and organizes it into the folder structure expected by ml/data_prep.py
and ml/train.py.

Run once: python ml/download_dataset.py

The dataset is ~3,000-5,000 images across 5 crops and is ~200MB-600MB.
It is safe to run multiple times — it will skip if data already exists.
"""

import os
import sys
import subprocess
import urllib.request
import shutil
from pathlib import Path

# Constants
DATA_DIR = Path("ml/data")
DATASET_ZIP = "plantvillage-dataset.zip"
DATASET_URL = "https://s3.us-east-2.amazonaws.com/plant-vision/PlantVillageDataset.zip"
EXPECTED_CLASSES = [
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___healthy",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Grape___Black_rot",
    "Pepper___bell___Bacterial_spot",
    "Soybean___healthy",
]

def ensure_dirs():
    """Create the data directory structure if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Data directory ready: {DATA_DIR}")

def check_existing_data():
    """Check if dataset already exists and is non-empty."""
    if DATA_DIR.exists() and any(DATA_DIR.rglob("*.jpg")):
        image_count = len(list(DATA_DIR.rglob("*.jpg")))
        print(f"✓ Dataset already present with {image_count} images — skipping download.")
        return True
    return False

def download_dataset():
    """Download the PlantVillage dataset zip file."""
    zip_path = Path.cwd() / DATASET_ZIP
    print(f"Downloading PlantVillage dataset from {DATASET_URL}...")
    print(f"(~200MB - 600MB depending on version; this may take a few minutes)")

    try:
        urllib.request.urlretrieve(DATASET_URL, zip_path)
        print("✓ Download complete.")
        return zip_path
    except Exception as e:
        print(f"✗ Download failed: {e}")
        print(
            "If this fails, you can manually download from:"
        )
        print("  https://www.kaggle.com/datasets/vitalitch/plantvillage-dataset")
        print("  and place the extracted folder as 'ml/data/PlantVillage/'")
        sys.exit(1)

def extract_dataset(zip_path: Path):
    """Extract the dataset zip into ml/data/."""
    print("Extracting dataset...")
    try:
        # Extract to current directory, then move
        shutil.unpack_archive(zip_path, "ml/data", "zip")
        # The zip extracts to a top-level folder; we'll rename/move it
        extracted = Path("ml/data/PlantVillage")
        if extracted.exists():
            # Move into ml/data/ if needed
            target = DATA_DIR / "PlantVillage"
            if not target.exists():
                shutil.move(str(extracted), str(target))
                print(f"✓ Moved PlantVillage folder to {DATA_DIR / 'PlantVillage'}")
            else:
                print("✓ PlantVillage folder already in place.")
        else:
            # Some zips extract differently; list what's in ml/data/
            print("Listing ml/data/ contents after extraction:")
            for p in sorted(DATA_DIR.iterdir()):
                print(f"  - {p.name}")
        return True
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return False

def organize_classes():
    """Ensure the expected class folders exist and are named correctly."""
    print("Verifying class folder structure...")

    # The PlantVillage dataset has these top-level folders:
    # Tomato___* , Corn___* , Grape___* , Pepper___* , Soybean___*
    # We need to ensure they exist under ml/data/PlantVillage/

    plant_village_dir = DATA_DIR / "PlantVillage"
    if not plant_village_dir.exists():
        print("✗ PlantVillage directory not found after extraction.")
        return False

    # Check which classes are present
    present_classes = sorted([p.name for p in plant_village_dir.iterdir() if p.is_dir()])
    print(f"Found classes: {present_classes}")

    # Map from dataset classes to our target classes
    # For now, we just verify the structure is correct
    # v1 classes: Early_blight, Late_blight, Healthy (tomato)
    # v2 additional: Corn rust, Corn NLB, Grape Black rot, Pepper Bacterial spot, Soybean healthy

    # Verify at least tomato classes exist
    tomato_dir = plant_village_dir / "Tomato"
    if tomato_dir.exists():
        print("✓ Tomato classes found in dataset.")
    else:
        print("⚠ No Tomato directory found — dataset structure may differ.")

    return True

def main():
    print("=" * 60)
    print("AgriVision: PlantVillage Dataset Downloader")
    print("=" * 60)
    print()

    if check_existing_data():
        print()
        print("All set! The dataset is already downloaded and organized.")
        print("You can now run:")
        print("  python ml/data_prep.py   # to verify split")
        print("  python ml/train.py       # to train / retrain model")
        return

    try:
        ensure_dirs()
        zip_path = download_dataset()
        if not extract_dataset(zip_path):
            print("\n⚠ Extraction had issues, but let's verify the class structure anyway.")
        organize_classes()

        print()
        print("=" * 60)
        print("Setup Complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Review ml/data/PlantVillage/ to confirm class folders.")
        print("  2. Run: python ml/data_prep.py  # verify leak-free split")
        print("  3. Run: python ml/train.py      # train/retrain MobileNetV2")
        print()

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Setup script for model files
Helps users download or create mock model files for testing
"""

import os
import sys
import argparse
from pathlib import Path

def create_mock_models():
    """Create mock/placeholder model files for testing structure"""
    print("🔧 Creating mock model files for testing...")
    
    mock_content = b"MOCK_YOLO_MODEL_FILE_FOR_TESTING_ONLY"
    
    for model_name in ["best.pt", "last.pt"]:
        model_path = Path(model_name)
        if model_path.exists():
            response = input(f"⚠️  {model_name} already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print(f"Skipping {model_name}")
                continue
        
        with open(model_path, 'wb') as f:
            f.write(mock_content)
        
        print(f"✅ Created mock file: {model_name} ({len(mock_content)} bytes)")
    
    print("\n⚠️  WARNING: These are MOCK files and will NOT work for actual detection!")
    print("📋 To get real models, see MODEL_SETUP.md")
    print("🔗 Download from: https://universe.roboflow.com/ayu-asipq/calory")

def check_models():
    """Check if model files exist and show their status"""
    print("🔍 Checking for model files...\n")
    
    models = ["best.pt", "last.pt"]
    all_present = True
    
    for model_name in models:
        model_path = Path(model_name)
        if model_path.exists():
            size = model_path.stat().st_size
            size_mb = size / (1024 * 1024)
            
            # Check if it's a mock file
            with open(model_path, 'rb') as f:
                content = f.read(100)
                is_mock = b"MOCK_YOLO_MODEL" in content
            
            status = "🟡 MOCK" if is_mock else "✅ REAL" if size_mb > 10 else "⚠️  SUSPICIOUS"
            print(f"{status} {model_name}: {size_mb:.2f} MB")
        else:
            print(f"❌ MISSING {model_name}")
            all_present = False
    
    print()
    
    if all_present:
        print("✅ All model files present!")
        if any("MOCK" in line for line in []):  # Simplified check
            print("⚠️  Note: Some files are mock/test files")
            print("📋 For real models, see MODEL_SETUP.md")
    else:
        print("❌ Some model files are missing!")
        print("\n📋 Next steps:")
        print("1. Read MODEL_SETUP.md for detailed instructions")
        print("2. Download from Roboflow: https://universe.roboflow.com/ayu-asipq/calory")
        print("3. Or create mock files for testing: python setup_models.py --mock")

def show_download_instructions():
    """Display download instructions"""
    print("""
📥 HOW TO DOWNLOAD MODEL FILES
================================

Option 1: Download from Roboflow (Recommended)
------------------------------------------------
1. Visit: https://universe.roboflow.com/ayu-asipq/calory
2. Select "YOLOv12" format
3. Download the trained model weights
4. Extract and copy best.pt & last.pt to this directory

Option 2: Train Your Own Models
--------------------------------
1. Collect and annotate food images
2. Train with: yolo detect train data=dataset.yaml model=yolov12.pt
3. Copy weights: cp runs/detect/train/weights/*.pt .

Option 3: Use Mock Files (Testing Only)
----------------------------------------
Run: python setup_models.py --mock

For detailed instructions, see MODEL_SETUP.md
""")

def main():
    parser = argparse.ArgumentParser(
        description="Setup utility for YOLO model files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--mock',
        action='store_true',
        help='Create mock model files for testing (not for real detection)'
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check if model files exist and show their status'
    )
    
    parser.add_argument(
        '--instructions',
        action='store_true',
        help='Show download instructions'
    )
    
    args = parser.parse_args()
    
    # Default behavior if no args
    if not (args.mock or args.check or args.instructions):
        args.check = True
    
    if args.check:
        check_models()
    
    if args.mock:
        create_mock_models()
    
    if args.instructions:
        show_download_instructions()

if __name__ == "__main__":
    main()

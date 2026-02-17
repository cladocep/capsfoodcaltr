# Model Files Setup Guide

## ⚠️ Important: Model Files Required

The application **requires** two YOLO model files to function:
- `best.pt` - Best performing model weights
- `last.pt` - Last checkpoint model weights

These files are **NOT included** in the git repository due to their large size (removed during history cleanup - see `HISTORY_CLEANUP.md`).

## Why Are They Missing?

The model files were removed from git history in commit cleanup because:
1. Large files (hundreds of MB each) bloat the repository
2. They were accidentally committed with 1,977 other files
3. Git is not designed for large binary files
4. It's better practice to distribute models separately

## 🚀 How to Get the Model Files

### Option 1: Download from Roboflow (Recommended)

The models were trained using a dataset from Roboflow. Follow these steps:

1. **Visit the Roboflow Project:**
   ```
   https://universe.roboflow.com/ayu-asipq/calory
   ```

2. **Download the Dataset:**
   - Select "YOLOv12" format
   - Download the trained model weights
   - Look for `best.pt` and `last.pt` files in the export

3. **Place Files in Project Root:**
   ```bash
   # Copy the model files to your project directory
   cp /path/to/downloaded/best.pt /home/runner/work/capsfoodcaltr/capsfoodcaltr/
   cp /path/to/downloaded/last.pt /home/runner/work/capsfoodcaltr/capsfoodcaltr/
   ```

### Option 2: Train Your Own Models

If you want to train custom models:

1. **Prepare Dataset:**
   - Collect food images (Indonesian foods)
   - Annotate with bounding boxes
   - Use Roboflow or CVAT for labeling

2. **Train with YOLOv12:**
   ```bash
   # Install ultralytics
   pip install ultralytics
   
   # Train the model
   yolo detect train data=dataset.yaml model=yolov12.pt epochs=100
   
   # The trained models will be in runs/detect/train/weights/
   cp runs/detect/train/weights/best.pt .
   cp runs/detect/train/weights/last.pt .
   ```

### Option 3: Use Mock Files for Testing (Development Only)

If you just want to test the application structure without actual detection:

```bash
# This will be provided by setup_models.py script
python setup_models.py --mock
```

## 📋 Verification

After placing the model files, verify they're in the correct location:

```bash
# Check files exist
ls -lh best.pt last.pt

# Expected output:
# -rw-r--r-- 1 user user 200M Jan 01 12:00 best.pt
# -rw-r--r-- 1 user user 195M Jan 01 12:00 last.pt
```

Then try running the application:

```bash
streamlit run app.py
```

The sidebar should show "Model loaded: best.pt" without errors.

## 🔒 Git Configuration

The `.gitignore` file is configured to:
- **Ignore** all `*.pt` files by default
- **Allow** `best.pt` and `last.pt` as exceptions (lines 3-4)

This means:
- ✅ You can commit `best.pt` and `last.pt` if needed
- ❌ Other `.pt` files won't be tracked
- ⚠️ Be cautious: large files slow down git operations

### Should You Commit Model Files?

**Recommendation: NO** - Keep them out of git

**Why:**
- Large files (200MB+ each) bloat the repository
- Slow clone/push operations
- Git is not designed for binary files
- Use Git LFS if you must version control them

**Alternative:**
- Store on cloud storage (Google Drive, S3)
- Use Git LFS for version control
- Distribute via releases
- Keep them local only

## 🆘 Troubleshooting

### Error: "File 'best.pt' not found!"

**Solution:** 
```bash
# Check if files exist
ls -lh *.pt

# If missing, download from Roboflow (Option 1 above)
```

### Error: "Model loading failed"

**Possible causes:**
1. File is corrupted - re-download
2. Wrong YOLO version - ensure YOLOv12 format
3. File permissions - check with `ls -lh`

**Solution:**
```bash
# Verify file integrity
file best.pt  # Should show: "data"

# Check file size (should be 100MB+)
du -h best.pt last.pt
```

### Error: "CUDA/GPU issues"

**Solution:**
```bash
# Run on CPU instead
# The app will automatically use CPU if GPU unavailable
# Check ultralytics installation: pip install ultralytics
```

## 📚 Additional Resources

- **YOLOv12 Documentation:** https://docs.ultralytics.com/
- **Roboflow Universe:** https://universe.roboflow.com/
- **Training Custom Models:** https://docs.ultralytics.com/modes/train/
- **Git LFS:** https://git-lfs.github.com/ (for version controlling large files)

## 📞 Support

If you continue to have issues:

1. Check `app.log` for detailed error messages
2. Verify Python dependencies: `pip install -r requirements.txt`
3. Ensure you have enough disk space (need ~500MB for models)
4. Review `HISTORY_CLEANUP.md` to understand why files were removed

---

**Remember:** Model files are essential for the application to work. Without them, you'll only be able to use the manual meal entry feature.

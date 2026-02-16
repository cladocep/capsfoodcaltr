# Food Calorie Tracker

An intelligent food detection and calorie tracking application using YOLOv12 deep learning model and Streamlit web framework.

## Features

- ✅ **Real-time Food Detection** - Automatic detection of 13 Indonesian food types using YOLO
- ✅ **Calorie Calculation** - Pre-loaded calorie database for common foods
- ✅ **Manual Entry** - Add meals without photos
- ✅ **Data Export** - Download meal history as CSV with timestamp
- ✅ **Input Validation** - Sanitize and validate all user inputs
- ✅ **Comprehensive Logging** - Track all application events
- ✅ **Configuration Management** - Easy config via YAML file

## Supported Food Items

The model can detect 13 Indonesian food categories:
- Ayam Goreng (Fried Chicken)
- Capcay (Mixed Vegetables)
- Nasi (Rice)
- Sayur Bayam (Spinach)
- Sayur Kangkung (Water Spinach)
- Sayur Sop (Vegetable Soup)
- Tahu (Tofu)
- Telur Dadar (Scrambled Eggs)
- Telur Mata Sapi (Sunny Side Up Eggs)
- Telur Rebus (Boiled Eggs)
- Tempe (Tempeh)
- Tumis Buncis (Stir-fried Green Beans)
- Food-z7P4 (Generic Food)

## Installation

### Requirements
- Python 3.8+
- pip or conda

### Setup

1. **Clone/Download the project**
```bash
cd caps4
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download pre-trained model**
The model files (best.pt, last.pt) are not included in repository due to size.

**Option A: Download from Roboflow** (Recommended)
```bash
# Go to: https://universe.roboflow.com/ayu-asipq/calory
# Download the dataset in YOLOv12 format
# Extract and copy [best.pt](http://_vscodecontentref_/1) & [last.pt](http://_vscodecontentref_/2) to project directory

## Running the Application

```bash
streamlit run app.py
```
The app will open at `http://localhost:8501`

## Testing

### Run Unit Tests
```bash
pytest test_app.py -v
```

### Test Coverage
- Input validation (meal name, calories, image)
- Edge cases and boundary values
- Error handling

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── config.yaml           # Configuration file
├── validators.py         # Input validation functions
├── test_app.py          # Unit tests
├── requirements.txt     # Python dependencies
├── best.pt             # Trained YOLOv12 model (best weights)
├── last.pt             # Trained YOLOv12 model (last checkpoint)
├── app.log             # Application logs
└── README.md           # This file
```

## Configuration

Edit `config.yaml` to customize:
- Model paths
- Confidence thresholds
- Logging level and file
- Download options

Example:
```yaml
model:
  best_model_path: "best.pt"
  default_confidence: 0.25

logging:
  level: "INFO"
  file: "app.log"
```

## How It Works

### Workflow
1. **Upload Image** - User uploads meal photo (JPG/PNG)
2. **Detect** - YOLO identifies food items with bounding boxes
3. **Review** - Model displays detections in table with confidence scores
4. **Confirm** - User can edit food names and calorie values
5. **Track** - Meals added to session and displayed with total calories
6. **Export** - Download data as CSV file

### Model Architecture
- **Framework**: YOLOv12 (Object Detection)
- **Training Dataset**: 974 images from Roboflow
- **Input Size**: 640x640 pixels
- **Output**: Bounding boxes + class predictions + confidence scores

## 🔍 Logging

All events logged to `app.log`:
- Model loading
- Image processing
- Detections
- User inputs
- Errors and warnings

View logs:
```bash
tail -f app.log
```

## Known Limitations

- Only detects 13 food categories (Indonesian foods)
- Accuracy depends on image quality and angle
- Confidence threshold may need adjustment per image
- Limited training data (974 images)
- session-only

## Performance Metrics

- **Inference Time**: ~155ms per image
- **Supported Batch Size**: 1 image at a time
- **Memory Usage**: ~2-3GB


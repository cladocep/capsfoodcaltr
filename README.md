# 🍽️ Food Calorie Tracker

An intelligent food detection and calorie tracking application using YOLOv12 deep learning model and Streamlit web framework.

> ⚠️ **IMPORTANT**: This application requires model files (`best.pt` and `last.pt`) that are **NOT included** in the repository.  
> 📋 **See [MODEL_SETUP.md](MODEL_SETUP.md) for download instructions** before running the app.

## 📋 Features

- ✅ **Real-time Food Detection** - Automatic detection of 13 Indonesian food types using YOLO
- ✅ **Calorie Calculation** - Pre-loaded calorie database for common foods
- ✅ **Manual Entry** - Add meals without photos
- ✅ **Data Export** - Download meal history as CSV with timestamp
- ✅ **Input Validation** - Sanitize and validate all user inputs
- ✅ **Comprehensive Logging** - Track all application events
- ✅ **Configuration Management** - Easy config via YAML file

## 🎯 Supported Food Items

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

## 🚀 Installation

### Requirements
- Python 3.8+
- pip or conda

### Setup

1. **Clone/Download the project**
```bash
git clone https://github.com/cladocep/capsfoodcaltr.git
cd capsfoodcaltr
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **🔴 REQUIRED: Download Model Files**

The app **requires** `best.pt` and `last.pt` to work. These files are NOT in the repository.

**Quick Setup:**
```bash
# Check if models are present
python setup_models.py --check

# Option A: Download from Roboflow (Recommended)
# Visit: https://universe.roboflow.com/ayu-asipq/calory
# Download YOLOv12 format and place best.pt & last.pt in project root

# Option B: Create mock files for testing (won't detect food)
python setup_models.py --mock
```

**📖 For detailed instructions, see [MODEL_SETUP.md](MODEL_SETUP.md)**

> **Why are they missing?** Model files were removed during git history cleanup (see `HISTORY_CLEANUP.md`).  
> Large binary files (200MB+ each) don't belong in git repositories.

## 🏃 Running the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🧪 Testing

### Run Unit Tests
```bash
pytest test_app.py -v
```

### Test Coverage
- Input validation (meal name, calories, image)
- Edge cases and boundary values
- Error handling

## 📁 Project Structure

```
.
├── app.py                    # Main Streamlit application
├── config.yaml              # Configuration file
├── validators.py            # Input validation functions
├── food_validators.py       # Food-specific validation
├── test_app.py             # Unit tests
├── requirements.txt        # Python dependencies
├── packages.txt            # System packages
├── .gitignore             # Git ignore patterns
├── .gitattributes         # Git file handling rules
├── best.pt                # Trained YOLOv12 model (download separately)
├── last.pt                # Trained YOLOv12 model (download separately)
├── app.log                # Application logs (gitignored)
├── HISTORY_CLEANUP.md     # Git history cleanup documentation
├── README.md              # This file
└── READMEcal.md          # Additional documentation
```

## ⚙️ Configuration

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

## 📊 How It Works

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

## ⚠️ Known Limitations

- Only detects 13 food categories (Indonesian foods)
- Accuracy depends on image quality and angle
- Confidence threshold may need adjustment per image
- Limited training data (974 images)
- No historical data persistence (session-only)

## 🔮 Future Enhancements

- [ ] Database integration for meal history
- [ ] User authentication system
- [ ] Data augmentation for improved model
- [ ] Nutritional info (protein, carbs, fats)
- [ ] Mobile app version
- [ ] Integration with fitness apps (MyFitnessPal)
- [ ] Multi-language support
- [ ] Export to PDF/Excel

## 📝 Input Validation Rules

### Meal Name
- Cannot be empty
- Max 100 characters
- Only alphanumeric, space, dash, comma

### Calories
- Must be numeric
- Cannot be negative
- Must be greater than 0
- Max 5000 kcal

### Image
- Max 10MB file size
- Supported: JPG, PNG
- Must be a valid image file

## 🐛 Troubleshooting

### Model Not Loading
```
Error: File 'best.pt' not found!
```
→ Ensure model files are in project directory

### No Detections Found
→ Try lowering confidence threshold (0.1-0.25)

### Image Upload Error
→ Check file size (<10MB) and format (JPG/PNG)

## 📈 Performance Metrics

- **Inference Time**: ~155ms per image
- **Supported Batch Size**: 1 image at a time
- **Memory Usage**: ~2-3GB

## 📜 License

Project for educational purposes. Dataset from Roboflow.

## 👨‍💻 Author

Created for Food Calorie Tracking capstone project.

## 📧 Support

For issues or questions, check the logs in `app.log` for detailed error information.

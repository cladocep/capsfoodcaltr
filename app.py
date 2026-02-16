import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import os
import csv
import yaml
import logging
from io import StringIO
from datetime import datetime
from pathlib import Path
from food_validators import validate_meal_name, validate_calories

# =====================================
# Configuration & Logging Setup
# =====================================
def setup_logging(config):
    """Setup logging from config"""
    log_level = getattr(logging, config["logging"]["level"])
    log_format = config["logging"]["format"]
    log_file = config["logging"]["file"]
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Load config
config_path = Path(__file__).parent / "config.yaml"
with open(config_path) as f:
    CONFIG = yaml.safe_load(f)

logger = setup_logging(CONFIG)
logger.info("Application started")

# =====================================
# Model Loading with Caching
# =====================================
@st.cache_resource
def load_model(model_choice):
    """Load YOLO model from local files"""
    model_path = CONFIG["model"]["best_model_path"] if model_choice == "Best Model (best.pt)" else CONFIG["model"]["last_model_path"]
    
    try:
        logger.info(f"Loading model: {model_path}")
        st.sidebar.write(f"Loading: {model_path}...")
        
        if not os.path.exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            st.sidebar.error(f"Error: File '{model_path}' not found!")
            return None
        
        model = YOLO(model_path)
        logger.info(f"Model loaded successfully: {model_path}")
        st.sidebar.success(f"Model loaded: {model_path}")
        return model
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}", exc_info=True)
        st.sidebar.error(f"Error: {str(e)[:100]}")
        return None

# =====================================
# Food Calories Dictionary
# =====================================
FOOD_CALORIES = {
    "ayam goreng": 260,
    "capcay": 67,
    "nasi": 129,
    "sayur bayam": 36,
    "sayur kangkung": 98,
    "sayur sop": 22,
    "tahu": 80,
    "telur dadar": 93,
    "telur mata sapi": 110,
    "telur rebus": 78,
    "tempe": 225,
    "tumis buncis": 65,
    "food-z7p4": 100,
    "food": 100,
    "telur": 70, "egg": 70,
    "sandwich": 250, "bread": 80,
    "kangkung": 25,
    "ayam": 165, "chicken": 165,
    "ikan": 100, "fish": 100,
    "sayur": 30, "vegetable": 30,
    "buah": 50, "fruit": 50,
}

# =====================================
# Page Setup
# =====================================
st.set_page_config(
    page_title=CONFIG["app"]["title"],
    layout=CONFIG["app"]["page_layout"]
)
st.title("Food Calorie Tracker")
st.write("Track your daily calorie intake by uploading meal images.")

if "meals" not in st.session_state:
    st.session_state.meals = []

# =====================================
# Model Selection
# =====================================
with st.sidebar:
    st.subheader("Model Settings")
    model_choice = st.radio(
        "Select YOLO Model:",
        ["Best Model (best.pt)", "Last Model (last.pt)"],
        index=0,
    )

model = load_model(model_choice)

# =====================================
# Main App - Image Upload & Detection
# =====================================
st.subheader("Upload Meal Image")
img_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if img_file and model:
    logger.info(f"Image uploaded: {img_file.name}")
    
    img = Image.open(img_file).convert("RGB")
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(img, caption="Original Image", use_container_width=True)
    
    conf_threshold = st.slider(
        "Confidence Threshold",
        min_value=CONFIG["detection"]["min_confidence"],
        max_value=CONFIG["detection"]["max_confidence"],
        value=CONFIG["model"]["default_confidence"],
        step=CONFIG["model"]["confidence_step"]
    )
    
    img_array = np.array(img)
    with st.spinner("Detecting food..."):
        logger.info(f"Running detection with confidence: {conf_threshold}")
        results = model.predict(img_array, conf=conf_threshold, verbose=False)
    
    if results and len(results) > 0:
        r = results[0]
        boxes = r.boxes
        class_names_raw = r.names or {}
        
        class_names = {}
        for class_id, name in class_names_raw.items():
            clean_name = name.split('-')[0].strip().lower()
            class_names[class_id] = clean_name
        
        detection_count = len(boxes)
        logger.info(f"Detection complete: {detection_count} items found")
        st.write(f"**Found {detection_count} detections**")
        
        with col2:
            try:
                annotated = r.plot()
                if annotated is not None:
                    annotated_rgb = annotated[:, :, ::-1]
                    st.image(annotated_rgb, caption="Detection Result", use_container_width=True)
                    st.success(f"Detected {detection_count} food items")
                else:
                    st.error("Failed to generate plot")
            except Exception as e:
                logger.error(f"Error generating plot: {str(e)}")
                st.error(f"Error: {str(e)}")
        
        st.write("**Detected Items:**")
        detected_data = []
        for idx, box in enumerate(boxes):
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            detected_data.append({
                "Item": idx + 1,
                "Class": class_names.get(class_id, f"Class {class_id}"),
                "Confidence": f"{confidence:.2%}"
            })
        st.dataframe(detected_data, hide_index=True)
        
        st.subheader("Add to Meals")
        for idx, box in enumerate(boxes):
            class_id = int(box.cls[0])
            class_name = class_names.get(class_id, f"Class {class_id}")
            default_calories = FOOD_CALORIES.get(class_name.lower(), 100)
            
            col_a, col_b, col_c = st.columns([2, 1, 1])
            
            with col_a:
                food_name = st.text_input(
                    "Food name",
                    value=class_name,
                    key=f"name_{idx}",
                    label_visibility="collapsed"
                )
            
            with col_b:
                calories = st.number_input(
                    "Calories",
                    value=default_calories,
                    min_value=0,
                    step=10,
                    key=f"cal_{idx}",
                    label_visibility="collapsed"
                )
            
            with col_c:
                if st.button("Add", key=f"btn_{idx}"):
                    st.session_state.meals.append({
                        "name": food_name,
                        "calories": int(calories)
                    })
                    logger.info(f"Added meal: {food_name} ({calories} kcal)")
                    st.rerun()
    else:
        logger.warning(f"No detections found with confidence threshold: {conf_threshold}")
        st.warning("No detections found. Try lowering the confidence threshold.")

elif img_file and not model:
    st.error("Model not loaded")

# =====================================
# Manual Meal Entry
# =====================================
st.subheader("Add Meal Manually")
with st.form("manual_form"):
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        meal_name = st.text_input("Meal name")
    with col2:
        meal_calories = st.number_input("Calories", min_value=0, value=100)
    with col3:
        st.write("")
        submitted = st.form_submit_button("Add")
    
    if submitted and meal_name:
        valid_name, msg_name = validate_meal_name(meal_name)
        valid_cal, msg_cal = validate_calories(meal_calories)
        
        if valid_name and valid_cal:
            st.session_state.meals.append({
                "name": meal_name.strip(),
                "calories": int(meal_calories)
            })
            logger.info(f"Manual meal added: {meal_name} ({meal_calories} kcal)")
            st.success("Added!")
        else:
            if not valid_name:
                st.error(msg_name)
            if not valid_cal:
                st.error(msg_cal)

# =====================================
# Display Meals & Download
# =====================================
st.subheader("Today's Meals")

if st.session_state.meals:
    meal_data = []
    total = 0
    for meal in st.session_state.meals:
        meal_data.append({
            "Meal": meal["name"],
            "Calories": meal["calories"]
        })
        total += meal["calories"]
    
    st.dataframe(meal_data, hide_index=True)
    st.metric("Total Calories", total)
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if CONFIG["download"]["csv_enabled"]:
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(["Meal", "Calories"])
            for meal in st.session_state.meals:
                csv_writer.writerow([meal["name"], meal["calories"]])
            
            if CONFIG["download"]["include_total"]:
                csv_writer.writerow(["", ""])
                csv_writer.writerow(["Total", total])
            
            csv_data = csv_buffer.getvalue()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"meals_{timestamp}.csv"
            
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv"
            )
    
    if st.button("Clear All"):
        st.session_state.meals = []
        st.rerun()
else:
    st.info("No meals added yet")

logger.info("Application render complete")

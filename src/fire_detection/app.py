import streamlit as st
import io
import os
import cv2
import utils
from main import CONFIG_FILE_PATH
from main import FireDetector


fire_detector = FireDetector()

st.title("Fire Detection")
FIRE_DETECT_DIR_NAME = "fire_detect"
os.makedirs(FIRE_DETECT_DIR_NAME,exist_ok=True)

uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])
temporary_location = False

if uploaded_file is not None:
    g = io.BytesIO(uploaded_file.read())  ## BytesIO Object
    temporary_location = os.path.join(FIRE_DETECT_DIR_NAME,utils.read_yaml(CONFIG_FILE_PATH).get("fire_detect").get("input_video_path"))

    with open(temporary_location, 'wb') as out:  ## Open temporary file as bytes
        out.write(g.read())  ## Read bytes into file


if st.button("Detect Fire"):
    fire_detector.combine_all()
    print("fire detection done")
        
"""
Configuration file

Author: zmingen
"""
import os

# Send detection result to this URL
detection_api = os.getenv("PPE_DETECTION_URL", "http://localhost:8080/v1/detections")

# Message sending interval, time unit is millisecond
message_send_interval = int(os.getenv("PPE_MESSAGE_SEND_INTERVAL", 1000))

# Object confidence threshold, if the object confidence smaller than threshold, it will be filtered out
object_confidence_threshold = float(os.getenv("PPE_OBJECT_CONFIDENCE_THRESHOLD", .5))

# Capture Image Size, Allowed Resolution:(640, 480), (1280, 720), (1920, 1080)
supported_video_resolution = [(640, 480), (1280, 720), (1920, 1080)]
capture_image_width = int(os.getenv("PPE_CAPTURE_IMAGE_WIDTH", 1280))
capture_image_height = int(os.getenv("PPE_CAPTURE_IMAGE_HEIGHT", 720))

# Display Window Size
display_full_screen = os.getenv("PPE_DISPLAY_FULL_SCREEN", "True").lower() == "true"
display_window_width = int(os.getenv("PPE_DISPLAY_WINDOW_WIDTH", 1280))
display_window_height = int(os.getenv("PPE_DISPLAY_WINDOW_HEIGHT", 720))

# Image Size of Storage
storage_image_width = int(os.getenv("PPE_STORAGE_IMAGE_WIDTH", 640))
storage_image_height = int(os.getenv("PPE_STORAGE_IMAGE_HEIGHT", 360))

# Input Type, ["camera", "file"]
input_type = os.getenv("PPE_INPUT_TYPE", "file")



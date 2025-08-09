import os

API_BASE_URL = os.getenv("API_BASE_URL", "https://proper-cricket-wholly.ngrok-free.app")
NOTIFICATION_URL = os.getenv("NOTIFICATION_URL", f"{API_BASE_URL.rstrip('/')}/notify/")

PREDICT_BASE_URL = os.getenv("PREDICT_BASE_URL", "http://127.0.0.1:5555")
PREDICT_URL = os.getenv("PREDICT_URL", f"{PREDICT_BASE_URL.rstrip('/')}/predict")

PREDICT_TIMEOUT = float(os.getenv("PREDICT_TIMEOUT", "3.0"))
FRAME_QUEUE_SIZE = int(os.getenv("FRAME_QUEUE_SIZE", "5"))
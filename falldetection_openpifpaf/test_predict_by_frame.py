import cv2
import requests
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from config import PREDICT_URL

video_path = "input/50waystofall.mp4"

cap = cv2.VideoCapture(video_path)

frame_count = 0

print(f"Reading video from: {video_path}")
print(f"Total frames: {frame_count}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Optional: Skip frames for faster testing
    if frame_count % 5 != 0:
        frame_count += 1
        continue

    _, img_encoded = cv2.imencode('.jpg', frame)
    response = requests.post(
        PREDICT_URL,
        files={"image": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")}
    )

    try:
        print(f"Frame {frame_count}: {response.json()}")
    except Exception as e:
        print(f"Frame {frame_count}: Error parsing response ->", e)

    frame_count += 1

cap.release()

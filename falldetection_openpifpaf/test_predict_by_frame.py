import cv2
import requests

video_path = "input/50waystofall.mp4"
predict_url = "http://127.0.0.1:5555/predict"

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
        predict_url,
        files={"image": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")}
    )

    try:
        print(f"Frame {frame_count}: {response.json()}")
    except Exception as e:
        print(f"Frame {frame_count}: Error parsing response ->", e)

    frame_count += 1

cap.release()

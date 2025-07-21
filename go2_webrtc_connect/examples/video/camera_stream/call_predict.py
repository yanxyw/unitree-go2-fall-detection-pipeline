import cv2
import asyncio
import logging
import threading
import time
import requests
import numpy as np
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from aiortc import MediaStreamTrack

PREDICT_URL = "http://localhost:5555/predict"

def send_to_fall_detector(frame):
    try:
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post(
            PREDICT_URL,
            files={"image": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")},
            timeout=1.5
        )
        response.raise_for_status()
        fall_count = response.json().get("fall_count", None)
        print(f"Fall Count: {fall_count}")
    except Exception as e:
        print(f"Prediction error: {e}")

def main():
    logging.basicConfig(level=logging.FATAL)
    conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalAP)

    async def recv_camera_stream(track: MediaStreamTrack):
        while True:
            frame = await track.recv()
            img = frame.to_ndarray(format="bgr24")
            img = cv2.resize(img, (640, 480))  # Resize for performance
            threading.Thread(target=send_to_fall_detector, args=(img,)).start()

    def run_asyncio_loop(loop):
        asyncio.set_event_loop(loop)
        async def setup():
            try:
                await conn.connect()
                conn.video.switchVideoChannel(True)
                conn.video.add_track_callback(recv_camera_stream)
            except Exception as e:
                logging.error(f"WebRTC error: {e}")
        loop.run_until_complete(setup())
        loop.run_forever()

    loop = asyncio.new_event_loop()
    threading.Thread(target=run_asyncio_loop, args=(loop,), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        loop.call_soon_threadsafe(loop.stop)

if __name__ == "__main__":
    main()

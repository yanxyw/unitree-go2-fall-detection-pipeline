import cv2
import asyncio
import logging
import threading
import time
import requests
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from aiortc import MediaStreamTrack
from collections import deque
from queue import Queue, Empty

PREDICT_URL = "http://localhost:5555/predict"

# FPS tracking
fps_deque = deque(maxlen=30)
last_fps_print = time.time()

# Frame queue to avoid spawning too many threads
frame_queue = Queue(maxsize=5)

def fall_detection_worker():
    global last_fps_print
    while True:
        try:
            frame = frame_queue.get(timeout=1)
        except Empty:
            continue

        try:
            start = time.time()
            _, img_encoded = cv2.imencode('.jpg', frame)
            response = requests.post(
                PREDICT_URL,
                files={"image": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")},
                timeout=2.0
            )
            duration = time.time() - start
            response.raise_for_status()

            data = response.json()
            fall_count = data.get("fall_count", None)
            print(f"✅ Fall Count: {fall_count} | ⏱️ Predict time: {duration:.3f}s")

            # FPS tracking
            fps_deque.append(time.time())
            if time.time() - last_fps_print >= 1.0:
                if len(fps_deque) >= 2:
                    time_diffs = [t2 - t1 for t1, t2 in zip(fps_deque, list(fps_deque)[1:])]
                    avg_frame_time = sum(time_diffs) / len(time_diffs)
                    fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
                    print(f"📷 Approx FPS: {fps:.2f}")
                last_fps_print = time.time()

        except Exception as e:
            print(f"❌ Prediction error: {e}")


def main():
    logging.basicConfig(level=logging.FATAL)
    conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalAP)

    # Start a single prediction worker thread
    threading.Thread(target=fall_detection_worker, daemon=True).start()

    async def recv_camera_stream(track: MediaStreamTrack):
        while True:
            frame = await track.recv()
            img = frame.to_ndarray(format="bgr24")
            img = cv2.resize(img, (640, 480))

            # Put frame into the queue if not full
            if not frame_queue.full():
                frame_queue.put(img)

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
        print("🛑 Stopping...")
        loop.call_soon_threadsafe(loop.stop)


if __name__ == "__main__":
    main()

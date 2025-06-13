import cv2
import asyncio
import logging
import threading
import time
from queue import Queue
from flask import Flask, Response
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from aiortc import MediaStreamTrack

# Global frame queue with a small buffer
frame_queue = Queue(maxsize=5)

# Flask app for MJPEG streaming
app = Flask(__name__)

@app.route('/video')
def video_feed():
    def mjpeg_stream():
        while True:
            if not frame_queue.empty():
                frame = frame_queue.get()
                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    continue
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            else:
                time.sleep(0.01)
    return Response(mjpeg_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_flask_server():
    app.run(host='0.0.0.0', port=8080, threaded=True)

# WebRTC setup
def main():
    logging.basicConfig(level=logging.FATAL)
    conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalAP)

    async def recv_camera_stream(track: MediaStreamTrack):
        while True:
            frame = await track.recv()
            img = frame.to_ndarray(format="bgr24")
            img = cv2.resize(img, (640, 480))  # Reduce size for performance
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
            time.sleep(1)  # Keep main thread alive
    except KeyboardInterrupt:
        loop.call_soon_threadsafe(loop.stop)

if __name__ == "__main__":
    threading.Thread(target=run_flask_server, daemon=True).start()
    main()

# Unitree Go2 Fall Detection Pipeline

This project implements a real-time fall detection system using the Unitree Go2 robot. It integrates live video streaming, a fall detection model, a backend API, and a mobile app to receive notifications.

---

## 1. Project Structure

The pipeline consists of four components:

### 1. `go2_webrtc_connect` — WebRTC Video Driver

A lightweight Flask server that connects to the Unitree Go2 robot, retrieves the camera feed, and exposes it as a video stream at:

```
http://localhost:8080/video
```

This module is adapted from [legion1581/go2_webrtc_connect](https://github.com/legion1581/go2_webrtc_connect).

#### Setup and Run

1. Follow the instructions in `go2_webrtc_connect/README.md` to install dependencies.
2. Then run:

    ```bash
    cd go2_webrtc_connect/examples/video/camera_stream
    python3 display_video_channel.py
    ```
    Live stream video can be accessed at `http://localhost:8080/video`.

---

### 2. `falldetection_openpifpaf` — Fall Detection Model

A fall detection system based on OpenPifPaf.

In this pipeline, it analyzes the video stream from the WebRTC driver and, when a fall is detected, sends a notification request to the backend API.

This module is adapted from [cwlroda/falldetection_openpifpaf](https://github.com/cwlroda/falldetection_openpifpaf).

#### Run the Model

```bash
python3 -m openpifpaf.video --source=http://localhost:8080/video --show --scale=0.2
```

The `--scale=0.2` argument reduces input resolution for better performance on lower-spec devices.

---

### 3. `api` — FastAPI Notification Server

A simple FastAPI backend that exposes a `/notify` endpoint. When this endpoint is called (e.g. by the fall detection model), it sends a push notification to the connected mobile device using Firebase Cloud Messaging (FCM).

#### Setup and Run

1. Follow the instructions in `api/README.md` to install dependencies.

2. Then run:
    ```bash
    uvicorn main:app --reload
    ```

    The server will start at `http://localhost:8000`.

---

### 4. `mobile` — Flutter App

A basic Flutter app that registers for FCM and listens for push notifications from the backend.


## 2. Architecture and Implementation Diagrams

### 1. System Architecture

The overall system architecture includes three major components:

- Unitree Go2 robot.
- Local/Cloud Servers — steam real-time video, handle video processing and backend logic.
- Mobile App — receives notifications when a fall is detected.

The backend and processing components can be deployed either locally or using cloud platforms like AWS, Azure, etc.

![architecrure](/assets/architecture.png)

### 2. Implementation Details

The diagram below illustrates the implementation details and data flow between components.

![implementation](/assets/implementation.png)
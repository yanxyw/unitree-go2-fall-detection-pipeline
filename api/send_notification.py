import json
import httpx
from fastapi import FastAPI, HTTPException
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from models import NotificationRequest, FCMTokenRequest
from typing import List

app = FastAPI()

# Load Firebase Service Account JSON file
SERVICE_ACCOUNT_FILE = "unitree-go2-fcm.json"

# In-memory token store for simplicity
stored_token: str | None = None

@app.post("/register-token/")
async def register_token(payload: FCMTokenRequest):
    global stored_token
    stored_token = payload.token
    print("Token registered:", stored_token)
    return {"message": "Token registered successfully"}

@app.get("/tokens/")
def get_tokens():
    return {"tokens": stored_tokens}


def get_firebase_access_token():
    """Get OAuth2 access token for Firebase Cloud Messaging (FCM) v1 API."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"],
    )
    credentials.refresh(Request())  # Refresh the token
    return credentials.token


@app.post("/notify/")
async def send_notification(request: NotificationRequest):
    if not stored_token:
        raise HTTPException(status_code=400, detail="No FCM token registered")

    access_token = get_firebase_access_token()
    FCM_ENDPOINT = f"https://fcm.googleapis.com/v1/projects/unitree-go2/messages:send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "message": {
            "token": stored_token,
            "notification": {
                "title": request.title,
                "body": request.body,
            },
        "data": {
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "title": request.title,
                "body": request.body,
            },
            "android": {
                "priority": "high",
            },
            "apns": {
                "payload": {
                    "aps": {
                        "alert": {
                            "title": request.title,
                            "body": request.body,
                        },
                        "sound": "default",
                    }
                }
            },
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(FCM_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        return {"message": "Notification sent successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

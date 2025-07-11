import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from models import NotificationRequest, FCMTokenRequest, Token
from db import get_session

router = APIRouter()

SERVICE_ACCOUNT_FILE = "unitree-go2-fcm.json"

@router.post("/register-token/")
async def register_token(payload: FCMTokenRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Token).where(Token.token == payload.token))
    existing = result.scalar_one_or_none()
    if existing:
        return {"message": "Token already registered"}

    new_token = Token(token=payload.token)
    session.add(new_token)
    await session.commit()
    return {"message": "Token registered successfully"}

@router.get("/tokens/")
async def get_tokens(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Token))
    tokens = result.scalars().all()
    return {"tokens": [t.token for t in tokens]}

def get_firebase_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"],
    )
    credentials.refresh(Request())
    return credentials.token

@router.post("/notify/")
async def send_notification(request: NotificationRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Token))
    tokens = result.scalars().all()

    if not tokens:
        raise HTTPException(status_code=400, detail="No FCM tokens registered")

    access_token = get_firebase_access_token()
    FCM_ENDPOINT = "https://fcm.googleapis.com/v1/projects/unitree-go2/messages:send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        for token in tokens:
            payload = {
                "message": {
                    "token": token.token,
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

            response = await client.post(FCM_ENDPOINT, headers=headers, json=payload)
            if response.status_code != 200:
                print(f"Failed to send to {token.token}: {response.text}")

    return {"message": "Notifications sent"}

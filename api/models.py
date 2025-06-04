from pydantic import BaseModel

class NotificationRequest(BaseModel):
    title: str
    body: str


class FCMTokenRequest(BaseModel):
    token: str
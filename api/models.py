from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Token(Base):
    __tablename__ = "fcm_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)

class NotificationRequest(BaseModel):
    title: str
    body: str
    timestamp: Optional[str] = None
    image: Optional[str] = None  # base64-encoded image

class FCMTokenRequest(BaseModel):
    token: str
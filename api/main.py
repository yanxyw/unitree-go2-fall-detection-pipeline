from typing import Union
from fastapi import FastAPI
from send_notification import app as notification_app

app = FastAPI()

app.include_router(notification_app.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

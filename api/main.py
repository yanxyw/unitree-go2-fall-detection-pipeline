from fastapi import FastAPI
from db import init_db
from send_notification import router as notification_router

app = FastAPI()
app.include_router(notification_router)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
def read_root():
    return {"Hello": "World"}

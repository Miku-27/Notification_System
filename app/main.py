from fastapi import FastAPI
from app.api.notification_router import notification_router

app = FastAPI()

app.include_router(
    router=notification_router,
    prefix="/notification",
    tags=["notification"]
)
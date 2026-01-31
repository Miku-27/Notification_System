from fastapi import APIRouter
from app.models.pydantic_models import NotificationModel
from app.services.notification_service import register_notification
from fastapi import Depends
from app.models.database import get_db

notification_router = APIRouter()

@notification_router.post("/")
async def create_notification_route(notification: NotificationModel,db=Depends(get_db)):
    response = register_notification(notification_data = notification,db=db)
    return {
        "status": response,
        "notification": notification.model_dump() 
    }

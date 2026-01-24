from fastapi import APIRouter
from app.models.pydantic_models import NotificationModel
notification_router = APIRouter()

@notification_router.post("/notifications")
async def create_notification_route(notification: NotificationModel):
    return {
        "status": "success",
        "notification": notification.model_dump()  # by_alias=True to show "from" instead of "from_"
    }

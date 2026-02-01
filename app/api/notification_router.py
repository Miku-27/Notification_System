from fastapi import APIRouter
from app.models.pydantic_models import NotificationModel
from app.services.notification_service import register_notification
from fastapi import Depends
from app.models.database import get_db
from app.dependencies import validate_api_key
from app.utils.response import make_response

notification_router = APIRouter(dependencies=[Depends(validate_api_key)])

@notification_router.post("")
async def create_notification_route(notification: NotificationModel,db=Depends(get_db)):
    response = register_notification(notification_dict = notification.model_dump(),db=db)
    
    return make_response(response)

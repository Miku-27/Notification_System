from fastapi import APIRouter
from app.models.schemas import NotificationModel,BatchNotificationModel
from app.services.notification_service import register_notification,register_batch_notification
from fastapi import Depends
from app.models.database import get_db
from app.dependencies import validate_api_key
from app.utils.response import make_response

notification_router = APIRouter(dependencies=[Depends(validate_api_key)])

@notification_router.post("")
async def create_notification_route(notification: NotificationModel,db=Depends(get_db)):
    
    if isinstance(notification,BatchNotificationModel):
        response = register_batch_notification(notification_dict = notification.model_dump(),db=db)
    else:
        response = register_notification(notification_dict = notification.model_dump(),db=db)

    return make_response(response)

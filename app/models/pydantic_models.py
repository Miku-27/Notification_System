from datetime import datetime
from typing import Literal,Annotated
from pydantic import BaseModel, Field, EmailStr,StringConstraints
from app.models.types import PriorityEnum,NotificationTypeEnum,PHONE_REGEX


class NotificationBaseModel(BaseModel):
    template:str
    payload_data:dict
    scheduled_at: datetime | None = None
    priority:str = PriorityEnum.LOW


class EmailNotificationModel(NotificationBaseModel):
    notification_type:Literal["email"]
    sender_address : EmailStr
    recipient_address : EmailStr


class SmsNotificationModel(NotificationBaseModel):
    notification_type:Literal["sms"]
    sender_address : Annotated[str,StringConstraints(pattern=PHONE_REGEX)]
    recipient_address : Annotated[str,StringConstraints(pattern=PHONE_REGEX)]
    
NotificationModel =  Annotated[EmailNotificationModel | SmsNotificationModel, Field(discriminator='notification_type')]


class EmailContentModel(BaseModel):
    subject:str
    body:str

class SmsContentModel(BaseModel):
    body:str

class TemplateModel(BaseModel):
    slug:str
    template_name:str
    template_type:Literal["email", "sms"]
    content:EmailContentModel | SmsContentModel


class indentityModel(BaseModel):
    indentity_name:str
    
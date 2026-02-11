from datetime import datetime
from typing import Literal,Annotated
from pydantic import BaseModel, Field, EmailStr,StringConstraints
from app.models.types import PriorityEnum,PHONE_REGEX
from dataclasses import dataclass

#identity model , might add more later
class identityModel(BaseModel):
    identity_name:str
    

#models for /template routes
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


#Base notification model
class NotificationBaseModel(BaseModel):
    scheduled_at: datetime | None = None
    priority:PriorityEnum = PriorityEnum.LOW

#single notification model
class EmailNotificationModel(NotificationBaseModel):
    mode:Literal["email"]

    sender_address : EmailStr
    recipient_address : list[EmailStr]
    
    template_id:str | None
    custom_template: EmailContentModel | None = None
    payload_data:dict | None = None

class SmsNotificationModel(NotificationBaseModel):
    mode:Literal["sms"]

    sender_address : Annotated[str,StringConstraints(pattern=PHONE_REGEX)]
    recipient_address : list[Annotated[str,StringConstraints(pattern=PHONE_REGEX)]]
    
    template_id:str | None
    custom_template: SmsContentModel | None = None
    payload_data:dict | None = None

#batch notification
#checks each with SingleEmailNotificationModel | SingleSmsNotificationModel so but bad performance , works for now
class BatchNotificationModel(BaseModel):
    mode:Literal['batch']
    notificaions:list[EmailNotificationModel | SmsNotificationModel]

NotificationModel = Annotated[
    
    EmailNotificationModel |
    SmsNotificationModel |
    BatchNotificationModel,    
    Field(discriminator="mode")
]


#custom template model for custom template route  
class CustomEmailModel(NotificationBaseModel):
    notification_type: Literal["email"]
    content: EmailContentModel
    sender_address: EmailStr
    recipient_address: EmailStr

class CustomSmsModel(NotificationBaseModel):
    notification_type: Literal["sms"]
    content: SmsContentModel
    sender_address: Annotated[str, StringConstraints(pattern=PHONE_REGEX)]
    recipient_address: Annotated[str, StringConstraints(pattern=PHONE_REGEX)]


#dataclass models

@dataclass(frozen=True)
class ResolvedTemplate:
    template_id: str | None
    content: dict
    is_custom: bool | None
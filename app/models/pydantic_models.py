import re
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, TypeAdapter, model_validator,HttpUrl
from app.models.types import PriorityEnum,NotificationTypeEnum
PHONE_REGEX = r"^\+[1-9]\d{7,14}$"

class NotificationModel(BaseModel):
    notification_type: NotificationTypeEnum
    sender_adderss: str
    recipient_address: str 
    template: str 
    data: dict 
    scheduled_at: datetime | None = None
    priority:str = PriorityEnum.LOW
    callback_url:HttpUrl | None = None


    @model_validator(mode="after")
    def validate_endpoints(self) -> "NotificationModel":
        if self.notification_type == NotificationTypeEnum.email:
            try:
                TypeAdapter(EmailStr).validate_python(self.sender)
                TypeAdapter(EmailStr).validate_python(self.recipient)
            except Exception:
                raise ValueError("For email, both 'to' and 'from' must be valid email addresses")

        elif self.notification_type == NotificationTypeEnum.sms:
            if not re.match(PHONE_REGEX, self.sender) and not re.match(PHONE_REGEX, self.recipient):
                raise ValueError("'to' and 'from' must be a valid phone number (+CountryCodeNumber)")
        return self
    
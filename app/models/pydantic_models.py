import re
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, TypeAdapter, model_validator,HttpUrl

PHONE_REGEX = r"^\+[1-9]\d{7,14}$"
class NotificationType(str, Enum):
    email = "email"
    sms = "sms"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class NotificationModel(BaseModel):
    type: NotificationType
    to: str
    recipient: str 
    template: str 
    data: dict 
    scheduled_at: datetime | None = None
    priority:str = Priority.LOW
    callback_url:HttpUrl | None = None


    @model_validator(mode="after")
    def validate_endpoints(self) -> "NotificationModel":
        if self.type == NotificationType.email:
            try:
                TypeAdapter(EmailStr).validate_python(self.to)
                TypeAdapter(EmailStr).validate_python(self.recipient)
            except Exception:
                raise ValueError("For email, both 'to' and 'from' must be valid email addresses")

        elif self.type == NotificationType.sms:
            if not re.match(PHONE_REGEX, self.to) and not re.match(PHONE_REGEX, self.recipient):
                raise ValueError("'to' and 'from' must be a valid phone number (+CountryCodeNumber)")
        return self
    
from enum import Enum

class PriorityEnum(str, Enum):
    LOW = "low"
    HIGH = "high"

class StatusEnum(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    ERRORED = "errored"

class NotificationTypeEnum(str, Enum):
    email = "email"
    sms = "sms"

PHONE_REGEX = r"^\+[1-9]\d{7,14}$"
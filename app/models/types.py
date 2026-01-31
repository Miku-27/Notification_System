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

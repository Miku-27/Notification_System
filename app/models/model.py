from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer,ForeignKey ,Index,Text,DateTime,Enum as PostgresEnum
from sqlalchemy.sql import func
from app.models.database import Base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.models.types import StatusEnum,PriorityEnum,NotificationTypeEnum

class NotificationTable(Base):
    __tablename__ = "notification_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False,autoincrement=True)
    sender_address:Mapped[str] = mapped_column(String(255),nullable=False)
    notification_type:Mapped[str] = mapped_column(PostgresEnum(NotificationTypeEnum,name="notification_type",create_type=True),nullable=False)
    recipient_address:Mapped[str] = mapped_column(String(255),nullable=False)
    template_id:Mapped[int | None] = mapped_column(Integer,ForeignKey("template_table.id"),nullable=True)

    custom_template:Mapped[dict | None] = mapped_column(Text,nullable=True)
    payload:Mapped[dict] =  mapped_column(JSONB,nullable=False)

    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    scheduled_at:Mapped[datetime] = mapped_column(DateTime,nullable=True)
    priority:Mapped[PriorityEnum] = mapped_column(PostgresEnum(PriorityEnum,name="priority_level",create_type=True),default=PriorityEnum.LOW)
    
    status:Mapped[StatusEnum] = mapped_column(PostgresEnum(StatusEnum,name="notification_status",create_type=True),default=StatusEnum.PENDING)
    
    # not needed right now
    # callback_url:Mapped[str] = mapped_column(String(255),nullable=True) 
    
    __table_args__ = (
        Index(
            "index_unprocessed_notification",
            priority,created_at,
            postgresql_where=status == StatusEnum.PENDING
        ),
    )

class TemplateTable(Base):
    __tablename__="template_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False,autoincrement=True)
    owner_id :Mapped[int] = mapped_column(Integer,ForeignKey("api_key_table.id"),nullable=False)
    slug:Mapped[str] = mapped_column(String(255),nullable=False)
    template_name:Mapped[str]= mapped_column(String(255),nullable=False)
    template_type:Mapped[str]=mapped_column(String(50),nullable=False)
    content:Mapped[str] = mapped_column(JSONB,nullable=False)

class ApikeyTable(Base):
    __tablename__ = "api_key_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False,autoincrement=True)
    apikey_name:Mapped[str] = mapped_column(String,nullable=False,unique=True)
    apikey_hash:Mapped[str] = mapped_column(String,nullable=False,unique=True)
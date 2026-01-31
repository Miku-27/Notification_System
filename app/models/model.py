from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String, Text,Integer,ForeignKey ,Index,text,DateTime,Enum as PostgresEnum
from app.models.database import Base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime,timezone
from app.models.types import StatusEnum,PriorityEnum,NotificationTypeEnum

class NotificationTable(Base):
    __tablename__ = "notification_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False,autoincrement=True)
    sender_address:Mapped[str] = mapped_column(String(255),nullable=False)
    notification_type:Mapped[str] = mapped_column(PostgresEnum(NotificationTypeEnum,name="notification_type",create_type=True))
    recipient_address:Mapped[str] = mapped_column(String(255),nullable=False)
    template_id:Mapped[int] = mapped_column(Integer,ForeignKey("template_table.id"),nullable=False)
    data:Mapped[dict] = mapped_column(JSONB,nullable=True)
    created_at:Mapped[datetime] = mapped_column(DateTime,default=datetime.now(timezone.utc))
    scheduled_at:Mapped[datetime] = mapped_column(DateTime,nullable=True)
    priority:Mapped[PriorityEnum] = mapped_column(PostgresEnum(PriorityEnum,name="priority_level",create_type=True),default=PriorityEnum.LOW)
    callback_url:Mapped[str] = mapped_column(String(255),nullable=True)
    status:Mapped[StatusEnum] = mapped_column(PostgresEnum(StatusEnum,name="notification_status",create_type=True),default=StatusEnum.PENDING)
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
    template_body:Mapped[str] = mapped_column(Text,nullable=False)

    subject:Mapped[str] = mapped_column(String(255),nullable=True)
    title:Mapped[str] = mapped_column(String(255),nullable=True)

class ApikeyTable(Base):
    __tablename__ = "api_key_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False,autoincrement=True)
    apikey_name:Mapped[str] = mapped_column(String,nullable=False)
    apikey_hash:Mapped[str] = mapped_column(String,nullable=False,unique=True)
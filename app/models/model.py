from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String, Text,Integer,ForeignKey ,Index,text,DateTime,Enum as PostgresEnum
from app.models.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime,timezone
from app.models.types import StatusEnum,PriorityEnum

class NotificationTable(Base):
    __tablename__ = "notification_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False,autoincrement=True)
    to:Mapped[str] = mapped_column(String(255),nullable=False)
    recipient:Mapped[str] = mapped_column(String(255),nullable=False)
    template_id:Mapped[int] = mapped_column(Integer,nullable=False)
    data:Mapped[dict] = mapped_column(JSONB,nullable=True)
    created_at:Mapped[datetime] = mapped_column(DateTime,default=datetime.now(timezone.utc))
    scheduled_at:Mapped[datetime] = mapped_column(DateTime,nullable=True)
    priority:Mapped[PriorityEnum] = mapped_column(PostgresEnum(PriorityEnum,name="priority_level",create_type=True),default=PriorityEnum.LOW)
    callback_url:Mapped[str] = mapped_column(String(255),nullable=True)
    status:Mapped[StatusEnum] = mapped_column(PostgresEnum(StatusEnum,name="notification_status",create_type=True),default=StatusEnum.PENDING)
    __table_args__ = (
        Index(
            "index_unprocessed_notification",
            "priority","created_at",
            postgresql_where=text("status = 'pending'")
        )
    )

class TemplateTable(Base):
    __tablename__="template_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False,autoincrement=True)
    slug:Mapped[str] = mapped_column(String,nullable=False)
    template_name:Mapped[str]= mapped_column(String,nullable=False)
    template_body:Mapped[str] = mapped_column(Text,nullable=False)

class ApikeyTable(Base):
    __tablename__ = "api_key_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False,autoincrement=True)
    apikey_name:Mapped[str] = mapped_column(String,nullable=False)
    apikey_hash:Mapped[str] = mapped_column(String,nullable=False,unique=True)
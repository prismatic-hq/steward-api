import uuid
from datetime import datetime

from sqlalchemy import DateTime, MetaData, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from steward_api.config import DB_SCHEMA

SOURCE_ALERT_CONSTRAINT = "uq_work_orders_source_alert_id"


class Base(DeclarativeBase):
    metadata = MetaData(schema=DB_SCHEMA)


class WorkOrder(Base):
    __tablename__ = "work_orders"
    __table_args__ = (UniqueConstraint("source_alert_id", name=SOURCE_ALERT_CONSTRAINT),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    site: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(16), default="open")
    assigned_crew: Mapped[str | None] = mapped_column(String(64))
    source_alert_id: Mapped[uuid.UUID | None]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

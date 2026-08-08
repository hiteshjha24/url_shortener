from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class URL(Base):
    __tablename__ = "urls"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    target_url: Mapped[str] = mapped_column(Text, nullable=False)
    short_code: Mapped[str] = mapped_column(String(10), unique=True, index=True, nullable=False)
    clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


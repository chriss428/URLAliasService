from datetime import datetime, timedelta, timezone
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)


class URL(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] = mapped_column(nullable=False)
    alias: Mapped[str] = mapped_column(nullable=False, unique=True)
    count: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=1),
    )

import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tgbot.models.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telega_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    language_code: Mapped[str] = mapped_column(String(7))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_bot: Mapped[bool] = mapped_column(default=False)
    orders = relationship(
        "Order", back_populates="user", lazy='selectin',
    )
    # have_premium: Mapped[bool] = mapped_column(default=False)

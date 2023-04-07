import datetime
import math
from typing import List, Union, Optional, Tuple
from sqlalchemy import DateTime, String, func, ForeignKey, select, Float, Enum, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tgbot.models.database import Base
from tgbot.schemas.enum import StatusOrder


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('products.id'), nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id')
    )
    user = relationship(
        "User", back_populates="orders"
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )
    check: Mapped[float] = mapped_column(
        Float
    )

    status: Mapped[StatusOrder] = mapped_column(Enum(StatusOrder), nullable=False)

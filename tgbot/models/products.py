import datetime
import math
from typing import List, Union, Optional, Tuple
from sqlalchemy import DateTime, String, func, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tgbot.models.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('category_products.id'), nullable=False,
    )
    category: Mapped['Category'] = relationship(
        'Category', back_populates='products', lazy='selectin',
    )
    pictures: Mapped[List['Picture']] = relationship(
        'Picture', back_populates='product', lazy='selectin',
    )
    description: Mapped[str] = mapped_column(String(150))
    commentary: Mapped[str] = mapped_column(String(150), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    def __repr__(self):
        return f'Product(id={self.id}, {self.name}, category_id{self.category_id})'

    @classmethod
    async def get_slice(
            cls,
            offset: int,
            limit: int,
            session: AsyncSession,
    ) -> List['Product']:
        to_db = select(cls).order_by(cls.id).slice(offset, limit)
        products = await session.execute(to_db)
        return products.scalars().all()

    def to_string(self):
        return f'★имя: {self.name} описание: {self.name}, штук в магазине 88\n -----\n'

    @classmethod
    async def get_str_product(cls,
                              offset: int,
                              limit: int,
                              session: AsyncSession,
                              products_str: str = '') -> Tuple[str, int]:
        products = await cls.get_slice(offset=offset, limit=limit, session=session)
        count = await cls.get_count(session=session)
        page = math.ceil(count / 15)
        print(page, 'count')
        for product in products:
            products_str += product.to_string()
        return products_str, page

    @classmethod
    async def get_count(cls,
                        session: AsyncSession):
        to_db = select(func.count()).select_from(cls)
        count = await session.scalar(to_db)
        return count


class Category(Base):
    __tablename__ = "category_products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    products: Mapped[List['Product']] = relationship(
        'Product', back_populates='category', lazy='selectin',
    )
    description: Mapped[str] = mapped_column(String(150), nullable=True)
    commentary: Mapped[str] = mapped_column(String(150), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )

    def __repr__(self):
        return f'Category(id={self.id}, name={self.name})'

    @classmethod
    async def get_slice(
            cls,
            offset: int,
            limit: int,
            session: AsyncSession,
    ) -> List['Category']:
        to_db = select(cls).order_by(cls.id).slice(offset, limit)
        categories = await session.execute(to_db)
        return categories.scalars().all()

    @classmethod
    async def get_count(cls,
                        session: AsyncSession):
        to_db = select(func.count()).select_from(cls)
        count = await session.scalar(to_db)
        return count


class Picture(Base):
    __tablename__ = "picture_products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    # path: Mapped[str] = mapped_column(String(30), unique=True)
    commentary: Mapped[str] = mapped_column(String(150), nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    product: Mapped['Product'] = relationship(
        'Product', back_populates='pictures', lazy='selectin',
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )

    def __repr__(self):
        return f'Picture(id={self.id}, {self.name}, product_id={self.product_id})'
        
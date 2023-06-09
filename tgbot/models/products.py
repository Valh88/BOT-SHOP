import datetime
import math
from typing import List, Union, Optional, Tuple
from sqlalchemy import DateTime, String, func, ForeignKey, select, Float
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tgbot.keyboards.product_inline import ProductsPaginateCBF, CategoriesPaginateCBF, ProductsCatalogPaginateCBF
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
    price: Mapped[float] = mapped_column(
        Float,
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
        return f'Product(id={self.id}, name={self.name}, category_id={self.category_id})'

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

    @classmethod
    async def get_slice_by_category_id(
            cls,
            offset: int,
            limit: int,
            category_id,
            session: AsyncSession,
    ) -> List['Product']:
        to_db = select(cls).where(cls.category_id == category_id).order_by(cls.category_id).slice(offset, limit)
        products = await session.execute(to_db)
        return products.scalars().all()

    def to_string(self):
        return f'★имя: {self.name} описание: {self.name}, штук в магазине 88\n -----\n'

    @classmethod
    async def get_str_product(cls,
                              session: AsyncSession,
                              callback_data: ProductsPaginateCBF = None,
                              products_str: str = '') -> Tuple[str, int]:
        count = await cls.get_count(session=session)
        page = math.ceil(count / 15)
        if callback_data is None:
            products = await cls.get_slice(session=session, offset=0, limit=15)
        else:
            if callback_data.current_page > page or callback_data.current_page <= 0:
                callback_data.current_page = 1
                callback_data.slice = 0
            products = await cls.get_slice(session=session,
                                           offset=callback_data.slice,
                                           limit=callback_data.slice + 15)
        for product in products:
            products_str += product.to_string()
        return products_str, page

    @classmethod
    async def get_count(cls,
                        session: AsyncSession):
        to_db = select(func.count()).select_from(cls)
        count = await session.scalar(to_db)
        return count

    @classmethod
    async def get_count_products_by_category(
            cls, session: AsyncSession, catalog_id: int
    ) -> int:
        to_db = select(func.count()).select_from(cls).where(cls.category_id == catalog_id)
        count = await session.scalar(to_db)
        return count

    @classmethod
    async def get_products_by_id_category(
            cls,
            session: AsyncSession,
            callback_data: ProductsCatalogPaginateCBF = None,
    ) -> Tuple[List['Product'], int, ProductsCatalogPaginateCBF]:
        count = await cls.get_count_products_by_category(session, callback_data.category_id)
        page = math.ceil(count / 8)
        if callback_data.current_page > page or callback_data.current_page <= 1:
            callback_data.current_page = 1
            callback_data.slice = 0
            products = await cls.get_slice_by_category_id(
                session=session,
                offset=callback_data.slice,
                limit=8,
                category_id=callback_data.category_id
            )
        else:
            products = await cls.get_slice_by_category_id(
                session=session,
                offset=callback_data.slice,
                limit=callback_data.slice + 8,
                category_id=callback_data.category_id)
        return products, page, callback_data

    @classmethod
    async def get_product_by_id(cls, session: AsyncSession, product_id: int) -> 'Product':
        to_db = select(cls).where(cls.id == product_id)
        products = await session.execute(to_db)
        return products.scalar()


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
                        session: AsyncSession) -> int:
        to_db = select(func.count()).select_from(cls)
        count = await session.scalar(to_db)
        return count

    @classmethod
    async def get_list_models(
            cls,
            session: AsyncSession,
            callback_data: CategoriesPaginateCBF,
    ) -> Tuple[List['Category'], int]:
        count = await cls.get_count(session)
        page = math.ceil(count / 8)
        if callback_data.current_page > page or callback_data.current_page < 1:
            callback_data.current_page = 1
            callback_data.slice = 0
        models = await cls.get_slice(
            session=session, offset=callback_data.slice, limit=callback_data.slice + 8)
        return models, page


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
        
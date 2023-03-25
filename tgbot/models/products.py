import datetime
from typing import List
from sqlalchemy import String, DateTime, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tgbot.models.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30),unique=True, index=True)
    # pictures: Mapped[str] = relationship()
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
    commentary: Mapped()[str] = mapped_column(String(150), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    def __repr__(self):
        return f'Product({self.id}, {self.name}, {self.category_id})'


class Category(Base):
    __tablename__ = "category_products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30),unique=True, index=True)
    products: Mapped[List['Product']] = relationship(
        'Product', back_populates='category', lazy='selectin',
    )
    description: Mapped[str] = mapped_column(String(150))
    commentary: Mapped()[str] = mapped_column(String(150), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )

    def __repr__(self):
        return f'Category({self.id}, {self.name})'


class Picture(Base):
    __tablename__ = "picture_products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30),unique=True, index=True)
    # path: Mapped[str] = mapped_column(String(30), unique=True)
    commentary: Mapped()[str] = mapped_column(String(150), nullable=True)
    product_id: Mapped[int] =  mapped_column(ForeignKey('products.id'), nullable=False)
    product: Mapped['Product'] = relationship(
        'Product', back_populates='pictures', lazy='selectin',
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )

    def __repr__(self):
        return f'Picture({self.id}, {self.name}, {self.product_id})'
        
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Text, func
from sqlalchemy.orm import relationship, Mapped
from typing import List, Optional
from datetime import datetime
from ..database.config import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    email: Mapped[str] = Column(String(100), unique=True, index=True)
    username: Mapped[str] = Column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = Column(String(255))
    full_name: Mapped[Optional[str]] = Column(String)
    is_active: Mapped[bool] = Column(Boolean, default=True)
    is_admin: Mapped[bool] = Column(Boolean, default=False)
    created_at: Mapped[datetime] = Column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = Column(Text, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="category", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    description: Mapped[Optional[str]] = Column(Text, nullable=True)
    price: Mapped[float] = Column(Float, nullable=False)
    stock: Mapped[int] = Column(Integer, nullable=False, default=0)
    category_id: Mapped[int] = Column(Integer, ForeignKey("categories.id"), nullable=False)
    image_url: Mapped[Optional[str]] = Column(String(255), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = Column(String(20), nullable=False)
    total_amount: Mapped[float] = Column(Float, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = Column(Integer, nullable=False)
    unit_price: Mapped[float] = Column(Float, nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    full_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(UserBase):
    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None
    password: str | None = Field(None, min_length=8)

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

# Category schemas
class CategoryBase(BaseModel):
    name: str
    description: str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: str | None = None
    description: str | None = None

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

# Product schemas
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int
    category_id: int
    image_url: str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    category_id: int | None = None
    image_url: str | None = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

# OrderItem schemas
class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    
    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    quantity: int | None = None
    unit_price: float | None = None

class OrderItem(OrderItemBase):
    id: int

# Order schemas
class OrderBase(BaseModel):
    user_id: int
    status: str
    total_amount: float
    
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(OrderBase):
    status: str | None = None
    total_amount: float | None = None

class Order(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: List[OrderItem]

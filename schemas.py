from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


# Схемы для товаров
class ProductBase(BaseModel):
    name: Annotated[str, Field(min_length=1, description="Название товара")]
    price: Annotated[float, Field(ge=0, description="Стоимость товара")]
    category: Annotated[str, Field(min_length=3, description="Категория товара")]


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Annotated[str | None, Field(min_length=1)] = None
    price: Annotated[float | None, Field(ge=0)] = None
    category: Annotated[str | None, Field(min_length=3)] = None


class ProductResponse(ProductBase):
    id: int


# Схемы для пользователей
class UserBase(BaseModel):
    name: Annotated[str, Field(max_length=20, description="Имя пользователя")]
    age: Annotated[
        int, Field(ge=1, le=120, description="Возраст пользователя (от 1 до 120 лет)")
    ]
    email: Annotated[EmailStr, Field(max_length=50, description="Электронная почта")]


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

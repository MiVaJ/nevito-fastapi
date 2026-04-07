from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI(
    openapi_tags=[
        {
            "name": "Домашнее задание от 28.03.2026",
            "description": "Валидация ID пользователя и Фильтрация товаров с валидацией",
        },
    ]
)


@app.get("/calculate")
async def calculate(
    a: Annotated[int, "Первое число"],
    b: Annotated[int, "Второе число"],
    operation: Annotated[str, "Операция: add, subtract, multiply, divide"],
) -> dict:
    if operation == "add":
        return {"result": a + b}
    elif operation == "subtract":
        return {"result": a - b}
    elif operation == "multiply":
        return {"result": a * b}
    elif operation == "divide":
        if b == 0:
            return {"error": "Деление на ноль"}
        return {"result": a / b}
    else:
        return {"error": f"Неизвестная операция: {operation}"}


@app.get("/users/{user_id}", tags=["Домашнее задание от 28.03.2026"])
async def get_user(
    user_id: Annotated[int, Path(description="ID пользователя от 1 до 1000")],
) -> dict:
    if user_id <= 0:
        return {"detail": "ID должен быть больше 0"}
    if user_id > 1000:
        return {"detail": "ID должен быть от 1 до 1000"}
    return {"user_id": user_id, "name": "Иван"}


@app.get("/products", tags=["Домашнее задание от 28.03.2026"])
async def search_products(
    category: Annotated[
        str | None, Query(min_length=3, pattern="^[a-zA-Zа-яА-Я]+$")
    ] = None,
    min_price: Annotated[float | None, Query(ge=0, le=1000000)] = None,
    max_price: float | None = None,
    in_stock: bool | None = None,
) -> dict:
    if max_price is not None and min_price is not None and max_price <= min_price:
        return {"detail": "max_price должен быть больше min_price"}
    return {
        "products": [],
        "filters": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "in_stock": in_stock,
        },
    }

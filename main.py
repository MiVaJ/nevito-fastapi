from typing import Annotated

from fastapi import Body, FastAPI, HTTPException, Path, Query, status

app = FastAPI(
    openapi_tags=[
        {
            "name": "Домашнее задание от 28.03.2026",
            "description": "Валидация и фильтрация",
        },
        {
            "name": "Домашнее задание от 29.03.2026",
            "description": "Работа с пользователями: создание, получение списка",
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


users_db = {
    1: {"name": "Ivan", "age": 25, "email": "ivan@example.com"},
    2: {"name": "Alice", "age": 30, "email": "alice@example.com"},
    3: {"name": "John", "age": 22, "email": "john@example.com"},
    4: {"name": "Sophia", "age": 28, "email": "sophia@example.com"},
    5: {"name": "Michael", "age": 35, "email": "michael@example.com"},
}


@app.get("/users/{user_id}", tags=["Домашнее задание от 28.03.2026"])
async def get_user(
    user_id: Annotated[int, Path(description="ID пользователя от 1 до 1000")],
) -> dict:
    if user_id <= 0:
        return {"detail": "ID должен быть больше 0"}
    if user_id > 1000:
        return {"detail": "ID должен быть от 1 до 1000"}
    return {"user_id": user_id, "name": "Иван"}


@app.get("/users", tags=["Домашнее задание от 29.03.2026"])
async def get_users() -> list[dict]:
    # Преобразуем словарь users_db в список, добавляя ID в каждый объект пользователя
    return [{"id": key} | value for key, value in users_db.items()]


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    tags=["Домашнее задание от 29.03.2026"],
)
async def create_user(
    name: Annotated[str, Body(max_length=20, description="Имя пользователя")],
    age: Annotated[
        int, Body(ge=1, le=120, description="Возраст пользователя (от 1 до 120 лет)")
    ],
    email: Annotated[str, Body(max_length=50, description="Электронная почта")],
) -> dict:
    for user in users_db.values():
        if user["email"] == email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

    new_index = max(users_db) + 1 if users_db else 1
    new_user = {"name": name, "age": age, "email": email}
    users_db[new_index] = new_user
    return new_user


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

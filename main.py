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
        {
            "name": "Домашнее задание от 04-05.04.2026",
            "description": "CRUD для товаров",
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


products_db = {
    1: {"name": "Smartphone", "price": 50000.0, "category": "Electronics"},
    2: {"name": "Laptop", "price": 100000.0, "category": "Electronics"},
    3: {"name": "Coffee Maker", "price": 15000.0, "category": "Appliances"},
    4: {"name": "Headphones", "price": 12000.0, "category": "Electronics"},
    5: {"name": "Smart Watch", "price": 25000.0, "category": "Electronics"},
    6: {"name": "Blender", "price": 8000.0, "category": "Appliances"},
    7: {"name": "Mechanical Keyboard", "price": 9000.0, "category": "Accessories"},
    8: {"name": "Gaming Mouse", "price": 5000.0, "category": "Accessories"},
    9: {"name": "Monitor", "price": 35000.0, "category": "Electronics"},
    10: {"name": "Vacuum Cleaner", "price": 20000.0, "category": "Appliances"},
}


def check_product_exists(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")


# GET /products — список всех товаров (с лимитированной выдачей: limit)
@app.get(
    "/products",
    tags=["Домашнее задание от 28.03.2026", "Домашнее задание от 04-05.04.2026"],
)
async def search_products(
    category: Annotated[
        str | None, Query(min_length=3, pattern="^[a-zA-Zа-яА-Я]+$")
    ] = None,
    min_price: Annotated[float | None, Query(ge=0, le=1000000)] = None,
    max_price: float | None = None,
    in_stock: bool | None = None,
    limit: Annotated[int, Query(ge=1, le=100, description="Лимит выдачи товаров")] = 3,
) -> dict:
    if max_price is not None and min_price is not None and max_price <= min_price:
        return {"detail": "max_price должен быть больше min_price"}
    products_list = [{"id": key} | value for key, value in products_db.items()]
    result_products = products_list[:limit]
    return {
        "products": result_products,
        "filters": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "in_stock": in_stock,
            "limit": limit,
        },
    }


# GET /products/{id} — конкретный товар
@app.get("/products/{id}", tags=["Домашнее задание от 04-05.04.2026"])
async def get_product(
    id: Annotated[int, Path(ge=1, description="ID продукта")],
) -> dict:
    check_product_exists(id)
    return {"id": id} | products_db[id]


# POST /products — создать товар
@app.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    tags=["Домашнее задание от 04-05.04.2026"],
)
async def create_product(
    name: Annotated[str, Body(min_length=1, description="Название товара")],
    price: Annotated[float, Body(ge=0, description="Стоимость товара")],
    category: Annotated[str, Body(min_length=3, description="Категория товара")],
) -> dict:
    for p in products_db.values():
        if p["name"] == name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists"
            )

    new_index = max(products_db) + 1 if products_db else 1
    new_product = {"name": name, "price": price, "category": category}
    products_db[new_index] = new_product
    return new_product


# PUT /products/{id} — полное обновление
@app.put("/products/{id}", tags=["Домашнее задание от 04-05.04.2026"])
async def update_product(
    id: Annotated[int, Path(ge=1)],
    name: Annotated[str, Body()],
    price: Annotated[float, Body(ge=0)],
    category: Annotated[str, Body()],
) -> dict:
    check_product_exists(id)
    products_db[id] = {"name": name, "price": price, "category": category}
    return {"id": id} | products_db[id]


# PATCH /products/{id} — частичное обновление
@app.patch("/products/{id}", tags=["Домашнее задание от 04-05.04.2026"])
async def patch_product(
    id: Annotated[int, Path(ge=1)],
    name: Annotated[str | None, Body()] = None,
    price: Annotated[float | None, Body(ge=0)] = None,
    category: Annotated[str | None, Body()] = None,
) -> dict:
    check_product_exists(id)
    # Предотвращаем обновление без указания данных
    if all(v is None for v in (name, price, category)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must update at least one field",
        )

    stored_item = products_db[id]

    if name is not None:
        stored_item["name"] = name
    if price is not None:
        stored_item["price"] = price
    if category is not None:
        stored_item["category"] = category

    return {"id": id} | stored_item


# DELETE /products/{id} — удаление
@app.delete("/products/{id}", tags=["Домашнее задание от 04-05.04.2026"])
async def delete_product(id: Annotated[int, Path(ge=1)]):
    check_product_exists(id)
    del products_db[id]
    return {"detail": f"Товар {id} удален"}

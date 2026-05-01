from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, Path, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import schemas
from database import messages_db, products_db, users_db

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
        {
            "name": "Домашнее задание от 11-12.04.2026",
            "description": "Фронтенд на Jinja2: работа с сообщениями",
        },
        {
            "name": "Домашнее задание от 18-19.04.2026 Jinja",
            "description": "Jinja2: серверный CRUD и HTML-формы",
        },
        {
            "name": "Домашнее задание от 18-19.04.2026 JS",
            "description": "JS: динамический CRUD через Fetch API и JSON",
        },
    ]
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["null", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


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


@app.get(
    "/users",
    response_model=list[schemas.UserResponse],
    tags=["Домашнее задание от 29.03.2026"],
)
async def get_users():
    # Преобразуем словарь users_db в список, добавляя ID в каждый объект пользователя
    return [{"id": key} | value for key, value in users_db.items()]


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse,
    tags=["Домашнее задание от 29.03.2026"],
)
async def create_user(user_data: schemas.UserCreate) -> dict:
    for user in users_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

    new_index = max(users_db) + 1 if users_db else 1
    new_user = {"name": user_data.name, "age": user_data.age, "email": user_data.email}
    users_db[new_index] = new_user
    return new_user


def check_product_exists(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")


# GET /products — список всех товаров (с лимитированной выдачей: limit)
@app.get(
    "/products",
    response_model=list[schemas.ProductResponse],
    tags=["Домашнее задание от 28.03.2026", "Домашнее задание от 04-05.04.2026"],
)
async def search_products(
    limit: Annotated[int, Query(ge=1, le=100, description="Лимит выдачи товаров")] = 3,
):
    products_list = [{"id": key} | value for key, value in products_db.items()]
    return products_list[:limit]


# GET /products/{id} — конкретный товар
@app.get(
    "/products/{id}",
    response_model=schemas.ProductResponse,
    tags=["Домашнее задание от 04-05.04.2026"],
)
async def get_product(
    id: Annotated[int, Path(ge=1, description="ID продукта")],
):
    check_product_exists(id)
    return {"id": id} | products_db[id]


# POST /products — создать товар
@app.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProductResponse,
    tags=["Домашнее задание от 04-05.04.2026"],
)
async def create_product(product: schemas.ProductCreate):
    for p in products_db.values():
        if p["name"] == product.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists"
            )

    new_index = max(products_db) + 1 if products_db else 1
    products_db[new_index] = product.model_dump()
    return {"id": new_index} | products_db[new_index]


# PUT /products/{id} — полное обновление
@app.put(
    "/products/{id}",
    response_model=schemas.ProductResponse,
    tags=["Домашнее задание от 04-05.04.2026"],
)
async def update_product(
    id: Annotated[int, Path(ge=1)],
    product: schemas.ProductCreate,
):
    check_product_exists(id)
    products_db[id] = {
        "name": product.name,
        "price": product.price,
        "category": product.category,
    }
    return {"id": id} | products_db[id]


# PATCH /products/{id} — частичное обновление
@app.patch(
    "/products/{id}",
    response_model=schemas.ProductResponse,
    tags=["Домашнее задание от 04-05.04.2026"],
)
async def patch_product(
    id: Annotated[int, Path(ge=1)],
    product: schemas.ProductUpdate,
):
    check_product_exists(id)
    # Предотвращаем обновление без указания данных
    if all(v is None for v in (product.name, product.price, product.category)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must update at least one field",
        )

    stored_item = products_db[id]

    if product.name is not None:
        stored_item["name"] = product.name
    if product.price is not None:
        stored_item["price"] = product.price
    if product.category is not None:
        stored_item["category"] = product.category

    return {"id": id} | stored_item


# DELETE /products/{id} — удаление
@app.delete("/products/{id}", tags=["Домашнее задание от 04-05.04.2026"])
async def delete_product(id: Annotated[int, Path(ge=1)]):
    check_product_exists(id)
    del products_db[id]
    return {"detail": f"Товар {id} удален"}


# GET /web/messages - получить список всех сообщений
@app.get(
    "/web/messages",
    response_class=HTMLResponse,
    tags=["Домашнее задание от 11-12.04.2026"],
)
async def list_messages(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "messages": messages_db},
    )


# GET /web/messages/{message_id}/edit - получить страницу с обновлением сообщения
@app.get(
    "/web/messages/{message_id}/edit",
    response_class=HTMLResponse,
    tags=["Домашнее задание от 11-12.04.2026"],
)
async def edit_message_form(request: Request, message_id: int):
    message = next((m for m in messages_db if m.id == message_id), None)

    if not message:
        raise HTTPException(status_code=404, detail="Сообщение не найдено")

    return templates.TemplateResponse(
        request=request, name="edit.html", context={"message": message}
    )


# GET /web/messages/create — форма для создания нового сообщения
@app.get(
    "/web/messages/create",
    response_class=HTMLResponse,
    tags=["Домашнее задание от 18-19.04.2026 Jinja"],
)
async def create_message_form(request: Request):
    return templates.TemplateResponse(request=request, name="create.html", context={})


# POST /web/messages — добавление нового сообщения в базу данных
@app.post("/web/messages", tags=["Домашнее задание от 18-19.04.2026 Jinja"])
async def create_message(content: Annotated[str, Form()]):
    new_id = max((m.id for m in messages_db), default=0) + 1
    new_msg = schemas.MessageRead(id=new_id, content=content)
    messages_db.append(new_msg)
    return RedirectResponse(url="/web/messages", status_code=303)


# POST /web/messages/{message_id} - обновление сообщения
@app.post("/web/messages/{message_id}", tags=["Домашнее задание от 11-12.04.2026"])
async def update_message(message_id: int, content: Annotated[str, Form()]):
    for i, m in enumerate(messages_db):
        if m.id == message_id:
            updated_message = schemas.MessageRead(id=message_id, content=content)

            messages_db[i] = updated_message

            return RedirectResponse(url="/web/messages", status_code=303)

    raise HTTPException(status_code=404, detail="Message not found")


# POST /web/messages/{message_id}/delete — удаление сообщения
@app.post(
    "/web/messages/{message_id}/delete",
    tags=["Домашнее задание от 18-19.04.2026 Jinja"],
)
async def delete_message(message_id: int):
    message = next((m for m in messages_db if m.id == message_id), None)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    messages_db.remove(message)
    return RedirectResponse(url="/web/messages", status_code=303)


# Вспомогательная функция для генерации нового ID
def next_id() -> int:
    return max((m.id for m in messages_db), default=0) + 1


# Вспомогательная функция для поиска сообщения по ID
def get_index(message_id: int) -> int:
    for i, m in enumerate(messages_db):
        if m.id == message_id:
            return i
    return -1


# GET /web/messages-js — открыть страницу с JS-интерфейсом
@app.get(
    "/web/messages-js",
    response_class=HTMLResponse,
    tags=["Домашнее задание от 18-19.04.2026 JS"],
)
async def messages_js_page(request: Request):
    return templates.TemplateResponse(request=request, name="messages_js.html")


# API GET /api/messages — получить список всех сообщений
@app.get(
    "/api/messages",
    response_model=list[schemas.MessageRead],
    tags=["Домашнее задание от 18-19.04.2026 JS"],
)
async def api_get_messages():
    return messages_db


# API POST /api/messages — создать сообщение (принимает JSON, а не форму)
@app.post(
    "/api/messages", status_code=201, tags=["Домашнее задание от 18-19.04.2026 JS"]
)
async def api_create_message(message: schemas.MessageCreate):
    new_msg = schemas.MessageRead(id=next_id(), content=message.content)
    messages_db.append(new_msg)
    return new_msg


# API PUT /api/messages/{message_id} — полное обновление сообщения
@app.put(
    "/api/messages/{message_id}",
    response_model=schemas.MessageRead,
    tags=["Домашнее задание от 18-19.04.2026 JS"],
)
async def api_update_message(message_id: int, message_data: schemas.MessageUpdate):
    idx = get_index(message_id)

    if idx < 0:
        raise HTTPException(status_code=404, detail="Message not found")

    updated_msg = schemas.MessageRead(id=message_id, content=message_data.content)
    messages_db[idx] = updated_msg
    return updated_msg


# API PATCH /api/messages/{message_id} — частичное обновление сообщения
@app.patch(
    "/api/messages/{message_id}",
    response_model=schemas.MessageRead,
    tags=["Домашнее задание от 18-19.04.2026 JS"],
)
async def api_patch_message(message_id: int, message_data: schemas.MessagePatch):
    idx = get_index(message_id)
    if idx < 0:
        raise HTTPException(status_code=404, detail="Message not found")

    if message_data.content is not None:
        messages_db[idx].content = message_data.content
    return messages_db[idx]


# API DELETE /api/messages/{id} — удалить сообщение
@app.delete(
    "/api/messages/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Домашнее задание от 18-19.04.2026 JS"],
)
async def api_delete_message(message_id: int):
    message = next((m for m in messages_db if m.id == message_id), None)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    messages_db.remove(message)
    return {"detail": "Deleted"}

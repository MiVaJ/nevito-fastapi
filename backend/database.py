from schemas import MessageRead

users_db = {
    1: {"name": "Ivan", "age": 25, "email": "ivan@example.com"},
    2: {"name": "Alice", "age": 30, "email": "alice@example.com"},
    3: {"name": "John", "age": 22, "email": "john@example.com"},
    4: {"name": "Sophia", "age": 28, "email": "sophia@example.com"},
    5: {"name": "Michael", "age": 35, "email": "michael@example.com"},
}

products_db: dict[int, dict[str, str | float]] = {
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

messages_db: list[MessageRead] = [
    MessageRead(id=1, content="Hello Dmitriy"),
    MessageRead(id=2, content="How are you Max?"),
    MessageRead(id=3, content="FastAPI is really fast!"),
    MessageRead(id=4, content="Jinja2 templates are great"),
    MessageRead(id=5, content="Learning backend is exciting"),
]

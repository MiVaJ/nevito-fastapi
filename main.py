from typing import Annotated

from fastapi import FastAPI

app = FastAPI()


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

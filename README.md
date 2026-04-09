# Nevito

Тестовый репозиторий для работы с FastAPI

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/MiVaJ/nevito-fastapi.git
cd nevito-fastapi
```

### 2. Настройка виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate     # Для Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Запуск приложения
```bash
uvicorn main:app --reload
```

## Разработка и качество кода

Для проверки кода используются Ruff и Mypy. Перед созданием коммита рекомендуется запускать следующие команды:

### 1. Линтинг и форматирование (Ruff)
Проверить код на ошибки и отсортировать импорты:
```bash
ruff check . --fix
```

Отформатировать код (привести к единому стилю):
```bash
ruff format .
```

### 2. Проверка типизации (Mypy)
Проверить корректность аннотаций типов:
```bash
mypy .
```
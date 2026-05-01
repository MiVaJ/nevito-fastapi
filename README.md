# Nevito

Тестовый репозиторий для работы с FastAPI

## Структура проекта
- `backend/`: API на FastAPI (Python 3.10+)
- `frontend/`: Клиентское приложение на React (Vite/NPM)

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
cd backend
uvicorn main:app --reload
```
## Навигация по проекту

После запуска сервера приложение доступно по следующим адресам:

### 1. Веб-интерфейс (Jinja2)
Классическое CRUD-приложение с серверным рендерингом.
*   **Путь**: `/web/messages`

### 2. Веб-интерфейс (JavaScript)
Динамическое CRUD-приложение, работающее через Fetch API.
*   **Путь**: `/web/messages-js`

### 3. Документация API
Интерактивная песочница Swagger для тестирования эндпоинтов.
*   **Путь**: `/docs`

## Разработка и качество кода

Для проверки кода используются Ruff и Mypy. Перед созданием коммита рекомендуется запускать следующие команды:

### 1. Линтинг и форматирование (Ruff)
Проверить код на ошибки и отсортировать импорты:
```bash
ruff check backend/ --fix
```

Отформатировать код (привести к единому стилю):
```bash
ruff format backend/
```

### 2. Проверка типизации (Mypy)
Проверить корректность аннотаций типов:
```bash
mypy backend/ --config-file backend/pyproject.toml
```
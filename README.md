# Nevito

Тестовый репозиторий для работы с FastAPI

## Структура проекта
- `backend/`: API на FastAPI (Python 3.10+)
- `frontend/`: Клиентское приложение на React (Vite/NPM)

## Установка и настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/MiVaJ/nevito-fastapi.git
cd nevito-fastapi
```

### 2. Настройка Бэкенда (FastAPI)
Создание окружения и установка зависимостей:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate     # Для Windows

pip install -r requirements.txt
```

### 3. Настройка Фронтенда (React)
Установка библиотек Node.js:
```bash
cd frontend
npm install
```
## Запуск проекта
Для полноценной работы нужно запустить оба сервера в разных терминалах.

### 1. Запуск Бэкенда
```bash
cd backend
uvicorn main:app --reload
```

### 2. Запуск Фронтенда
```bash
cd frontend
npm run dev
```

## Навигация по проекту

После запуска сервера приложение доступно по следующим путям:

### 1. Интерфейс React (Порт 5173)
*   **Адрес**: `localhost:5173` (основное приложение)

### 2. Веб-интерфейс (Jinja2)
Классическое CRUD-приложение с серверным рендерингом.
*   **Путь**: `:8000/web/messages`

### 3. Веб-интерфейс (JavaScript)
Динамическое CRUD-приложение, работающее через Fetch API.
*   **Путь**: `:8000/web/messages-js`

### 4. Документация API
Интерактивная песочница Swagger для тестирования эндпоинтов.
*   **Путь**: `:8000/docs`

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
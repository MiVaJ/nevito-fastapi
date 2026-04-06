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
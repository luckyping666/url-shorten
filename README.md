# URL Shortener Service

Асинхронный сервис сокращения ссылок на FastAPI с поддержкой:
- генерации коротких идентификаторов
- редиректов
- подсчёта кликов
- асинхронной работы (SQLAlchemy + aiosqlite)
- тестов (pytest + httpx.AsyncClient)
- Docker‑окружения

---

## 🚀 Стек технологий

- FastAPI
- SQLAlchemy 2.0 (async)
- SQLite / aiosqlite
- Pydantic v2
- pytest + pytest-asyncio
- httpx.AsyncClient
- Docker / docker-compose

---

## 📦 Установка и запуск локально

### 1. Клонировать репозиторий
```bash
git clone <repo-url>
cd url_shortener
```

### 2. Создать виртуальное окружение
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Запустить приложение
```bash
uvicorn app.main:app --reload --port 8001
```

### 5. Открыть Swagger UI
```bash
http://127.0.0.1:8001/docs
```


## 🐳 Запуск в Docker

### 1. Собрать образ
```bash
docker-compose build
```

### 2. Запустить контейнер
```bash
docker-compose up -d
```

### Запуск тестов
```bash
pytest app/tests -v
```

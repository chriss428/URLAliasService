# URL Alias Service

## Описание
Проект представляет собой сервис для сокращения URL-адресов с возможностью аутентификации пользователей, создания коротких ссылок, их деактивации и просмотра статистики.

## Функционал
- Регистрация пользователя
- Получение списка активных ссылок (требует аутентификации)
- Создание короткой ссылки (требует аутентификации)
- Перенаправление на оригинальный URL
- Деактивация короткой ссылки (требует аутентификации)

## Технологический стек
- Python 3.12
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Poetry (управление зависимостями)
- Alembic (миграции)

## Установка и запуск

### В контейнере

1. **Запустите compose файл:**
    ```bash
   docker compose up -d
2. **Перейдите по адресу:**
    ```bash
    localhost:1500/docs

1. **Установите и настройте  PostgreSQL**
2. **Склонируйте репозиторий и перейдите в директорию проекта**
   ```bash
   git clone https://github.com/URL_Alias_Service.git
   cd URL_Alias_Service

3. **Создайте виртуальное окружение**
    ```bash
    python -m venv venv
   
4. **Активируйте виртуальное окружение**
- Windows:
    ```bash
    venv\Scripts\activate

- Linux/MacOS:
    ```bash
    source venv/bin/activate

5. **Установите все зависимости**
    ```bash
    pip install poetry
    poetry install
   
6. **Создайте файл .env в корне проекта со следующими переменными:**
    ```python
    DB_HOST = "127.0.0.1"
    DB_PORT = "5432"
    DB_NAME = "name-db"
    DB_USER = "user"
    DB_PASSWORD = "password"

7. **Примените миграцию для создания таблицы в БД**
    ```bash
   alembic upgrade head

8. **Запустите приложение**
    ```bash
   uvicorn app.main:app

9. **Перейдите по ссылке: http://localhost:8000/docs**



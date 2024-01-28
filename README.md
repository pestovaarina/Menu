## Использованные технологии:
- Python (FastAPI, SQLAlchemy)
- PostgreSQL
- Docker
- pytest

## Описание проекта
REST API по работе с меню ресторана.

Документация доступна по адресу http://127.0.0.1:8000/docs, после установки и запуска сервиса.

## Установка и запуск
Для запуска приложения необходим Docker.

Клонируйте репозиторий и перейдите в папку проекта:

```
git clone git@github.com:pestovaarina/Menu.git
```
```
cd Menu
```

Создайте .env файл, с параметрами:

``` 
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres

POSTGRES_USER_TEST=postgres
POSTGRES_PASSWORD_TEST=postgres
POSTGRES_DB_TEST=postgres_test
```

Выполните команду для сборки и запуска проекта:

```
docker-compose up --build -d
```
```
docker-compose up test
```
## Сложный ORM запрос
v1/crud/menu.py/get_menu

# Проект cat_charity_fund
## Описание

Бэкенд приложения и api для благотворительных пожертвований для животных. 

## Стек:
FastAPI, SQLAlchemy, Alembic, pydantic, aiosqlite, JSON Web Token.

### Реализованные функции:
- Регистрация/аутентификация пользователей
- Отправка донатов в благотворительные проекты/просмотр своих донатов
- Для суперюзера - создание/редактирование благотворительных проектов.

## Установка:
Клонировать репозиторий и перейти в него в командной строке:
```sh
git@github.com:VDronovVladislav/cat_charity_fund.git
cd cat_charity_fund
```
Cоздать и активировать виртуальное окружение:
```sh
python -m venv venv
```
* Если у вас Linux/macOS

```
source venv/bin/activate

```

* Если у вас windows

```
source venv/Scripts/activate

```
Установить зависимости из файла requirements.txt:
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Использование:
Запустить приложение командой в терминале:
```sh
uvicorn app.main:app --reload
```
Документация API будет доступно по адресу:
```sh
http://127.0.0.1:8000/docs
```

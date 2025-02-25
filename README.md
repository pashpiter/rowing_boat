# rowing_boat

#### Стек: Python, FastAPI, uvicorn, SQLModel, sqlite, pytest

## О проекте
Этот проект представляет собой веб-приложение для управления лодкой и ее характеристиками.

## Запуск проекта

Для запуска проекта необходимо: 
* Клонировать репозиторий
```
git clone git@github.com:pashpiter/rowing_boat.git
```
* Перейти в папку rowing_boat

* Создать виртуальное окружение:
```
python3 -m venv venv
```
* Активировать виртуальное окружение:
```
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows
```
* Установить зависимости:
```
pip install -r requirements.txt
```
* Запустить приложение:
```
uvicorn app.main:app --reload
```

## Документация
Документация доступна по адресу:
```
http://127.0.0.1:8000/docs
```

## Тестирование

Команда для запуска тестов:
```
pytest
```
Тесты используют отдельную базу данных test_database.db, которая создается в папке tests. После выполнения тестов база данных автоматически очищается.

## API

### Получить информацию о лодке

`GET /api/v1/boat`

Пример ответа:
```
{
  "name": "string",
  "seats": 2,
  "speed": 0,
  "direction": "Вперед",
  "passengers": [],
  "age": 0
}
```
---
### Обновить поля лодки
`PATCH /api/v1/boat`

Query-параметры:
- name (строка, опционально): Название лодки.
- seats (целое число, опционально): Количество мест.
- speed (число, опционально): Скорость лодки.
- direction (строка, опционально): Направление движения лодки.

Пример запроса:
```
PATCH /api/v1/boat?name=Ласточка&seats=4&speed=2&direction=Назад
```
Пример ответа:
```
{
  "name": "Ласточка",
  "seats": 4,
  "speed": 2,
  "direction": "Назад",
  "passengers": [
    {
        "name": "Андрей"
    }
  ],
  "age": 0
}
```
---
### Добавить пассажира в лодку
`PATCH /api/v1/boat/add_passenger`

Query-параметры:
- name (строка): Имя пассажира.

Пример запроса:
```
PATCH /api/v1/boat/add_passenger?name=Марк
```
Пример ответа:
```
{
  "name": "Ласточка",
  "seats": 4,
  "speed": 2,
  "direction": "Назад",
  "passengers": [
    {
        "name": "Андрей"
    },
    {
        "name": "Марк"
    }
  ],
  "age": 0
}
```
---
### Удалить пассажира с лодки
`PATCH /api/v1/boat/delete_passenger`

Query-параметры:
- name (строка): Имя пассажира.

Пример запроса:
```
PATCH /api/v1/boat/delete_passenger?name=Марк
```
Пример ответа:
```
{
  "name": "Ласточка",
  "seats": 4,
  "speed": 2,
  "direction": "Назад",
  "passengers": [
    {
        "name": "Андрей"
    }
  ],
  "age": 0
}
```
---
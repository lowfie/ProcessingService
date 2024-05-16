# Processing Service

## Описание
Сервис для обработки высокой нагрузки данных и представления агрегированной информацию в удобной форме.

Swagger - http://localhost:8000/api/v1/docs  
entrypoint - `src/api/main.py`
## Запуск приложения

#### Создание конфигурационных файлов.
В корне проекта создать `.env` файл, пример `.env.example` файл.  
В `src/config/files` создать `dev.yaml` или `production.yaml`, пример файла находится в этой же директории.

### Полная инициализация
#### Запуск проекта/миграций/админа
Команда `make init`

### Частичная инициализация
#### Запуск проекта
Команда `make up`

#### Создаём миграции
Команда `make revision upgrade`

#### Создаём админа 
Команда `make create-admin`

## Make команды
1. init - инициализация включающая в себя пул команд
2. up/down/restart - запуск/остановка/перезагрузка приложения
3. logs-<service> - просмотр логов (logs просмотр логов api)
4. shell-<service> - открытие интерактивной консоли (shell запуск python терминала приложения)
5. revision - сделать миграцию
6. upgrade - инициализировать +1 миграцию от предыдущей
7. upgrade-head - инициализация всех миграций
8. downgrade - откатиться на -1 миграцию
9. clean-migrations - отчистка всех миграций
10. clean - полная чистка базы данных и миграций
11. create-admin - создание админа

## Технологии
 - Python 3.12
 - FastApi [uvicorn]
 - Pydantic 2
 - SQLAlchemy [asyncpg]
 - PostgresSQL 15
 - Docker, Docker compose
 - Poetry

## Нюансы
Я не хешировал пароли в базе данных,
так как это демонстрационный пример источников (пользователей)

В директории `src/scripts/populate.py` можно создать нагрузку для создания данных.
В нём нужно указать количество источников, ивентов в секунду от источников,
токен авторизации источника (пользователя), лимит на количество итераций.

Также можно добавить админ панель, используя SQLAdmin. 
Нагрузочное тестирование проводил в мануальном режиме.
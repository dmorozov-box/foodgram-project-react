# Сайт "Продуктовый помощник" http://51.250.95.157/

![example branch parameter](https://github.com/dmorozov-box/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?event=push)

## Описание

Это сайт, на котором можно публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. 

На сайте есть «Список покупок», в который можно добавлять рецепты, которые Вы собираетесь приготовить и на его основе скачать список и количество покупаемых продуктов.

Фронтэнд сайта разработан предоставил Яндекс Практикум.

Сайт доступен по ссылке (фронтенд) http://51.250.95.157/

Админ панель сайта http://51.250.95.157/admin/

OpenAPI спецификация бэкенда http://51.250.95.157/api/docs/


## Развертывание проекта на локальном сервере

### Шаблон наполнения файла переменных окружения .env
```
POSTGRES_DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
POSTGRES_DB_NAME=postgres # имя базы данных
POSTGRES_USER=foodgram # логин для подключения к базе данных
POSTGRES_PASSWORD=foodgram # пароль для подключения к БД (установите свой)
POSTGRES_DB_HOST=db # название сервиса (контейнера)
POSTGRES_DB_PORT=5432 # порт для подключения к БД 
```

### Команды запуска проекта в Docker

1. В папке /infra Собрать и запустить образы
```
docker-compose up -d --build
```
2. Выполнить миграции, создать суперпользователя и собрать статику в контейнере
Для этого в контейнере backend нужно выполнить команды:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
```
3. Для остановки контейнеров воспользуйтесь командой
```
docker-compose down -v
```
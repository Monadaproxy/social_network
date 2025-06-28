# *Social Network Project*

****Проект, реализующий социальную сеть, где пользователи могут общаться,
добавлять друг друга в друзья, выкладывать записи в профиль и комментировать посты****

Для запуска проекта на локальном веб-сервере потребуется `Docker`

## Инструкция по запуску

1. Клонируйте репозиторий:

```bash
    git clone https://github.com/Monadaproxy/social_network.git
    cd social_network
```

2. Запустите сервисы:
```bash
    docker-compose build
    docker-compose up -d
```

🔧 **Логи** (если нужно):
```bash
    docker-compose logs -f
```
#### После поднятия стенда автоматически создастся суперпользователь `admin` с паролем `admin1234`
Административная панель доступна на `http://127.0.0.1:8000/admin/`

## Стек технологий


+ Python 3
+ Django
+ PostgreSQL 
+ RabbitMQ 
+ Docker


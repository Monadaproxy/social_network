#!/bin/bash

set -e


if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


python manage.py makemigrations

python manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin1234') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

exec "$@"
#!/bin/sh

if [ "$POSTGRES_DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python3 app/manage.py makemigrations
python3 app/manage.py migrate
python3 app/manage.py runserver 0.0.0.0:8000

exec "$@"
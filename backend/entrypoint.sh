#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
while ! pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
    sleep 1
done

echo "PostgreSQL is ready!"

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Creating superuser if it doesn't exist..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created.')
else:
    print('Superuser already exists.')
END

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"

#!/bin/bash

# Wait for the Postgres database to be available
python manage.py wait_for_db

# Apply database migrations
python manage.py migrate

# Insert initial data !! not in production

if [ "$ENV_TYPE" != "production" ]; then
  python manage.py insertdata
fi

# Start the Django development server
exec python manage.py runserver 0.0.0.0:8000

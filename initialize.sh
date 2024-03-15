#!/bin/bash


# Apply database migrations
python manage.py migrate

# Insert initial data !! not in production

if [ "$ENV_TYPE" != "production" ]; then
  python manage.py insertdata
  exec python manage.py test

fi

# Start the Django development server
exec python manage.py runserver 0.0.0.0:8000

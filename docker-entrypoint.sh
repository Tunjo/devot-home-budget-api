#!/bin/sh
python3 -m pip install -r requirements.txt
# Don't run migrations before postgres container running
echo "Waiting for postgres to get up and running..."
while ! nc -z home_budget_db 5432; do
  # wait for postgres to start
  echo "waiting for postgres..."
  sleep 0.1
done
echo "PostgreSQL started"
echo "Running migrations"
python3 manage.py migrate
echo "Creating predefined categories..."
python3 manage.py create_predefined_categories
echo "Starting the server..."
python3 manage.py runserver 0.0.0.0:8000
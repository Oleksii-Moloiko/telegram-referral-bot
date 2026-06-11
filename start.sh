#!/bin/bash

set -e

echo "Running migrations..."
python manage.py migrate

echo "Starting bot..."
python bot/main.py
#!/bin/bash
cd Athena-master
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

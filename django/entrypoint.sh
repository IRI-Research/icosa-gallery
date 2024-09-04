#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput

if [[ -v DEPLOYMENT_HOST_WEB ]];
then
    echo "Setting $DEPLOYMENT_HOST_WEB as the default domain"
    python manage.py shell -c \
    "from django.contrib.sites.models import Site; Site.objects.filter(domain='example.com').update(domain='$DEPLOYMENT_HOST_WEB', name='$DEPLOYMENT_HOST_WEB')"
fi


echo "Running in $DEPLOYMENT_ENV mode"
if [[ $DEPLOYMENT_ENV == 'production' ]];
then
    python manage.py run_huey &
    gunicorn django_project.wsgi:application --bind 0.0.0.0:8000 --timeout 900
else
    python manage.py run_huey &
    python manage.py runserver 0.0.0.0:8000
fi

#!/bin/sh

if [ -z ${ENVIRONMENT} ]; then export ENVIRONMENT=local; fi

# start api with gunicorn
/usr/src/gajounal/venv/bin/gunicorn mysite.wsgi:application --bind 127.0.0.1:8004

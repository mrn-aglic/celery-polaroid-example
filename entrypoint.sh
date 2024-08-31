#!/bin/sh

echo $1

if [ "$1" = 'scheduler' ]
then
    exec celery -A celery_polaroid.beat beat --loglevel info
elif [ "$1" = 'monitoring' ]
then
    exec celery -A celery_polaroid.celeryapp events --camera=celery_polaroid.monitoring.camera.CeleryMonitor --frequency=2 --loglevel info
elif [ "$1" = 'worker' ]
then
    exec celery -A celery_polaroid.worker worker -E -Q default --loglevel info
elif [ "$1" = 'flower' ]
then
    exec celery -A celery_polaroid.worker --broker=redis://redis:6379/0 flower --conf=/config/flowerconfig.py
fi

exec "$@"

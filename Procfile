web: gunicorn core.wsgi --log-file-
web: python manage.py migrate && gunicorn core.wsgi
worker: celery -A core worker --loglevel=info

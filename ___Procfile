web: gunicorn core.wsgi

# Will be run after the build phase
release: python manage.py migrate && celery -A core worker --loglevel=info
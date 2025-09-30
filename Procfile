web: python manage.py migrate --noinput && gunicorn finsage_project.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 2

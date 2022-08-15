release: python manage.py migrate
web: waitress-serve --listen=*:8000 settings.wsgi:application
from .common import *
import os
import dj_database_url


DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['guide-system-backend.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config()
}

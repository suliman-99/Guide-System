from .common import *
import os
import dj_database_url
from datetime import timedelta


DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['guide-system-backend.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config()
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT'),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=5),
    'BLACKLIST_AFTER_ROTATION': False,
}

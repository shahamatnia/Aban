from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
SECRET_KEY = DJANGO_.SECRET_KEY

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': DBCONNECTION.ENGINE,
        'NAME': DBCONNECTION.NAME,
        'USER': DBCONNECTION.USER,
        'PASSWORD': DBCONNECTION.PASSWORD,
        'HOST': DBCONNECTION.HOST,
        'PORT': DBCONNECTION.PORT,
    }
}

# REDIS_HOST = 'localhost'

REDIS_HOST = 'redis'

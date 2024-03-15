import os

environment = os.getenv('DJANGO_ENV', 'local')

if environment == 'prod':
    from .prod import *
else:
    from .local import *

"""
for simplicity considerations
 !! we do not read credentials and sensitive data from environment variables and we hardcode them here !!
"""
import os


class DjangoConfigs:
    SECRET_KEY = 'django-insecure-=w1l4cy8_*g#tdxms1ef4g15xp@0%u_c1-c&()mfqu)-o&nlgp'


class DBConnectionConfigs:
    ENGINE = 'django.db.backends.postgresql'
    NAME = 'aban'
    USER = 'aban'
    PASSWORD = 'abanPass'
    HOST = 'db'
    PORT = 5432


class PurchaseConfigs:
    MIN_COST_INSTANT = 10

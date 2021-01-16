import dj_database_url

from decouple import config

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rentworkplace',
        'USER': 'postgres',
        'PASSWORD': '1',
    }
}


prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)



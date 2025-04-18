import os
from pathlib import Path
from datetime import timedelta

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jdeyzx1zzpteu^^ixg*dinazl@$tr_qo_s*34n94ac1dys(gk0'

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True


ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'IP_ВАШЕГО_СЕРВЕРА']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Добавляем настройки для статических файлов
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'),
]
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-jdeyzx1zzpteu^^ixg*dinazl@$tr_qo_s*34n94ac1dys(gk0'

DEBUG = False


ALLOWED_HOSTS = ['localhost', '127.0.0.1', '185.195.24.209']

CORS_ALLOWED_ORIGINS = [
    "http://185.195.24.209",     # публичный IP
    "http://localhost:3000",     # если тестируешь с локального React
]

# Добавляем настройки для статических файлов
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'),
]

STATIC_ROOT = '/var/www/static'

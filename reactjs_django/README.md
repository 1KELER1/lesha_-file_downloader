# React Frontend для Django File Downloader

## Разработка

1. Установите зависимости:
```bash
npm install
```

2. Запустите приложение в режиме разработки:
```bash
npm start
```

По умолчанию, приложение будет подключаться к бэкенду по адресу `http://127.0.0.1:8000` (указано в файле `.env`).

## Переменные окружения

Приложение использует переменные окружения для настройки API URL:

- `.env` - базовая конфигурация для разработки
- `.env.production` - конфигурация для продакшн-среды (используется при `npm run build`)

Основные переменные:
- `REACT_APP_API_URL` - базовый URL API (например, `http://127.0.0.1:8000` для разработки или пустая строка для продакшн)

## Деплой на продакшн

1. Сборка для продакшн:
```bash
npm run build
```

При сборке будет использован файл `.env.production`, где `REACT_APP_API_URL` пустой, что означает использование относительных путей для API.

2. Загрузите содержимое папки `build` на сервер в директорию `/var/www/html/build/`

3. Настройка Nginx для обслуживания React приложения и проксирования API запросов:
```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    # React static files
    location ^~ /static/ {
        alias /var/www/html/build/static/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Django static files
    location ^~ /staticfiles/ {
        alias /var/www/static/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Django media files
    location /media/ {
        alias /path/to/your/django/media/;
        expires 30d;
    }

    # Django admin
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # All other requests go to React SPA
    location / {
        root /var/www/html/build/;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

## Смена API URL

Для изменения URL API в режиме разработки, отредактируйте файл `.env`:
```
REACT_APP_API_URL=http://новый_ip:порт
```

Для продакшн, файл `.env.production` можно оставить с пустым `REACT_APP_API_URL` для использования относительных путей.


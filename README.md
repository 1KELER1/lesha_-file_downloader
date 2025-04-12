# Django 4 и React JS 18 - Приложение загрузки и скачивания файлов с JWT авторизацией

Это веб-приложение позволяет пользователям загружать файлы на сервер, просматривать и скачивать их. Для использования системы требуется авторизация. Приложение использует Django REST framework на бэкенде и React на фронтенде.

![Скриншот приложения](https://via.placeholder.com/800x400?text=Скриншот+приложения)

## Функциональность

- 🔐 Авторизация и регистрация через JWT токены
- 📤 Загрузка файлов любого формата
- 📋 Просмотр списка загруженных файлов
- 📥 Скачивание файлов с сохранением правильных расширений
- 👤 Управление профилем пользователя

## Технологии

### Бэкенд
- Python 3.8+
- Django 4.x
- Django REST framework
- djangorestframework-simplejwt
- SQLite (для хранения данных)

### Фронтенд
- React 18
- React Router Dom 6
- Axios (для API запросов)
- Bootstrap 5 (для стилизации)

## Установка и запуск

### Требования
- Python 3.8+
- Node.js 18+
- npm 9+

### Шаг 1: Подготовка и запуск бэкенда (Django)

1. Клонируйте репозиторий:
   ```bash
   git clone [URL_РЕПОЗИТОРИЯ]
   cd Django-4-and-React-JS-18-File-Upload-and-Download
   ```

2. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   ```

3. Активируйте виртуальное окружение:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   pip install djangorestframework-simplejwt
   ```

5. Подготовьте базу данных:
   ```bash
   cd django_reactjs
   python manage.py migrate
   ```

6. Создайте суперпользователя для админ-панели:
   ```bash
   python manage.py createsuperuser
   ```
   Следуйте инструкциям для создания учетной записи администратора.

7. Запустите сервер Django:
   ```bash
   python manage.py runserver
   ```
   Сервер будет запущен по адресу: http://127.0.0.1:8000

### Шаг 2: Запуск фронтенда (React)

1. Откройте новое окно терминала

2. Перейдите в папку с React-приложением:
   ```bash
   cd Django-4-and-React-JS-18-File-Upload-and-Download/reactjs_django
   ```

3. Установите зависимости:
   ```bash
   npm install
   ```

4. Если вы используете Node.js версии 17+, добавьте параметр для совместимости:
   - Windows:
     ```bash
     set NODE_OPTIONS=--openssl-legacy-provider
     ```
   - Linux/Mac:
     ```bash
     export NODE_OPTIONS=--openssl-legacy-provider
     ```

5. Запустите приложение:
   ```bash
   npm start
   ```

6. Приложение будет доступно по адресу: http://localhost:3000

## Использование приложения

1. Сначала создайте учетную запись, перейдя на http://localhost:3000/register

2. После регистрации войдите в систему на странице http://localhost:3000/login

3. После успешной авторизации вы будете перенаправлены на главную страницу, где можно:
   - Загружать файлы любых форматов
   - Просматривать список загруженных файлов
   - Скачивать файлы
   - Управлять своей учетной записью

4. Для управления проектом через админ-панель перейдите на http://127.0.0.1:8000/admin и введите данные суперпользователя

## Структура проекта

```
Django-4-and-React-JS-18-File-Upload-and-Download/
├── django_reactjs/          # Django бэкенд
│   ├── core/                # Django приложение для API файлов и авторизации
│   ├── django_reactjs/      # Настройки Django проекта
│   ├── media/               # Хранилище загруженных файлов
│   └── manage.py            # Скрипт управления Django
│
└── reactjs_django/          # React фронтенд
    ├── public/              # Статические файлы React
    ├── src/                 # Исходный код React
    │   ├── components/      # React компоненты
    │   └── resources/       # Ресурсы (CSS, изображения)
    └── package.json         # Конфигурация NPM
```

## Решение проблем

- **Ошибка с конфигурацией браузеров**: Если появляется ошибка `.browserslistrc` и настроек в `package.json`, удалите один из этих файлов.
- **Ошибка OpenSSL**: Если вы используете Node.js v17+, добавьте флаг `--openssl-legacy-provider` как указано в инструкции выше.
- **Проблемы с CORS**: Если API возвращает ошибки CORS, проверьте настройки CORS в `settings.py`.

## Вклад в проект

1. Сделайте форк проекта
2. Создайте ветку для новой функциональности: `git checkout -b feature/amazing-feature`
3. Зафиксируйте изменения: `git commit -m 'Add some amazing feature'`
4. Отправьте ветку в свой форк: `git push origin feature/amazing-feature`
5. Создайте Pull Request

## Лицензия

Распространяется под лицензией MIT. См. файл `LICENSE` для получения дополнительной информации. 
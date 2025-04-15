#!/usr/bin/env python
"""
Скрипт для создания профилей для всех существующих пользователей.
Запустите его с помощью:
python manage.py shell < create_profiles.py
"""

from django.contrib.auth.models import User
from core.models import Profile

# Создаем профили для пользователей, у которых их еще нет
users_without_profile = []
for user in User.objects.all():
    try:
        # Проверяем, есть ли у пользователя профиль
        profile = user.profile
        print(f"У пользователя {user.username} уже есть профиль.")
    except Profile.DoesNotExist:
        # Если профиля нет, создаем новый
        Profile.objects.create(user=user)
        users_without_profile.append(user.username)
        print(f"Создан профиль для пользователя {user.username}")

if not users_without_profile:
    print("Все пользователи уже имеют профили")
else:
    print(f"Создано {len(users_without_profile)} профилей для пользователей: {', '.join(users_without_profile)}") 
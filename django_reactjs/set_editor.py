
#!/usr/bin/env python
"""
Скрипт для назначения роли EDITOR пользователю.
Запустите его с помощью:
python manage.py shell < set_editor.py
"""

from django.contrib.auth.models import User
from core.models import Profile

# Имя пользователя для назначения роли редактора
USERNAME = 'redactor'  # Замените на нужное имя пользователя

try:
    # Получаем пользователя
    user = User.objects.get(username=USERNAME)
    
    # Назначаем пользователю is_staff=True для доступа к админке
    user.is_staff = True
    user.save()
    
    # Получаем или создаем профиль
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Устанавливаем роль EDITOR
    profile.role = 'EDITOR'
    profile.save()
    
    print(f"Пользователю {user.username} успешно назначена роль EDITOR")
    print(f"is_staff: {user.is_staff}")
    print(f"Роль: {profile.get_role_display()}")

except User.DoesNotExist:
    print(f"Пользователь с именем {USERNAME} не найден")
except Exception as e:
    print(f"Произошла ошибка: {str(e)}") 
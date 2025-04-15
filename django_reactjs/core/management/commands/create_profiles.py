from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile

class Command(BaseCommand):
    help = 'Создает профили для всех пользователей, у которых их еще нет'

    def handle(self, *args, **options):
        users_without_profile = []
        for user in User.objects.all():
            try:
                # Проверяем, есть ли у пользователя профиль
                profile = user.profile
            except Profile.DoesNotExist:
                # Если профиля нет, добавляем пользователя в список
                users_without_profile.append(user)
                
        # Создаем профили для пользователей из списка
        for user in users_without_profile:
            Profile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Профиль создан для пользователя {user.username}'))
            
        if not users_without_profile:
            self.stdout.write(self.style.SUCCESS('Все пользователи уже имеют профили'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Создано {len(users_without_profile)} профилей')) 
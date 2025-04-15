from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    class Role(models.TextChoices):
        VISITOR = 'VISITOR', _('Посетитель')
        EDITOR = 'EDITOR', _('Редактор')
        ADMIN = 'ADMIN', _('Администратор')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.VISITOR,
        verbose_name=_('Роль')
    )

    class Meta:
        verbose_name = _('Профиль')
        verbose_name_plural = _('Профили')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Проверяем, существует ли профиль уже
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except Profile.DoesNotExist:
        # Если профиля нет, создаем его
        Profile.objects.create(user=instance)

class Files(models.Model):
    pdf = models.FileField(upload_to='store/pdfs/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    is_public = models.BooleanField(default=True, verbose_name=_('Общедоступный'))

    def __str__(self):
        return str(self.pdf)

    class Meta:
        verbose_name = _('Файл')
        verbose_name_plural = _('Файлы')

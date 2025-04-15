from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission, Group
from .models import Files, Profile

# Расширяем стандартный UserAdmin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_filter = ('profile__role', 'is_staff', 'is_superuser')
    
    def get_role(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return 'Нет профиля'
    get_role.short_description = 'Роль'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Если пользователь суперадмин, показываем всех пользователей
        if request.user.is_superuser:
            return qs
        # Если пользователь редактор, показываем только обычных пользователей и редакторов
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            return qs.filter(is_superuser=False)
        return qs
    
    def has_change_permission(self, request, obj=None):
        # Если пользователь суперадмин, разрешаем всё
        if request.user.is_superuser:
            return True
        # Если пользователь редактор
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            # Если объект не указан (список пользователей), разрешаем
            if obj is None:
                return True
            # Если редактируем обычного пользователя или редактора, разрешаем
            if not obj.is_superuser:
                return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Если пользователь суперадмин, разрешаем всё
        if request.user.is_superuser:
            return True
        # Редакторам разрешаем удалять только обычных пользователей
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            if obj is None:
                return True
            if hasattr(obj, 'profile') and obj.profile.role == 'VISITOR':
                return True
        return False
    
    def has_add_permission(self, request):
        # Суперадмины и редакторы могут добавлять пользователей
        return request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR')
    
    def save_model(self, request, obj, form, change):
        # Сохраняем модель
        super().save_model(request, obj, form, change)
        
        # Если пользователь редактор, и мы создаем новую запись
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR' and not change:
            # Даем доступ к админке
            obj.is_staff = True
            obj.save()
            
            # После сохранения создаем или обновляем профиль
            profile, created = Profile.objects.get_or_create(user=obj)
            # По умолчанию - посетитель
            profile.role = 'VISITOR'
            profile.save()

    def has_view_permission(self, request, obj=None):
        # Редакторы всегда могут просматривать пользователей
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            return True
        return super().has_view_permission(request, obj)

# Регистрируем модель Files
@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('pdf', 'owner', 'is_public')
    list_filter = ('is_public',)
    search_fields = ('pdf', 'owner__username')
    
    def has_change_permission(self, request, obj=None):
        # Суперадмины могут менять все файлы
        if request.user.is_superuser:
            return True
        # Редакторы могут менять любые файлы
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            return True
        # Обычные пользователи могут менять только свои файлы
        if obj is not None and obj.owner == request.user:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        # То же, что и для редактирования
        return self.has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        # Редакторы всегда могут просматривать файлы
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            return True
        return super().has_view_permission(request, obj)

# Регистрируем модель Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Имя пользователя'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Если пользователь суперадмин, показываем все профили
        if request.user.is_superuser:
            return qs
        # Если пользователь редактор, показываем только профили обычных пользователей и редакторов
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            return qs.exclude(role='ADMIN')
        return qs
    
    def has_change_permission(self, request, obj=None):
        # Суперадмины могут менять все профили
        if request.user.is_superuser:
            return True
        # Редакторы могут менять профили обычных пользователей и редакторов
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            if obj is None:
                return True
            return obj.role != 'ADMIN'
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Аналогично правам на изменение
        return self.has_change_permission(request, obj)
    
    def has_add_permission(self, request):
        # Только суперадмины могут создавать профили напрямую
        return request.user.is_superuser
    
    def save_model(self, request, obj, form, change):
        # Редакторы не могут повышать роль до ADMIN
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            if obj.role == 'ADMIN':
                obj.role = 'EDITOR'  # Понижаем до редактора
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        # Редакторы всегда могут просматривать профили
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            return True
        return super().has_view_permission(request, obj)

# Отменяем регистрацию стандартного UserAdmin и регистрируем наш CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Скрываем модели Group и Permission от редакторов
class GroupAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

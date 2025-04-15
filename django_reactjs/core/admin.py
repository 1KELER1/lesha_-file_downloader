from django.contrib import admin
from .models import Files, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Имя пользователя'

@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('pdf', 'owner', 'is_public')
    list_filter = ('is_public',)
    search_fields = ('pdf', 'owner__username')

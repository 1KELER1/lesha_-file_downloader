from django.http import HttpResponseForbidden
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

class RoleMiddleware(MiddlewareMixin):
    """
    Middleware для проверки ролей пользователей при доступе к админ-панели.
    Разрешает доступ только администраторам и редакторам.
    """
    
    def process_request(self, request):
        # Проверяем, идет ли запрос к админ-панели
        if request.path.startswith('/admin/'):
            # Если пользователь не аутентифицирован, пропускаем (Django сам перенаправит на страницу входа)
            if not request.user.is_authenticated:
                return None
                
            # Суперпользователям разрешаем всё
            if request.user.is_superuser:
                return None
                
            # Проверяем, является ли пользователь сотрудником (имеет доступ к админке)
            if not request.user.is_staff:
                return HttpResponseForbidden("У вас нет доступа к админ-панели")
                
            # Проверяем роль пользователя - должен быть редактор или админ
            try:
                if hasattr(request.user, 'profile'):
                    if request.user.profile.role in ['EDITOR', 'ADMIN']:
                        return None
            except Exception as e:
                # Если произошла ошибка, разрешаем доступ is_staff пользователям
                # для отладки и чтобы избежать блокировки легитимных пользователей
                print(f"Ошибка при проверке профиля: {str(e)}")
                return None
                    
            # В остальных случаях запрещаем доступ
            return HttpResponseForbidden("У вас недостаточно прав для доступа к админ-панели")
            
        return None 
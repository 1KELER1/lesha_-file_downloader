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
                    # Отладочная информация
                    print(f"User: {request.user.username}, Role: {request.user.profile.role}, Staff: {request.user.is_staff}")
                    if request.user.profile.role in ['EDITOR', 'ADMIN']:
                        # Редакторы и админы имеют доступ
                        return None
                    else:
                        # У пользователя есть профиль, но неверная роль
                        print(f"Access denied: user {request.user.username} has role {request.user.profile.role}")
                else:
                    # У пользователя нет профиля
                    print(f"Access denied: user {request.user.username} has no profile")
            except Exception as e:
                # Если произошла ошибка, логируем и пропускаем для отладки
                print(f"Ошибка при проверке профиля: {str(e)}")
                return None
                    
            # В остальных случаях запрещаем доступ
            return HttpResponseForbidden("У вас недостаточно прав для доступа к админ-панели")
            
        return None 

class EditorRoleRestrictionMiddleware(MiddlewareMixin):
    """
    Middleware для ограничения доступа редакторов к роли администратора.
    """
    
    def process_response(self, request, response):
        # Проверяем только для авторизованных пользователей-редакторов
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            # Если страница - HTML и в ней есть выпадающий список ролей
            if 'text/html' in response.get('Content-Type', '') and b'<select' in response.content:
                # Добавляем JavaScript в конец страницы для скрытия опции "Администратор"
                script = """
                <script>
                document.addEventListener('DOMContentLoaded', function() {
                    // Найти все выпадающие списки ролей
                    var roleSelects = document.querySelectorAll('select[name*="role"]');
                    
                    roleSelects.forEach(function(select) {
                        // Найти опцию "Администратор" и скрыть её
                        for (var i = 0; i < select.options.length; i++) {
                            if (select.options[i].value === 'ADMIN' || select.options[i].text === 'Администратор') {
                                select.options[i].disabled = true;
                                select.options[i].style.display = 'none';
                            }
                        }
                    });
                });
                </script>
                """
                
                # Вставляем скрипт перед закрывающим тегом body
                response.content = response.content.replace(b'</body>', script.encode('utf-8') + b'</body>')
        
        return response 
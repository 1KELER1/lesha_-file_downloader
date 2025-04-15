from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .models import Files, Profile

def is_editor(user):
    """Проверяет, имеет ли пользователь роль редактора"""
    if not user.is_authenticated:
        return False
    return hasattr(user, 'profile') and user.profile.role in ['EDITOR', 'ADMIN']

@login_required
def editor_dashboard(request):
    """Панель управления для редакторов"""
    if not is_editor(request.user):
        return HttpResponseForbidden("Доступ запрещен. Требуется роль редактора.")
    
    # Получаем все файлы
    files = Files.objects.all()
    
    # Получаем всех пользователей (кроме админов)
    users = User.objects.filter(is_superuser=False)
    
    context = {
        'files': files,
        'users': users,
    }
    
    return render(request, 'core/editor_dashboard.html', context)

@login_required
def file_list(request):
    """Список всех файлов"""
    if not is_editor(request.user):
        return HttpResponseForbidden("Доступ запрещен. Требуется роль редактора.")
    
    files = Files.objects.all()
    
    return render(request, 'core/file_list.html', {'files': files})

@login_required
def user_list(request):
    """Список всех пользователей"""
    if not is_editor(request.user):
        return HttpResponseForbidden("Доступ запрещен. Требуется роль редактора.")
    
    users = User.objects.filter(is_superuser=False)
    
    return render(request, 'core/user_list.html', {'users': users})

@login_required
def toggle_file_public(request, file_id):
    """Переключение статуса публичности файла"""
    if not is_editor(request.user):
        return HttpResponseForbidden("Доступ запрещен. Требуется роль редактора.")
    
    file = get_object_or_404(Files, id=file_id)
    file.is_public = not file.is_public
    file.save()
    
    return redirect('file_list')

@login_required
def promote_to_editor(request, user_id):
    """Повышение пользователя до редактора"""
    if not is_editor(request.user):
        return HttpResponseForbidden("Доступ запрещен. Требуется роль редактора.")
    
    user = get_object_or_404(User, id=user_id)
    
    # Пользователь не может повысить себя
    if user == request.user:
        return HttpResponseForbidden("Вы не можете изменить свою роль.")
    
    # Нельзя повысить админа
    if user.is_superuser:
        return HttpResponseForbidden("Вы не можете изменить роль администратора.")
    
    # Устанавливаем права доступа к админке
    user.is_staff = True
    user.save()
    
    # Устанавливаем роль EDITOR
    profile, created = Profile.objects.get_or_create(user=user)
    profile.role = 'EDITOR'
    profile.save()
    
    return redirect('user_list')

@login_required
def delete_file(request, file_id):
    """Удаление файла"""
    if not is_editor(request.user):
        return HttpResponseForbidden("Доступ запрещен. Требуется роль редактора.")
    
    file = get_object_or_404(Files, id=file_id)
    
    # Проверяем, является ли пользователь владельцем файла или редактором
    if file.owner == request.user or request.user.profile.role == 'ADMIN':
        file.delete()
    else:
        return HttpResponseForbidden("Вы можете удалять только свои файлы.")
    
    return redirect('file_list')

@login_required
def delete_user(request, user_id):
    """Удаление пользователя"""
    if not is_editor(request.user):
        return HttpResponseForbidden("Доступ запрещен. Требуется роль редактора.")
    
    user_to_delete = get_object_or_404(User, id=user_id)
    
    # Нельзя удалить себя
    if user_to_delete == request.user:
        return HttpResponseForbidden("Вы не можете удалить свою учетную запись.")
    
    # Нельзя удалить админа
    if user_to_delete.is_superuser:
        return HttpResponseForbidden("Вы не можете удалить администратора.")
    
    # Редактор может удалять только обычных пользователей
    if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
        if hasattr(user_to_delete, 'profile') and user_to_delete.profile.role == 'EDITOR':
            return HttpResponseForbidden("Вы не можете удалить другого редактора.")
    
    # Удаляем пользователя
    user_to_delete.delete()
    
    return redirect('user_list') 
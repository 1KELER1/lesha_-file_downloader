from django.shortcuts import render
from .models import Files, User, Profile
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .serializers import FilesSerializer, UserSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsEditorOrAdmin, IsAdmin, IsPublicOrHasAccess

# Create your views here.

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    permission_classes = [IsPublicOrHasAccess]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'profile') and self.request.user.profile.role in ['EDITOR', 'ADMIN']:
                return Files.objects.all()
            return Files.objects.filter(is_public=True) | Files.objects.filter(owner=self.request.user)
        return Files.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsEditorOrAdmin])
    def toggle_public(self, request, pk=None):
        file = self.get_object()
        file.is_public = not file.is_public
        file.save()
        return Response({'status': 'success', 'is_public': file.is_public})

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_file(self, request, pk=None):
        file = self.get_object()
        # Проверяем, является ли пользователь владельцем файла или администратором
        if file.owner == request.user or (hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN'):
            file.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "У вас нет прав для удаления этого файла"}, status=status.HTTP_403_FORBIDDEN)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([IsEditorOrAdmin])
def promote_to_editor(request, pk):
    """
    Повышение пользователя до редактора.
    Только администраторы и редакторы могут вызывать этот метод.
    """
    try:
        user = User.objects.get(pk=pk)
        
        # Проверяем, имеет ли текущий пользователь право повысить роль
        if hasattr(request.user, 'profile') and request.user.profile.role == 'EDITOR':
            # Редакторы могут повышать только обычных пользователей
            if hasattr(user, 'profile') and user.profile.role != 'VISITOR':
                return Response({"error": "Редакторы могут повышать только обычных пользователей"},
                               status=status.HTTP_403_FORBIDDEN)
                               
            # Редакторы могут только повышать до роли редактора, но не администратора
            requested_role = request.data.get('role', 'EDITOR')
            if requested_role == 'ADMIN':
                return Response({"error": "Редакторы не могут назначать роль администратора"},
                                status=status.HTTP_403_FORBIDDEN)
        
        # Даем пользователю права доступа к админке
        user.is_staff = True
        user.save()
        
        # Устанавливаем роль EDITOR
        if hasattr(user, 'profile'):
            # Если текущий пользователь администратор, он может назначить любую роль
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN'):
                user.profile.role = request.data.get('role', 'EDITOR')
            else:
                # Иначе можно назначить только роль EDITOR
                user.profile.role = 'EDITOR'
            user.profile.save()
        
        return Response({"status": "success", "message": f"Пользователь {user.username} повышен до редактора"})
    except User.DoesNotExist:
        return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdmin])
def demote_to_visitor(request, pk):
    """
    Понижение пользователя до обычного пользователя.
    Только администраторы могут вызывать этот метод.
    """
    try:
        user = User.objects.get(pk=pk)
        
        # Убираем права доступа к админке
        user.is_staff = False
        user.save()
        
        # Устанавливаем роль VISITOR
        if hasattr(user, 'profile'):
            user.profile.role = 'VISITOR'
            user.profile.save()
        
        return Response({"status": "success", "message": f"Пользователь {user.username} понижен до посетителя"})
    except User.DoesNotExist:
        return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

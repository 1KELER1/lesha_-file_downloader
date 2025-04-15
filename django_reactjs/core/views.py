from django.shortcuts import render
from .models import Files, User, Profile
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
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

    @action(detail=True, methods=['delete'], permission_classes=[IsAdmin])
    def delete_file(self, request, pk=None):
        file = self.get_object()
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

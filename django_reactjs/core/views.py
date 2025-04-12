from django.shortcuts import render
from .models import Files
from rest_framework import viewsets, generics, permissions
from .serializers import FilesSerializer, UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи могут получить доступ

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

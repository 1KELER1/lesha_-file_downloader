from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FilesViewSet, RegisterView, UserDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('files', FilesViewSet, basename='files')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/user/', UserDetailView.as_view(), name='user_info'),
]

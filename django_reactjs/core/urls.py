from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FilesViewSet, RegisterView, UserDetailView, promote_to_editor, demote_to_visitor
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .editor_views import editor_dashboard, file_list, user_list, toggle_file_public, promote_to_editor as editor_promote

router = DefaultRouter()
router.register('files', FilesViewSet, basename='files')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/user/', UserDetailView.as_view(), name='user_info'),
    path('api/users/<int:pk>/promote-to-editor/', promote_to_editor, name='promote_to_editor'),
    path('api/users/<int:pk>/demote-to-visitor/', demote_to_visitor, name='demote_to_visitor'),
    path('editor/', editor_dashboard, name='editor_dashboard'),
    path('editor/files/', file_list, name='file_list'),
    path('editor/users/', user_list, name='user_list'),
    path('editor/files/<int:file_id>/toggle-public/', toggle_file_public, name='toggle_file_public'),
    path('editor/users/<int:user_id>/promote/', editor_promote, name='editor_promote'),
]

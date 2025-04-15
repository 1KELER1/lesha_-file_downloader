from rest_framework import permissions

class IsEditorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'profile') and (
            request.user.profile.role in ['EDITOR', 'ADMIN']
        )

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'profile') and (
            request.user.profile.role == 'ADMIN'
        )

class IsPublicOrHasAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return request.user and request.user.is_authenticated and (
            request.user == obj.owner or 
            (hasattr(request.user, 'profile') and request.user.profile.role in ['EDITOR', 'ADMIN'])
        ) 
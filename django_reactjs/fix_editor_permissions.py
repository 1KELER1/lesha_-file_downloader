"""
Script to fix editor permissions
Run directly: python fix_editor_permissions.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_reactjs.settings')
django.setup()

# Import models
from django.contrib.auth.models import User, Permission
from core.models import Profile

# Username to fix
USERNAME = 'redactor'  # Change to your username

try:
    # Get user
    user = User.objects.get(username=USERNAME)
    
    # Make sure user is staff
    user.is_staff = True
    
    # Give user all permissions to core models
    app_models = ['files', 'profile']
    for model in app_models:
        for perm_type in ['add', 'change', 'delete', 'view']:
            codename = f"{perm_type}_{model}"
            try:
                perm = Permission.objects.get(codename=codename)
                user.user_permissions.add(perm)
                print(f"Added permission: {perm.codename}")
            except Permission.DoesNotExist:
                print(f"Permission {codename} does not exist")
    
    # Save user
    user.save()
    
    # Verify profile
    profile, created = Profile.objects.get_or_create(user=user)
    profile.role = 'EDITOR'
    profile.save()
    
    print(f"\nPermissions fixed for user {user.username}")
    print(f"is_staff: {user.is_staff}")
    print(f"Role: {profile.get_role_display()}")
    print(f"Permissions: {list(user.user_permissions.values_list('codename', flat=True))}")
    
    print("\nIf the admin panel is still empty, try:")
    print("1. Restart the Django server")
    print("2. Clear browser cache or use incognito mode")
    print("3. If using firefox, try using Chrome/Edge")

except User.DoesNotExist:
    print(f"User {USERNAME} not found")
except Exception as e:
    print(f"Error: {str(e)}")

# Wait for input before closing
input("Press Enter to exit...") 
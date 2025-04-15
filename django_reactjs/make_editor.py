"""
Script for making user an Editor
Run directly: python make_editor.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_reactjs.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from core.models import Profile

# Username to set as editor
USERNAME = 'redactor'  # Change to your username

try:
    # Get user
    user = User.objects.get(username=USERNAME)
    
    # Set is_staff=True for admin access
    user.is_staff = True
    user.save()
    
    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Set EDITOR role
    profile.role = 'EDITOR'
    profile.save()
    
    print(f"User {user.username} successfully granted EDITOR role")
    print(f"is_staff: {user.is_staff}")
    print(f"Role: {profile.get_role_display()}")

except User.DoesNotExist:
    print(f"User {USERNAME} not found")
except Exception as e:
    print(f"Error: {str(e)}")

# Wait for input before closing
input("Press Enter to exit...") 
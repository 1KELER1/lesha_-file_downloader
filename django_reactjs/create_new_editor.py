"""
Script for creating a new editor user
Run directly: python create_new_editor.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_reactjs.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from core.models import Profile

# Editor details
USERNAME = 'editor1'
PASSWORD = 'editor123'
EMAIL = 'editor@example.com'

try:
    # Check if user already exists
    try:
        User.objects.get(username=USERNAME)
        print(f"User {USERNAME} already exists!")
    except User.DoesNotExist:
        # Create new user
        user = User.objects.create_user(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD
        )
        
        # Set as staff member for admin access
        user.is_staff = True
        user.save()
        
        # Create profile with EDITOR role
        profile = Profile.objects.create(user=user, role='EDITOR')
        
        print(f"Created new editor user: {USERNAME}")
        print(f"Password: {PASSWORD}")
        print(f"Email: {EMAIL}")
        print(f"is_staff: {user.is_staff}")
        print(f"Role: {profile.get_role_display()}")
        print("\nYou can now log in to the admin panel with these credentials")

except Exception as e:
    print(f"Error: {str(e)}")

# Wait for input before closing
input("Press Enter to exit...") 
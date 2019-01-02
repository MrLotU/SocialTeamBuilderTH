from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserCreateForm(UserCreationForm):
    """User creation form"""
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

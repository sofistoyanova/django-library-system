from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# forms.ModelForm - allow to work with specific database model
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_staff']
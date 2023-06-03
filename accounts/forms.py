from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=128, required=True, help_text='Email required. Please, enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
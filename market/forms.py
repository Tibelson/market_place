from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):

    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username','password']
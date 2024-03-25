from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from captcha.fields import CaptchaField 


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class CaptchaAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()


 


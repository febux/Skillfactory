from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    # verification_code = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

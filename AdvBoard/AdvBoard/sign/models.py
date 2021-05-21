from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class OneTimeCode(models.Model):
    code = models.TextField(unique=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def get_code(self):
        return self.code

# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .base import BaseAuth, MyAuthException


class AuthForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def login_user(self, request):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        print('login = ', login)

        password = cleaned_data.get('password')
        print('password = ', password)
        BaseAuth.login(request, login, password)

    def clean(self):
        cleaned_data = super(AuthForm, self).clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')
        if not BaseAuth.correct_login(login) or not BaseAuth.correct_password(password):
            raise forms.ValidationError("Empty field")
        return cleaned_data

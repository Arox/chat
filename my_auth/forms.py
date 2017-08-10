# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .base import BaseAuth, MyAuthException, DoesNotExistUser


class AuthForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def login_user(self, request):
        cleaned_data = super().clean()
        if self.is_valid():
            login = cleaned_data.get('login')
            password = cleaned_data.get('password')
            BaseAuth.login(request, login, password)

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')
        if not BaseAuth.correct_login(login) or not BaseAuth.correct_password(password):
            raise forms.ValidationError("Empty field")
        if not BaseAuth.has_login(login):
            raise forms.ValidationError("User does not exist")
        try:
            BaseAuth.get_user_by_name(login, password)
        except DoesNotExistUser:
            raise forms.ValidationError("User does not exist")
        return cleaned_data


class RegistrationForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()

    def registration_user(self, request):
        cleaned_data = super().clean()
        if self.is_valid():
            login = cleaned_data.get('login')
            password = cleaned_data.get('password')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            BaseAuth.create_user(login, password, first_name, last_name)

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')
        if not BaseAuth.correct_login(login) or not BaseAuth.correct_password(password):
            raise forms.ValidationError("Empty field")
        if BaseAuth.has_login(login):
            raise forms.ValidationError("Login exist")
        return cleaned_data

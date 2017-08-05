from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'last_name', 'is_active')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
            max_length=30,
            style={'placeholder': ''},
            label='Имя пользователя'
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': ''},
        label='Пароль'
    )

from .models import User
from django.contrib import auth


class MyAuthException(Exception):
    def __init__(self, message):
            super().__init__(message)


class NonCorrectLogin(MyAuthException):
    def __init__(self, login):
        super().__init__("Login is non correct. Data: %s" % login)


class NonCorrectPassword(MyAuthException):
    def __init__(self, password):
        super().__init__("Password is non correct. Data: %s" % password)


class DoesNotExistUser(MyAuthException):
    def __init__(self):
        super().__init__("User does not exist")


class BlockedUser(MyAuthException):
    def __init__(self):
        super().__init__("User is not active")


class BaseAuth(object):
    @staticmethod
    def get_user(request):
        user = auth.get_user(request)
        if user is None:
            raise DoesNotExistUser()
        return user

    @staticmethod
    def get_user_by_name(login, password):
        user = auth.authenticate(username=login, password=password)
        if user is None:
            raise DoesNotExistUser()
        return user

    @staticmethod
    def correct_login(data):
        return data is not None and len(data) > 0

    @staticmethod
    def is_login(request):
        user = BaseAuth.get_user(request)
        if user is not None:
            return user.is_authenticated()
        return False

    @staticmethod
    def correct_password(data):
        return data is not None and len(data) > 0

    @staticmethod
    def logout(request):
        if BaseAuth.is_login(request):
            auth.logout(request)

    @staticmethod
    def login(request, login, password):
        if BaseAuth.is_login(request):
            BaseAuth.logout(request)
        if BaseAuth.correct_login(login):
            if BaseAuth.correct_password(password):
                user = BaseAuth.get_user_by_name(login, password)
                if user.is_active:
                    auth.login(request, user)
                else:
                    raise BlockedUser
            else:
                raise NonCorrectPassword
        else:
            raise NonCorrectLogin


# class MyBackend(object):
#     @staticmethod
#     def authenticate(username=None, password=None):
#         try:
#             return MyUser.objects.get(username=username, password=password)
#         except MyUser.DoesNotExist:
#             return None
#
#     def get_user(self, user_id):
#         try:
#             return MyUser.objects.get(pk=user_id)
#         except MyUser.DoesNotExist:
#             return None
#
#     def has_perm(self, user_obj, perm, obj=None):
#         return False

from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .base import BaseAuth
# Create your views here.


class LoginView(APIView):
    """
    По логину и пароль осуществляет аутентификацию пользователя
    """
    def get_serializer_class(self):
        return LoginSerializer

    def get_success_url(self):
        next_url = self.request.GET['next'] if 'next' in self.request.GET else '/'
        return next_url

    def get(self, request):
        if request.is_ajax():
            username = request.data['username']
            password = request.data['password']
        else:
            # return error response
            pass

    def post(self, request):
        if request.is_ajax():
            try:
                serializer = self.get_serializer_class(data=request.data)
                if serializer.is_valid():
                    BaseAuth.login(request, login=serializer.data['username'], password=serializer.data['password'])
                else:
                    pass
                    # return ErrorResponse('LoginFailed',
                    #                      exception_value=None,
                    #                      status_message=status.HTTP_400_BAD_REQUEST,
                    #                      develop_message=str(serializer.errors))

            except MyAuthException as error:
                pass
                # return ErrorResponse('LoginFailed',
                #              exception_value=error,
                #              status_message=status.HTTP_403_FORBIDDEN)


            response = Response(status=status.HTTP_200_OK, content_type='application/json')
            response.set_cookie("user_id", request.user.id)
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AuthLogoutView(APIView):
    """
    Разлогиневает пользователя
    """
    def get_success_url(self):
        next_url = self.request.GET['next'] if 'next' in self.request.GET else '/'
        return next_url

    def get(self, request):
        if BaseAuth.is_login(request):
            BaseAuth.logout(request)
        return HttpResponseRedirect(self.get_success_url())
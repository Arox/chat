from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.AuthLogoutView.as_view(), name='logout'),
    url(r'^form/', views.AuthFormView.as_view(), name='form'),
    url(r'^registration/', views.RegistrationFormView.as_view(), name='registration'),
]

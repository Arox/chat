from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.AuthLogoutView.as_view(), name='logout'),
]

"""chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view
from django.views.generic import RedirectView

swagger_view = get_swagger_view(title='SWAGGER DOCS')

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/room/')),
    url(r'^auth/', include('my_auth.urls', namespace='auth', app_name='auth')),
    url(r'^room/', include('room.urls', namespace='room', app_name='room')),
    url(r'^docs/', swagger_view),
]

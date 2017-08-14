from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.WindowView.as_view(), name='main'),
    url(r'^add/$', views.RoomView.as_view(), name='create_room'),
    url(r'^users/(?P<pk>[0-9\-]+)/$', views.RoomUsersView.as_view(), name='users_room'),
    url(r'^messages/(?P<pk>[0-9\-]+)/$', views.RoomMessage.as_view(), name='messages_room'),
]

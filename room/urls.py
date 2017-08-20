from django.conf.urls import url, include
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', login_required(views.WindowView.as_view()), name='main'),
    url(r'^add/$', views.RoomView.as_view(), name='create_room'),
    url(r'^users/(?P<pk>[0-9\-]+)/$', views.RoomUsersView.as_view(), name='users_room'),
    url(r'^users/all/(?P<pk>[0-9\-]+)/$', views.ForRoomUsersView.as_view(), name='users_all'),
    url(r'^users/chat/(?P<room_pk>[0-9\-]+)/add/(?P<user_pk>[0-9\-]+)/$', views.RoomAddUserView.as_view(), name='user_add'),
    url(r'^users/chat/(?P<room_pk>[0-9\-]+)/add/admin/(?P<user_pk>[0-9\-]+)/$', views.RoomAddAdminView.as_view(), name='admin_add'),
    url(r'^users/chat/(?P<room_pk>[0-9\-]+)/remove/(?P<user_pk>[0-9\-]+)/$', views.RoomRemoveUserView.as_view(), name='user_remove'),
    url(r'^users/chat/(?P<room_pk>[0-9\-]+)/remove/admin/(?P<user_pk>[0-9\-]+)/$', views.RoomRemoveAdminView.as_view(), name='admin_remove'),
    url(r'^self/chat/(?P<room_pk>[0-9\-]+)/$', views.RoomUserInfoView.as_view(), name='self_info'),
    url(r'^messages/(?P<pk>[0-9\-]+)/$', views.RoomMessage.as_view(), name='messages_room'),
]

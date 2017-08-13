from django.http import HttpResponse
from rest_framework import status

from channels.handler import AsgiHandler
from channels import Group
import json
from django.contrib.sessions.models import Session
from my_auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from .models import Room


def pk_from_url(url: str):
    if url[-1] == '/':
        pk = url.split('/')[-2]
    else:
        pk = url.split('/')[-1]
    return pk


def get_user_by_session(session_id):
    session = Session.objects.get(session_key=session_id)
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')
    return User.objects.get(id=uid)


@channel_session_user_from_http
def connect_room(request):
    url: str = request.content['path']
    pk = pk_from_url(url)
    try:
        room = Room.objects.get(pk=pk, users__in=[request.user])
        request.reply_channel.send({"accept": True})
        Group('room{0}'.format(pk)).add(request.reply_channel)
    except Room.DoesNotExist:
        request.reply_channel.send({"accept": False})


def disconnect_room(request):
    url: str = request.content['path']
    pk = pk_from_url(url)
    Group('room{0}'.format(pk)).discard(request.reply_channel)


def send_room(request):
    body = json.loads(request.content['text'])
    print(body)
    url: str = request.content['path']
    pk = pk_from_url(url)
    Group('room{0}'.format(pk)).send({'text' : json.dumps(body)})

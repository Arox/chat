from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponse

import json

from .models import Room, ChatMessage
from my_auth.models import User

# Create your views here.


class WindowView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        kwargs['host'] = self.request.META['HTTP_HOST']
        if self.request.user.is_authenticated and isinstance(self.request.user, User):
            kwargs['rooms'] = Room.objects.filter(users__in = [self.request.user])
        return super().get_context_data(**kwargs)


class RoomView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, User):
            room_chat = Room(name=request.POST['name'])
            room_chat.save()
            room_chat.users.add(request.user)
            room_chat.admin.add(request.user)
            room_chat.save()
            return HttpResponse(json.dumps(dict(pk=room_chat.pk, name=room_chat.name)), status=201, content_type="application/json")
        return HttpResponse(status=400)


class RoomUserInfoView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, User):
            room = Room.objects.get(pk=kwargs['room_pk'])
            return HttpResponse(json.dumps({'is_admin': (request.user in room.admin.all())}), status=200, content_type="application/json")
        return HttpResponse(status=400)


class RoomUsersView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, User):
            room = Room.objects.get(pk=kwargs['pk'])
            users = User.objects.filter(pk__in=[x.pk for x in room.users.all()])
            admins = room.admin.all()
            result = [{'pk': x.pk, 'name': x.str_name, 'is_admin': x in admins} for x in users]
            return HttpResponse(json.dumps(result), status=200, content_type="application/json")
        return HttpResponse(status=400)


class ForRoomUsersView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, User):
            room = Room.objects.get(pk=kwargs['pk'])
            users = User.objects.exclude(pk__in=[x.pk for x in room.users.all()])
            result = [{'pk': x.pk, 'name': x.str_name} for x in users]
            return HttpResponse(json.dumps(result), status=200, content_type="application/json")
        return HttpResponse(status=400)


class RoomMessage(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, User):
            room = Room.objects.get(pk=kwargs['pk'])
            messages = ChatMessage.objects.filter(room=room).order_by('time')
            result = [{'time': str(x.time), 'user': x.author.str_name, 'message': x.text} for x in messages]
            return HttpResponse(json.dumps(result), status=200, content_type="application/json")
        return HttpResponse(status=400)


class RoomAddUserView(View):
    def post(self, request, room_pk, user_pk, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, User):
            room_chat = Room.objects.get(pk=room_pk)
            if request.user in room_chat.admin.all():
                user = User.objects.get(pk=user_pk)
                room_chat.users.add(user)
                room_chat.save()
                message = ChatMessage(text='add user: {}'.format(user.str_name), room=room_chat)
                message.author = request.user
                message.save()
                return HttpResponse(status=200)
        return HttpResponse(status=400)


class RoomAddAdminView(View):
    def post(self, request, room_pk, user_pk, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, User):
            room_chat = Room.objects.get(pk=room_pk)
            if request.user in room_chat.admin.all():
                user = User.objects.get(pk=user_pk)
                if user in room_chat.users.all():
                    room_chat.admin.add(user)
                    room_chat.save()
                    message = ChatMessage(text='set user admin: {}'.format(user.str_name), room=room_chat)
                    message.author = request.user
                    message.save()
                    return HttpResponse(status=200)
        return HttpResponse(status=400)


class RoomRemoveAdminView(View):
    def post(self, request, room_pk, user_pk, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, User):
            room_chat = Room.objects.get(pk=room_pk)
            if request.user in room_chat.admin.all():
                user = User.objects.get(pk=user_pk)
                if user in room_chat.users.all():
                    room_chat.admin.remove(user)
                    room_chat.save()
                    message = ChatMessage(text='unset user admin: {}'.format(user.str_name), room=room_chat)
                    message.author = request.user
                    message.save()
                    return HttpResponse(status=200)
        return HttpResponse(status=400)


class RoomRemoveUserView(View):
    def post(self, request, room_pk, user_pk, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, User):
            room_chat = Room.objects.get(pk=room_pk)
            if request.user in room_chat.admin.all() or request.user.pk == user_pk:
                user = User.objects.get(pk=user_pk)
                room_chat.users.remove(user)
                room_chat.save()
                message = ChatMessage(text='remove user: {}'.format(user.str_name), room=room_chat)
                message.author = request.user
                message.save()
                return HttpResponse(status=200)
        return HttpResponse(status=400)
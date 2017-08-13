from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponse

import json

from .models import Room
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
            room_chat.save()
            return HttpResponse(status=201)
        return HttpResponse(status=400)


class RoomUsersView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, User):
            room = Room.objects.get(pk=kwargs['pk'])
            users = User.objects.filter(pk__in=[x.pk for x in room.users.all()])
            result = ['{} {}'.format(x.first_name, x.last_name) for x in users]
            return HttpResponse(json.dumps(result), status=200, content_type="application/json")
        return HttpResponse(status=400)
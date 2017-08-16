from django.db import models
from my_auth.models import User
# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    users = models.ManyToManyField(to=User)
    admin = models.ForeignKey(to=User, related_name='admin')


class ChatMessage(models.Model):
    author = models.ForeignKey(to=User, null=False)
    time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)
    room = models.ForeignKey(to=Room)

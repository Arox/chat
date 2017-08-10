from django.db import models
from my_auth.models import User
# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    users = models.ManyToManyField(to=User)

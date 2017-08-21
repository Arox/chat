from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class InvalidUserData(Exception):
        pass

    def save(self, *args, **kwargs):
        if len(self.password) < 1 or len(self.username) < 1:
            raise User.InvalidUserData()
        return super().save(*args, **kwargs)

    @property
    def str_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

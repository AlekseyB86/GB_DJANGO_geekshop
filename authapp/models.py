from datetime import timedelta, datetime

import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'null': True, 'blank': True}


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='Аватар')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', default=18)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_created = models.DateTimeField(auto_now_add=True, **NULLABLE)

    def is_activation_key_expired(self):
        return datetime.now(pytz.timezone(settings.TIME_ZONE)) >= self.activation_key_created + timedelta(hours=48)

    def delete(self, using=None, keep_parents=False):
        self.is_active = not self.is_active
        self.save()

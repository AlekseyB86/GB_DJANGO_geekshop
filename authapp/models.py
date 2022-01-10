from datetime import timedelta, datetime

import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE, unique=True, db_index=True)
    tagline = models.CharField(max_length=150, blank=True, verbose_name='тэги')
    about_me = models.TextField(blank=True, verbose_name='о себе')
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=1, verbose_name='пол')

    # В db лежит
    # user_profile.gender
    # W
    # в шаблонах в отображении
    # user_profile.get_gender_display()
    # user_profile.get_gender_display
    # Ж

#     Сигналы
    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()


from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_for_products')
def media_for_products(img_path):
    if not img_path:
        img_path = 'products/product_default.jpg'

    return f'{settings.MEDIA_URL}{img_path}'


@register.filter(name='media_for_users')
def media_for_users(img_path):
    if not img_path:
        img_path = 'users_avatars/user_default.png'

    return f'{settings.MEDIA_URL}{img_path}'

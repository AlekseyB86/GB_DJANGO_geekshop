from datetime import datetime, timedelta

import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    """Парсит данные о пользователе из ВК и записывает в профиль"""

    if backend.name != 'vk-oauth2':
        return

    # api_url = urlunparse(('https',
    #                       'api.vk.com',
    #                       '/method/users.get',
    #                       None,
    #                       urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
    #                                             access_token=response['access_token'],
    #                                             v='5.131')),
    #                       None
    #                       ))

    # api_url = f'{settings.VK_API_URL}method/users.get/'
    # fields_list = ['bdate', 'sex', 'about']
    # params = {
    #     "fields": ",".join(fields_list),
    #     "access_token": response["access_token"],
    #     "v": "5.131"
    # }
    # requests.get(api_url, params=params)

    api_url = f'http://api.vk.com/method/users.get/?fields=bdate,sex,about&access_token={response["access_token"]}&v=5.92'

    response = requests.get(api_url)
    if response.status_code != 200:
        return

    data = response.json()['response'][0]

    # сохраняем в профиль пол пользователя
    if 'sex' in data:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE

    # сохраняем в профиль "обо мне" пользователя
    if 'about' in data:
        user.shopuserprofile.about_me = data['about']

    # сохраняем в профиль кол-во лет пользователя, если меньше 18 - удаляем его
    if 'bdate' in data:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = (date.today() - bdate) // timedelta(days=365.2425)
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    user.save()

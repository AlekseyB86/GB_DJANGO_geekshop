from datetime import datetime, timedelta, date

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
    #                                             v='5.92')),
    #                       None
    #                       ))

    # api_url = f'{settings.VK_API_URL}method/users.get/'
    # fields_list = ['bdate', 'sex', 'about']
    # params = {
    #     "fields": ",".join(fields_list),
    #     "access_token": response["access_token"],
    #     "v": "5.92"
    # }
    # requests.get(api_url, params=params)

    api_url = f'http://api.vk.com/method/users.get/?fields=bdate,sex,about,photo_max_orig&access_token={response["access_token"]}&v=5.92'

    response = requests.get(api_url)
    if response.status_code != 200:
        return

    data = response.json()['response'][0]

    # сохраняем в профиль пол пользователя
    if data['sex']:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE

    # сохраняем в профиль "обо мне" пользователя
    if data['about']:
        user.shopuserprofile.about_me = data['about']

    # сохраняем в профиль кол-во лет пользователя, если меньше 18 - удаляем его
    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = (date.today() - bdate) // timedelta(days=365.2425)
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if data['photo_max_orig']:
        photo_content = requests.get(data['photo_max_orig'])
        with open(f'{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpg', 'wb') as photo_file:
            photo_file.write(photo_content.content)
            user.avatar = f'users_avatars/{user.pk}.jpg'

    user.save()

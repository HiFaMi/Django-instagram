from django.contrib.auth import get_user_model

from config import settings
import requests

User = get_user_model()
class FacebookBackend:
    def authenticate(self, request, code):

        def get_access_token(code):
            url = 'https://graph.facebook.com/v3.0/oauth/access_token?'
            params = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': 'http://localhost:8000/members/facebook-login/',
                'client_secret': settings.FACEBOOK_APP_SECRET_CODE,
                'code': code,
            }

            response = requests.get(url, params)
            # 파이썬에 내장된 json모듈을 사용해서, JSON형식의 텍스트를 파이썬 Object로 변환
            response_dict = response.json()
            access_token = response_dict['access_token']
            return access_token

        # access_token을 검사하기 위함
        # input_token의 경우 검사하기위한 access_token
        # access_token의 경우 개발자의 token id 및 secret code
        def debug_token(token):
            url = 'https://graph.facebook.com/debug_token?'

            token_params = {
                'input_token': token,
                'access_token': '{}|{}'.format(
                    settings.FACEBOOK_APP_ID,
                    settings.FACEBOOK_APP_SECRET_CODE),
            }

            response = requests.get(url, token_params)
            return response.json()

        def get_user_info(token, params_list=None):
            """
            주어진 Token에 해당하는 Facebook User의 정보를 리턴
            """
            url = 'https://graph.facebook.com/v3.0/me'
            if params_list is None:
                params = {
                    'fields': ','.join([
                        'id',
                        'name',
                        'first_name',
                        'last_name',
                        'picture',
                    ]),
                    'access_token': token,
                }

            else:
                params = {
                    'fields': params_list,
                    'access_token': token,
                }
            response = requests.get(url, params)
            response_dict = response.json()
            return response_dict

        def create_user_from_facebook_user_info(user_info):
            facebook_user_id = user_info['id']
            first_name = user_info['first_name']
            last_name = user_info['last_name']
            url_img_profile = user_info['picture']['data']['url']
            return User.objects.get_or_create(
                username=facebook_user_id,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                }, )

        access_token = get_access_token(code)
        user_info = get_user_info(access_token)
        user, user_created = create_user_from_facebook_user_info(user_info)
        return user

    def get_user(self, user_id):

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

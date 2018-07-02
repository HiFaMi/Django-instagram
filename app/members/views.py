from django.contrib.auth import authenticate, get_user_model, login, logout

import requests
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect

from config import settings
from members.forms import SignupForm
from posts.models import Post
from posts.views import index

# User 클래스 자체를 가져올때는 get_user_model()
# ForeignKey에 User모델을 지정할때는 settings.AUTH_USER_MODEL
User = get_user_model()


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET['next'])

            return redirect('posts:post-list')
        else:
            return redirect('members:login')

    else:
        return render(request, 'members/login.html')


def logout_view(request):

    if request.method == 'POST':

        logout(request)
        return redirect('index')


def signup_view(request):

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        # form에 들어있는 데이터가 유효한지 검사
        if form.is_valid():
            user = form.signup()
            login(request, user)
            return redirect('posts:post-list')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }

    return render(request, 'members/signup.html', context)


def signup_view_back(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_check = request.POST['password_check']

        context = {
            'errors': [],
        }

        # if not username:
        #     context['errors'].append('username을 입력 해 주세요')
        # elif not email:
        #     context['errors'].append('email을 입력 해 주세요')
        # elif not password or not password_check:
        #     context['errors'].append('password 또는 password check를 입력 해 주세요')

        required_fields = {'username': {
                                'verbose_name': '아이디',
                            },
                           'email': {
                               'verbose_name': '이메일',
                           },
                           'password': {
                               'verbose_name': '비밀번호',
                           },
                           'password_check': {
                               'verbose_name': '비밀번호 확인',
                           }}

        for field_name in required_fields:
            if not locals()[field_name]:
                context['errors'].append('{}를 입력 해 주세요'.format(required_fields[field_name]['verbose_name']))

        if User.objects.filter(username=username).exists():
            context['errors'].append('유저가 이미 존재함')

        if password != password_check:
                context['errors'].append('비밀번호가 다릅니다.')

        context['username'] = username
        context['password'] = password
        context['email'] = email

        if not context['errors']:

            user = authenticate(request, username=username, email=email, password=password)
            create_user = User.objects.create_user(username=username, email=email, password=password)
            create_user.save()
            login(request, user)
            return redirect('posts:post-list')

        return render(request, 'members/signup.html', context)
    return render(request, 'members/signup.html')


def follow_toggle(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(id=pk)
        using_user = request.user

        if post.author in using_user.following:
            using_user.unfollow(post.author)
            return redirect('posts:post-list')

        else:
            using_user.follow(post.author)
            return redirect('posts:post-list')


# def post_like(request, pk):
#     if request.method == 'POST':
#
#         if not Post.objects.filter(
#                 post=Post.objects.get(id=pk),
#                 user=request.user).exists():
#             posts_like = PostLike.objects.create(
#                 post=Post.objects.get(id=pk),
#                 user=request.user,
#                 post_like=PostLike.CHOICES_POST_UNLIKE
#             )
#             posts_like.save()
#
#         else:
#             post = PostLike.objects.get(
#                 post=Post.objects.get(id=pk),
#                 user=request.user,
#             )
#
#             post.post_like = PostLike.CHOICES_POST_UNLIKE
#             post.save()
#
#         return redirect('posts:post-list')


def following_view(request):

    return render(request, 'posts/following_detail.html')


def following_block(request, pk):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.following_block(User.objects.get(id=pk))

    return redirect('members:following')


def follower_view(request):
    return render(request, 'posts/follower_detail.html')


def follower_block(request, pk):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.follower_block(User.objects.get(id=pk))

    return redirect('members:follower')


def facebook_view(request):
    code = request.GET.get('code')
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
    return response_dict


def facebook_take_token(request):
    url = 'https://graph.facebook.com/debug_token?'

    token_params = {
        'input_token': facebook_view(),
        'access_token': '{}|{}'.format(
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_APP_SECRET_CODE),
    }

    response = requests.get(url, token_params)
    return response


def facebook_graph(request):
    # GraphAPI를 통해서 Facebook User 정보 받아오기
    url = 'https://graph.facebook.com/v3.0/me'
    params = {
        'fields': ','.join([
            'id',
            'name',
            'first_name',
            'last_name',
            'picture',
            ]),
        'access_token': facebook_view(),
    }
    response = requests.get(url, params)
    response_dict = response.json()
    return response_dict


def facebook_to_user(request):
    response_dict = facebook_graph()
    facebook_user_id = response_dict['id']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    url_img_profile = response_dict['picture']['data']['url']

    user, user_created = User.objects.get_or_create(
        username=facebook_user_id,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'img_profile': url_img_profile,
        })
    login(request, user)

    return redirect('index')

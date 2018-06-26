from django.contrib.auth import authenticate, get_user_model

from django.contrib.auth.views import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from members.forms import SignupForm
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
            return redirect('posts:post-list')
        else:
            return redirect('members:login')

    else:
        return render(request, 'members/login.html')


def logout_view(request):

    if request.method == 'POST':

        logout(request)
        return redirect(index)


def signup_view(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        # form에 들어있는 데이터가 유효한지 검사
        if form.is_valid():
            user = form.signup()
            login(request, user)
            return redirect('posts:post-list')

        else:
            # ['{}: {}'.format(key, value) for key, value in form.errors.items()])
            # return HttpResponse(result)
            context = {
                'form': form,
            }

            return render(request, 'members/signup.html', context)
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


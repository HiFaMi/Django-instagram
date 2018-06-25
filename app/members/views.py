from django.contrib.auth import authenticate, get_user_model

from django.contrib.auth.views import login, logout
from django.shortcuts import render, redirect


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

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'errors': [],
            'username': request.POST['username'],
            'email': request.POST['email'],
        }

        if User.objects.filter(username=username).exists():

            context['errors'].append('유저가 이미 존재함')

            if request.POST['password'] != request.POST['password_check']:
                context['errors'].append('비밀번호가 다릅니다.')

            return render(request, 'members/signup.html', context)

        else:

            if request.POST['password'] != request.POST['password_check']:
                context['errors'].append('비밀번호가 다릅니다.')
                return render(request, 'members/signup.html', context)

            else:

                user = authenticate(request, username=username, email=email, password=password)
                create_user = User.objects.create_user(username=username, email=email, password=password)
                create_user.save()
                login(request, user)
                return redirect('posts:post-list')

    return render(request, 'members/signup.html')


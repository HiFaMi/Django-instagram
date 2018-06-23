from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from posts.views import index


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
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            return redirect('members:signup')
        else:
            create_user = User.objects.create_user(username=username, password=password)
            create_user.save()
            login(request, user)
            return redirect('posts:post-list')
    else:
        return render(request, 'members/signup.html')


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from members.models import User
from posts.forms import PostForm
from posts.models import Post


def index(request):
    # return HttpResponseRedirect('/posts/')
    return redirect('posts:post-list')


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)


def post_user_detail(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }

    return render(request, 'posts/post_user_detail.html', context)

@login_required
def post_create(request):

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():

            form.create(request.user)

            return post_detail(request, request.user.id)

    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'posts/post_create.html', context)


@login_required
def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        if request.user == post.author:
            post.delete()

    return redirect('index')


def withdraw(request):
    print(request.user.id)
    if request.method == 'POST':
        User.objects.filter(id=request.user.id).delete()

    return redirect('index')






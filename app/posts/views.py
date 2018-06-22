from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

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

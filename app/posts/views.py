from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from members.models import User
from posts.models import Post, Comment

from posts.forms import PostForm, PostModelForm, CommentModelForm


def index(request):
    # return HttpResponseRedirect('/posts/')
    return redirect('posts:post-list')


def post_list(request):
    form = CommentModelForm()

    posts = Post.objects.all()
    comments = Comment.objects.all()
    context = {
        'posts': posts,
        'form': form,
        'comments': comments,
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


def post_create(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

    else:
        form = PostModelForm()

    context = {
        'form': form
    }

    return render(request, 'posts/post_create.html', context)


@login_required
def post_create_with_form(request):

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():

            post = form.create(request.user)
            return redirect('posts:post-detail', pk=post.id)

    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'posts/post_create.html', context)


@login_required
@require_POST
def post_delete_bak(request, pk):

    post = get_object_or_404(Post, id=pk)
    if request.user == post.author:
        post.delete()
    else:
        raise PermissionDenied('지울 권한이 없습니다.')
    return redirect('posts:post-list')


def post_delete(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        if request.user == post.author:
            post.delete()
        else:
            raise PermissionDenied('지울 권한이 없습니다.')
    return redirect('posts:post-list')


def withdraw(request):
    if request.method == 'POST':
        User.objects.filter(id=request.user.id).delete()

    return redirect('index')


@login_required
def post_comment(request, pk):
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = Post.objects.get(id=pk)
            comment.save()
        return redirect('posts:post-list')





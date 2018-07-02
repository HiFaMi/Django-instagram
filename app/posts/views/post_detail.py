from django.shortcuts import render

from posts.models import Post

__all__ = (
    'post_detail',
    'post_user_detail',
)


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

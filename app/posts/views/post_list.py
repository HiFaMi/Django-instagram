from django.shortcuts import render

from posts.forms import CommentModelForm
from posts.models import Post, Comment

__all__ = (
    'post_list',
)


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

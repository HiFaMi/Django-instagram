from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from posts.models import Post

__all__ = (
    'post_like',
    'post_dislike',
)

@login_required
@require_POST
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    request.user.like_posts.add(post)
    return redirect('posts:post-detail', pk=pk)


@login_required
@require_POST
def post_dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    request.user.like_posts.remove(post)
    return redirect('posts:post-detail', pk)



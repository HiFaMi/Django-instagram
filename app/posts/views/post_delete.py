from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from members.models import User
from posts.models import Post

__all__ =(
    'post_delete',
    'withdraw',
)

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

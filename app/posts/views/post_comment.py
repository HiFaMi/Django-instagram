from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from posts.forms import CommentModelForm
from posts.models import Post

__all__ = (
    'post_comment',
)


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

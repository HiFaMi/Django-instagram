from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from posts.models import Post

__all__ = (
    'follow_toggle',
    'following_view',
    'follower_view',
    'following_block',
    'follower_block',
)


User = get_user_model()


def follow_toggle(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(id=pk)
        using_user = request.user

        if post.author in using_user.following:
            using_user.unfollow(post.author)
            return redirect('posts:post-list')

        else:
            using_user.follow(post.author)
            return redirect('posts:post-list')


# def post_like(request, pk):
#     if request.method == 'POST':
#
#         if not Post.objects.filter(
#                 post=Post.objects.get(id=pk),
#                 user=request.user).exists():
#             posts_like = PostLike.objects.create(
#                 post=Post.objects.get(id=pk),
#                 user=request.user,
#                 post_like=PostLike.CHOICES_POST_UNLIKE
#             )
#             posts_like.save()
#
#         else:
#             post = PostLike.objects.get(
#                 post=Post.objects.get(id=pk),
#                 user=request.user,
#             )
#
#             post.post_like = PostLike.CHOICES_POST_UNLIKE
#             post.save()
#
#         return redirect('posts:post-list')


def following_view(request):

    return render(request, 'posts/following_detail.html')


def following_block(request, pk):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.following_block(User.objects.get(id=pk))

    return redirect('members:following')


def follower_view(request):
    return render(request, 'posts/follower_detail.html')


def follower_block(request, pk):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.follower_block(User.objects.get(id=pk))

    return redirect('members:follower')

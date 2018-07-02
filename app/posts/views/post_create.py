from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from posts.forms import PostModelForm, PostForm

__all__ =(
    'post_create',
    'post_create_with_form',
)


def post_create(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post-list')

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

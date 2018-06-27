from django import forms
from django.http import request

from posts.models import Post


class PostForm(forms.Form):
    img = forms.FileField(
        label='사진',
    )

    description = forms.CharField(
        label='설명',
        widget=forms.Textarea(),
        required=False,
    )

    def create(self, user):

        img = self.cleaned_data['img']

        description = self.cleaned_data['description']

        post = Post.objects.create(author=user, photo=img, content=description)
        post.save()
        return post




from django import forms
from django.forms import ModelForm
from django.http import request

from posts.models import Post, Comment


class PostModelForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['photo', 'content']


class CommentModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['user_comment']
        widgets = {
            'user_comment': forms.TextInput(
                attrs={
                    'class': ('form-control', 'float-left'),
                    'style': 'width: 80%',
                }
            )
        }


class PostForm(forms.Form):
    img = forms.FileField(
        label='사진',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    description = forms.CharField(
        label='설명',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        required=False,
    )

    def create(self, user):

        img = self.cleaned_data['img']

        description = self.cleaned_data['description']

        post = Post.objects.create(author=user, photo=img, content=description)
        post.save()
        return post




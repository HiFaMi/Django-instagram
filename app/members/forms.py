from django import forms

from django.core.exceptions import ValidationError

from members.models import User


class SignupForm(forms.Form):

    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    email = forms.EmailField(
        label='이메일',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    password_check = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    gender = forms.CharField(
        label='성별',
        widget=forms.Select(
            choices=User.CHOICES_GENDER,
            attrs={
                'class': 'form-control'
            }
        ),
    )

    img_profile = forms.ImageField(
        label='프로필 사진',
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        ),
    )

    introduce = forms.CharField(
        label='소개',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
    )

    site = forms.ChoiceField(
        label='블로그',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
    )

    def clean_username(self):
        data = self.cleaned_data['username']

        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('똑같은 아이디가 존재합니다.')

        return data

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password != password_check:
            msg = '비밀번호와 비밀번호 확인의 값이 같지 않습니다.'

            self.add_error('password_check', msg)

        return self.cleaned_data

    def signup(self):
        fields = [
            'username',
            'email',
            'password',
            'gender',
            'img_profile',
            'introduce',
            'site'
        ]
        # create_user_dict = {}
        #
        # for key, value in self.cleaned_data.items():
        #     if key in fields:
        #         create_user_dict[key] = value

        # create_user_dict = {key: value for key, value in self.cleaned_data.items() if key in fields}

        def in_fields(item):
            return item[0] in fields
        create_user_dict =dict(filter(in_fields, self.cleaned_data.items()))

        user = User.objects.create_user(**create_user_dict)

        # username = self.cleaned_data['username']
        # email = self.cleaned_data['email']
        # password = self.cleaned_data['password']
        # img_profile = self.cleaned_data['img_profile']
        # introduce = self.cleaned_data['introduce']
        # gender = self.cleaned_data['gender']
        # site = self.cleaned_data['site']
        #
        # user = User.objects.create_user(
        #     username=username,
        #     email=email,
        #     password=password,
        #     img_profile=img_profile,
        #     site=site,
        #     introduce=introduce,
        #     gender=gender,
        # )

        return user

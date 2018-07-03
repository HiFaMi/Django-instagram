# access_token을 받아오기 위함
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

from config import settings
import requests

__all__ = (
    'facebook_view',
)


def facebook_view(request):

    code = request.GET.get('code')
    user = authenticate(request, code=code)

    if user is not None:
        login(request, user)
        return redirect('index')
    return redirect('members:login')
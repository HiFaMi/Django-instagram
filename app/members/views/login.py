from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

__all__ = (
    'login_view',
)


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET['next'])

            return redirect('posts:post-list')
        else:
            return redirect('members:login')

    else:
        return render(request, 'members/login.html')

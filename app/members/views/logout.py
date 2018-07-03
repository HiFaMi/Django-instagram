from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):

    if request.method == 'POST':

        logout(request)
        return redirect('index')

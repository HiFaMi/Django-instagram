
from django.shortcuts import redirect
from .post_comment import *
from .post_create import *
from .post_delete import *
from .post_detail import *
from .post_like import *
from .post_list import *

def index(request):
    # return HttpResponseRedirect('/posts/')
    return redirect('posts:post-list')











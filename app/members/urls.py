from django.urls import path

from .views import login_view, logout_view, signup_view, follow_toggle, following_view, following_block, follower_view, \
    follower_block

app_name = 'members'
urlpatterns =[
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('<int:pk>/follow/', follow_toggle, name='follow'),
    # path('<int:pk>/postlike/', post_like, name='post-like'),
    path('following_detail', following_view, name='following'),
    path('<int:pk>/following_detail/block', following_block, name='following-block'),
    path('follower_detail', follower_view, name='follower'),
    path('<int:pk>/follower_detail/block', follower_block, name='follower-block')
]

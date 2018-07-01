from django.urls import path

from .views import login_view, logout_view, signup_view, follow_toggle, post_like

app_name = 'members'
urlpatterns =[
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('<int:pk>/follow/', follow_toggle, name='follow'),
    path('<int:pk>/postlike/', post_like, name='post-like'),
]

from django.urls import path

from .views import post_list, post_detail, post_create, post_delete, post_user_detail, withdraw, comment_view

app_name = 'posts'
urlpatterns = [
    path('', post_list, name='post-list'),
    path('<int:pk>/', post_detail, name='post-detail'),
    path('create/', post_create, name='post-create'),
    path('<int:pk>/delete/', post_delete, name='post-delete'),
    path('user_detail/', post_user_detail, name='post-user-detail'),
    path('withdraw/', withdraw, name='withdraw'),
    path('comment/', comment_view, name='post-comment'),
]

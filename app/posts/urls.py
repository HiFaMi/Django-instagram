from django.urls import path


from .views import post_detail, post_create, post_delete, post_user_detail, withdraw, \
    post_comment, post_list, post_like, post_dislike

app_name = 'posts'
urlpatterns = [
    path('', post_list, name='post-list'),
    path('<int:pk>/', post_detail, name='post-detail'),
    path('create/', post_create, name='post-create'),
    path('<int:pk>/delete/', post_delete, name='post-delete'),
    path('user_detail/', post_user_detail, name='post-user-detail'),
    path('withdraw/', withdraw, name='withdraw'),
    path('<int:pk>/comment/', post_comment, name='post-comment'),
    path('<int:pk>/like/', post_like, name='post-like'),
    path('<int:pk>/dislike/', post_dislike, name='post-dislike'),

]

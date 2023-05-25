from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('posts/<int:pk>/', views.post_detail.as_view(), name='post_detail'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
    path('category/<slug:category_slug>/', views.category_posts.as_view(),
         name='category_posts'),
    path('profile/<username>/', views.profile_view.as_view(), name='profile'),
    path('profile/<int:pk>/edit/',
         views.edit_profile.as_view(), name='edit_profile'),
    path('posts/create/', views.create_post.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/', views.edit_post.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/',
         views.delete_post.as_view(), name='delete_post'),
    path('profile/', views.index.as_view(), name='profile'),
]

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('posts/<int:pk>/', views.Post_view.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/', views.Category_posts.as_view(),
         name='category_posts'),
    path('profile/<username>/', views.Profile.as_view(), name='profile'),
    path('profile/<int:pk>/edit/',
         views.Edit_profile.as_view(), name='edit_profile'),
    path('posts/create/', views.Create_post.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/', views.Edit_post.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/',
         views.Delete_post.as_view(), name='delete_post'),
    path('<int:pk>/comment/', views.Add_comment.as_view(), name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:pk>/',
         views.Edit_comment.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:pk>/',
         views.Delete_comment.as_view(), name='delete_comment')
]

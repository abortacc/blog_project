from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/<int:id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.CreatePostCreateView.as_view(), name='create_post'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts')
]

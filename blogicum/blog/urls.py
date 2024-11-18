from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('posts/<int:id>', views.post_detail),
    path('category/<slug:category_slug>', views.category_posts)
]

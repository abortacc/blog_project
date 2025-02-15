from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post, Category
from datetime import datetime
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .forms import CreatePostForm
from django.utils import timezone


User = get_user_model()


class IndexListView(ListView):
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    queryset = Post.objects.select_related(
        'location',
        'author'
    ).filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )
    paginate_by = 5


class CreatePostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = CreatePostForm


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Post.objects.select_related('category').filter(
            (Q(is_published=True) | Q(category__is_published=True)) &
            Q(pub_date__lte=timezone.now())
        )


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.select_related('category').filter(
        category__slug=category_slug,
        pub_date__lte=datetime.now()
    )
    context = {
        'category_slug': category_slug,
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)

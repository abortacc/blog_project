from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post, Category
from datetime import datetime


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'location',
        'author'
    ).filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    ).order_by(
        '-pub_date'
    )[:5]
    context = {
        'post_list': post_list
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            Q(is_published=True)
            | Q(category__is_published=True),
            pub_date__lte=datetime.now(),
        ),
        pk=id
    )
    context = {
        'post': post
    }
    return render(request, template, context)


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

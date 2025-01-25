from django.shortcuts import render


def index(request):
    template = 'blog/index.html'
    context = {}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    context = {}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    context = {
        'category_slug': category_slug
    }
    return render(request, template, context)

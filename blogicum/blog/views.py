from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post, Category, Comment
from datetime import datetime
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm
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
    form_class = PostForm


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Post.objects.select_related('category').filter(
            (Q(is_published=True) | Q(category__is_published=True)) &
            Q(pub_date__lte=timezone.now())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class ProfileListView(ListView):
    template_name = 'blog/profile.html'
    model = Post
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.select_related('author').filter(
            author__username=self.kwargs['username']
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    post_obj = None

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)


class CategoryPostsListView(ListView):
    template_name = 'blog/category.html'
    model = Post
    slug_url_kwarg = 'category_slug'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.select_related('category').filter(
            category__slug=self.kwargs.get('category_slug'),
            pub_date__lte=datetime.now()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs.get('category_slug'),
            is_published=True
        )
        return context

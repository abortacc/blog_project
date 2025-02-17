from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q, Count
from .models import Post, Category, Comment
from datetime import datetime
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm, ProfileForm
from django.utils import timezone
from django.urls import reverse


User = get_user_model()


class IndexListView(ListView):
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    queryset = Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    ).annotate(
        comments_count=Count('comments')
    )
    paginate_by = 5


class PostMixin:
    model = Post
    template_name = 'blog/create.html'


class PostCreateView(PostMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])


class PostUpdateView(PostMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.kwargs['id']})


class PostDeleteView(PostMixin, LoginRequiredMixin, DeleteView):
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse("blog:profile", kwargs={"username": self.request.user})


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


class ProfileUpdateView(UpdateView):
    template_name = 'blog/user.html'
    model = User
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])



class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.kwargs['post_id']})


class CommentMixin(LoginRequiredMixin, View):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(
            Comment,
            pk=kwargs['comment_id']
        )
        if comment.author != request.user:
            return redirect('blog:post_detail', id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.kwargs['post_id']})


class CommentUpdateView(CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentMixin, DeleteView):
    pass


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

from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'pub_date', 'is_published',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

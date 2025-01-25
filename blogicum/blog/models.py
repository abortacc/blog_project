from django.db import models
from django.contrib.auth import get_user_model
from core.models import IsPubslishedClass


User = get_user_model()


class Category(IsPubslishedClass):
    title = models.CharField(max_length=256)
    description = models.TextField()
    slug = models.SlugField(unique=True)


class Location(IsPubslishedClass):
    name = models.CharField(max_length=256)


class Post(IsPubslishedClass):
    title = models.CharField(max_length=256)
    text = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

from django.db import models
from django.contrib.auth import get_user_model
from core.models import IsPubslishedClass


User = get_user_model()


class Category(IsPubslishedClass):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            f'Идентификатор страницы для URL; '
            f'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title


class Location(IsPubslishedClass):
    name = models.CharField(max_length=256, verbose_name='Название')

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'местоположения'

    def __str__(self):
        return self.name


class Post(IsPubslishedClass):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время',
        help_text=(
            f'Если установить дату и время в будущем'
            f' — можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'публикации'

    def __str__(self):
        return f"Публикация №{self.id}: '{self.title}'"

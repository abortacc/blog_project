from django.contrib import admin
from .models import Category, Location, Post, Comment


admin.site.empty_value_display = '(Пусто)'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at'
    )
    list_display_links = (
        'title',
    )
    list_editable = (
        'description',
        'slug',
        'is_published'
    )
    search_fields = (
        'title',
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at'
    )
    list_display_links = (
        'name',
    )
    search_fields = (
        'name',
    )
    list_editable = (
        'is_published',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'location',
        'category',
        'author',
        'pub_date',
        'is_published'
    )
    list_editable = (
        'text',
        'location',
        'category',
        'is_published'
    )
    list_display_links = (
        'title',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'location',
        'category',
        'author'
    )


admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)

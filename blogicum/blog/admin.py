from django.contrib import admin
from .models import Category, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug'
    )
    list_display_links = (
        'title',
    )
    list_editable = (
        'description',
        'slug'
    )
    search_fields = (
        'title',
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    list_display_links = (
        'name',
    )
    search_fields = (
        'name',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'location',
        'category',
        'author',
        'pub_date'
    )
    list_editable = (
        'text',
        'location',
        'category'
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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)

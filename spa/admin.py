from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from spa.models import Comment, CustomUser, Review

admin.site.register(CustomUser, UserAdmin)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "text", "created_on", "file")
    sortable_by = ["author", "created_on"]
    search_fields = ["author", "created_on"]
    list_per_page = 10


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("review", "author", "comment_text", "created_on")
    sortable_by = ["author", "created_on"]
    search_fields = ["review", "author"]
    list_per_page = 10

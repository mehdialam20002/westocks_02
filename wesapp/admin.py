from atexit import register
from django.contrib import admin

# Register your models here.
from .models import Comment, Contact, Post
# admin.site.register(Comment)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content2')


admin.site.register(Post, PostAdmin)
admin.site.register(Contact)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'body', 'post')


admin.site.register(Comment, CommentAdmin)

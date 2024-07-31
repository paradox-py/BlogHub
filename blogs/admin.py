from django.contrib import admin
from .models import Blog,Comment
# from taggit.admin import TaggitAdmin

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'content','tags')



class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'created_at')
    search_fields = ('blog__title', 'author__username', 'content')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
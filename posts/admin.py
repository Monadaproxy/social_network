from django.contrib import admin
from .models import Post, Comment, PostImage

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    fields = ('image', 'alt_text')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    inlines = [CommentInline, PostImageInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostImage)
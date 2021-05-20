from django.contrib import admin
from .models import Category, Post, Comment, Author


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('author_post', 'header_post', 'text_post', 'show_category')

    def show_category(self, obj):
        return "\n".join([a.category_name for a in obj.category_post.all()])


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, CategoryAdmin)
admin.site.register(Comment)


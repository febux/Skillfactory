from django.contrib import admin

from .models import Category, SlackUser, Channel, Post

admin.site.register(SlackUser)
admin.site.register(Category)
admin.site.register(Channel)
admin.site.register(Post)

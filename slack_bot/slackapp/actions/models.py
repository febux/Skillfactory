from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache  # импортируем наш кэш


class Category(models.Model):
    category_name = models.TextField(unique=True)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def check_exist(category):
        try:
            Category.objects.get(category_name=category)
        except Category.DoesNotExist:
            Category.objects.create(category_name=category)
            print(f'category {category} was created.')
        else:
            print(f'category {category} was found.')

    def __str__(self):
        return self.category_name


class Post(models.Model):
    post_category = models.ManyToManyField(to=Category, blank=True)
    post_link = models.TextField()
    post_header = models.TextField()
    post_text = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def check_exist(post_link):
        try:
            Post.objects.get(post_link=post_link)
        except Post.DoesNotExist:
            print('Call post creating...')
            return False
        else:
            print('Post was found.')
            return True

    def preview(self):
        preview = self.post_text[:100] + '...'
        return preview

    def __str__(self):
        return self.post_header

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class Channel(models.Model):
    channel_name = models.TextField(unique=True)
    channel_category = models.ManyToManyField(to=Category, blank=True)

    @staticmethod
    def get_all_channels():
        return Channel.objects.all()

    def get_categories_channel(self):
        return self.channel_category.all()

    def __str__(self):
        return self.channel_name


class SlackUser(models.Model):
    slack_category = models.ManyToManyField(to=Category, blank=True)
    slack_user = models.CharField(max_length=12, unique=True)
    is_stuff = models.BooleanField(default=0)

    def __str__(self):
        return self.slack_user

    def get_categories_user(self):
        return self.slack_category.all()

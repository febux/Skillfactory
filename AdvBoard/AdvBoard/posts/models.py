from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username


class Category(models.Model):
    category_name = models.TextField(unique=True)
    subscriber = models.ManyToManyField(to=User)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_post = models.ManyToManyField(to=Category,
                                           blank=True,
                                           related_name='category')
    date_post = models.DateTimeField(auto_now_add=True)
    header_post = models.TextField()
    text_post = models.TextField()

    def get_comments_post(self):
        comments = Comment.objects.filter(post_comment=self)
        return comments

    def preview(self):
        preview = self.text_post[:100] + '...'
        return preview

    def __str__(self):
        return self.header_post

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'news-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        info = "'" + str(self.text_comment) + "'" + "--- Author:" + str(self.author_comment.username) +\
                "- Date:" + str(self.date_comment)
        return info


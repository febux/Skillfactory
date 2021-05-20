from django.forms import ModelForm
from .models import Post, Category


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['author_post', 'header_post', 'text_post', 'category_post']


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['category_name', 'subscriber']
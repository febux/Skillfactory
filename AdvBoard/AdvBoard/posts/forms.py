from django.forms import ModelForm
from .models import Post, Category, Comment


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['header_post', 'text_post', 'category_post']


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['category_name', 'subscriber']


class AddCommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text_comment']

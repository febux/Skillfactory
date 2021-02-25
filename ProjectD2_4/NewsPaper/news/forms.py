from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['author_post', 'header_post', 'text_post', 'category_post']

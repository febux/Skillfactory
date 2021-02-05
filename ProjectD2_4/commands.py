from django.contrib.auth.models import User
from NewsPaper.news.models import Author, Post, Comment, Category

#  Создаем пользователей
User.objects.create(username='Abdullah', password='qwerty')
User.objects.create(username='Salem', password='qwerty')

# Создаем авторов
Author.objects.create(author=User.objects.get(id=1))
Author.objects.create(author=User.objects.get(id=2))

# Создаем категории
Category.objects.create(name='IT')
Category.objects.create(name='AI')
Category.objects.create(name='Business')
Category.objects.create(name='New Tech')

# Создаем новости и статьи
Post.objects.create(author=Author.objects.get(id=1), type='AR',
                    header='Article 1',
                    article_text='Text of Article 1')

Post.objects.create(author=Author.objects.get(id=1), type='AR',
                    header='Article 2',
                    article_text='Text of Article 2')

Post.objects.create(author=Author.objects.get(id=1), type='NW',
                    header='News',
                    article_text='Text of News')

# Присваиваем категории новости
post = Post.objects.get(id=1)
post.category.add(Category.objects.get(id=1))
post.category.add(Category.objects.get(id=2))

post = Post.objects.get(id=2)
post.category.add(Category.objects.get(id=2))
post.category.add(Category.objects.get(id=4))

# Создаем комментарии
author = User.objects.get(id=2)
post = Post.objects.get(id=1)
Comment.objects.create(post=post, author=author, text='Comment text')
author = User.objects.get(id=1)
Comment.objects.create(post=post, author=author, text='Comment text 1')

author = User.objects.get(id=1)
post = Post.objects.get(id=2)
Comment.objects.create(post=post, author=author, text='Comment text 2')
author = User.objects.get(id=2)
Comment.objects.create(post=post, author=author, text='Comment text 3')

# Ставим лайки комментариям
comments = Comment.objects.all()
comments[1].like()
comments[2].like()
comments[1].dislike()
comments[3].like()
comments[3].dislike()
comments[4].like()

# Ставим лайк для поста
post.like()

# Меняем рейтинг посту
post.post_rating = 100
post.save()

# Обновляем рейтинги авторов
for auth in Author.objects.all():
    auth.update_raiting()

# Выводим имя и рейтинг лучшего пользоветеля
Author.objects.all().order_by('-rating_author').values('author__username', 'rating_author')[0]

# Выводим самую лучшую статью
best = Post.objects.all().order_by('-post_rating')[0]
best_post = Post.objects.all().order_by('-post_rating').values(  # выводим параметры
    'date_post',
    'author__author__username',
    'header_post', 'rating_post',
    'text_post')[0]
best.preview()

# Выводим все комменты к статье
Comment.objects.filter(post=best).values('author_comment__username', 'date_comment', 'text_comment')

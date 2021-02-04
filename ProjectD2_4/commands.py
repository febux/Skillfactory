from django.contrib.auth.models import User
from news.models import Author, Post, Comment, Category, PostCategory

#  Создаем пользователей
User.objects.create(username='Abdullah', password='qwert')
User.objects.create(username='Salem', password='qwert')

# Создаем авторов
Author.objects.create(author=User.objects.get(id=1))
Author.objects.create(author=User.objects.get(id=2))

# Создаем категории
Category.objects.create(name='Спорт')
Category.objects.create(name='Путешествия')
Category.objects.create(name='Бизнес')
Category.objects.create(name='Технологии')

# Создаем новости и статьи
Post.objects.create(author=Author.objects.get(id=5), type='NW',
                    header='Новость',
                    article_text='Сам текст новости')

# Присваиваем категории новости из примера выше id=5
# Вар 1
post = Post.objects.get(id=5)
post.category.add(Category.objects.get(id=1))

# Вар 2
cat = Category.objects.get(id=2)
PostCategory.objects.create(post=post, category = cat)

# Создаем комментарии
author = User.objects.get(id=6)
post = Post.objects.get(id=5)
Comment.objects.create(post=post, author=author, text='Здесь будет текст комментария')

# Ставим лайки комментариям
comments = Comment.objects.all()
comments[6].like()  # 3 лайка для Тома Круза

# Ставим лайки для поста
post.like()

# меняем рейтинг посту
post.post_rating = 100
post.save()

# Обновляем рейтинги авторов
for auth in Author.objects.all():
    auth.update_raiting()

# Вывести имя и рейтинг лучшего пользоветеля
Author.objects.all().order_by('-author_rating').values('author__username', 'author_rating')[0]

# Вывести самую крутую статью
best = Post.objects.all().order_by('-post_rating')[0]
best_post = Post.objects.all().order_by('-post_rating').values( # выводим параметры
    'created_time',
    'author__author__username',
    'header', 'post_rating',
    'article_text')[0]
best.preview()

# Вывести все комменты к статье
Comment.objects.filter(post=best).values('author__username', 'created_time', 'text')
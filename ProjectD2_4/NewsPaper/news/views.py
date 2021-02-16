# from django.shortcuts import render
from datetime import datetime

from django.views.generic import ListView, \
    DetailView  # импортируем класс, который говорит нам о том, что в этом представлении
# мы будем выводить список объектов из БД
from .models import Post


# создаём представление в котором будет детали конкретного отдельного товара
class PostDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'new.html'  # название шаблона
    context_object_name = 'new'  # название объекта в нём будет


class PostsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    queryset = Post.objects.order_by('-id')
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать html,
    # в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,

    # его надо указать, чтобы обратиться к самому списку объектов через html-шаблон
    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон.
    # В возвращаемом словаре context будут храниться все переменные.
    # Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # post = Post.objects.get(id=1)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime

from django.template.loader import render_to_string
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
# импортируем класс, который говорит нам о том, что в этом представлении
# мы будем выводить список объектов из БД
from django.views import View
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .models import Post, Author, Category
from .filters import PostFilter, PostFilterView  # импортируем недавно написанный фильтр
from .forms import PostForm, CategoryForm
from django.contrib.auth.mixins import PermissionRequiredMixin

from .tasks import mailing_followers


class CategorySubscribeView(LoginRequiredMixin, UpdateView):
    model = Category  # указываем модель, объекты которой мы будем выводить
    # queryset = Category.objects.order_by('-id')
    form_class = CategoryForm
    template_name = 'subscribe.html'  # указываем имя шаблона, в котором будет лежать html,
    # в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'category'  # это имя списка, в котором будут лежать все объекты

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Category.objects.get(pk=id)

    # def get(self, request, *args, **kwargs):
    #     return render(request, 'subscribe.html', {})

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        current_category = Category.objects.get(pk=id)
        current_user = self.request.user
        current_category.subscriber.add(current_user)

        # получем наш html
        html_content = render_to_string(
            'subscription_created.html',
            {
                'category': current_category,
                'user': current_user,
            }
        )

        # отправляем письмо
        msg = EmailMultiAlternatives(
            subject=f'{current_user.username}',
            # имя клиента будет в теме для удобства
            body=None,  # сообщение с кратким описанием проблемы
            from_email='davydenkoraar@mail.ru',  # здесь указываете почту, с которой будете отправлять
            to=[current_user.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем

        return redirect('/news/')


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
    paginate_by = 10  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['filter'] = PostFilterView(self.request.GET, queryset=self.get_queryset())
        return context


class PostsFilter(ListView):
    model = Post
    queryset = Post.objects.order_by('-id')
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-date_post']
    paginate_by = 5  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data
        # у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    template_name = 'news/post_add.html'
    form_class = PostForm
    success_url = '/news/'

    def post(self, request, *args, **kwargs):
        category = request.POST['category_post']
        new_post = Post.objects.create(
            author_post=Author.objects.get(pk=request.POST['author_post']),
            header_post=request.POST['header_post'],
            text_post=request.POST['text_post'],
        )
        current_category = Category.objects.get(pk=category)
        new_post.category_post.add(current_category)
        new_post.save()

        return redirect('/news/')


# дженерик для редактирования объекта
class PostEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news/post_edit.html'
    form_class = PostForm
    success_url = '/news/'

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



from allauth.account.utils import user_email
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
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
from .models import Post, Author, Category, Comment
from .filters import PostFilter, PostFilterView  # импортируем недавно написанный фильтр
from .forms import PostForm, CategoryForm, AddCommentForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.files.uploadedfile import SimpleUploadedFile

from django.core.cache import cache  # импортируем наш кэш

from AdvBoard.settings import DEFAULT_FROM_EMAIL


class CategorySubscribeView(LoginRequiredMixin, UpdateView):
    model = Category  # указываем модель, объекты которой мы будем выводить
    # queryset = Category.objects.order_by('-id')
    form_class = CategoryForm
    template_name = 'subscribe.html'  # указываем имя шаблона, в котором будет лежать html,
    # в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'category'  # это имя списка, в котором будут лежать все объекты

    def get_object(self, **kwargs):
        uid = self.kwargs.get('pk')
        return Category.objects.get(pk=uid)

    # def get(self, request, *args, **kwargs):
    #     return render(request, 'subscribe.html', {})

    def post(self, request, *args, **kwargs):
        uid = self.kwargs.get('pk')
        current_category = Category.objects.get(pk=uid)
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

        return redirect('/posts/')


# создаём представление в котором будет детали конкретного отдельного товара
class PostDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного
    template_name = 'post.html'  # название шаблона
    context_object_name = 'post'  # название объекта
    queryset = Post.objects.all()

    # def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
    #     obj = cache.get(f'posts-{self.kwargs["pk"]}',
    #                     None)  # кэш очень похож на словарь, и метод get действует также.
    #     # Он забирает значение по ключу, если его нет, то забирает None.
    #     # если объекта нет в кэше, то получаем его и записываем в кэш
    #     if not obj:
    #         obj = super().get_object(queryset=self.get_queryset())
    #         cache.set(f'posts-{self.kwargs["pk"]}', obj)
    #
    #     return obj

    def get_object(self, **kwargs):
        uid = self.kwargs.get('pk')
        return Post.objects.get(pk=uid)


class PostsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    queryset = Post.objects.order_by('-id')
    template_name = 'posts.html'  # указываем имя шаблона, в котором будет лежать html,
    # в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты,

    # его надо указать, чтобы обратиться к самому списку объектов через html-шаблон
    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон.
    # В возвращаемом словаре context будут храниться все переменные.
    # Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    paginate_by = 10  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        return context


class PostsFilter(ListView):
    model = Post
    queryset = Post.objects.order_by('-id')
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-date_post']
    paginate_by = 5  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data
        # у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_post', )
    template_name = 'posts/post_add.html'
    form_class = PostForm
    success_url = '/posts/'

    def post(self, request, *args, **kwargs):
        category = request.POST['category_post']
        author = Author.objects.get(author__username=request.POST['username'])
        new_post = Post.objects.create(
            author_post=Author.objects.get(pk=author.id),
            header_post=request.POST['header_post'],
            text_post=request.POST['text_post'],
            image_post=request.FILES['image_post']
        )
        current_category = Category.objects.get(pk=category)
        new_post.category_post.add(current_category)
        new_post.save()

        return redirect('/posts/')


# дженерик для редактирования объекта
class PostEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('posts.change_post',)
    template_name = 'posts/post_edit.html'
    form_class = PostForm
    success_url = '/posts/'

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        uid = self.kwargs.get('pk')
        return Post.objects.get(pk=uid)


# дженерик для удаления товара
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('posts.delete_post',)
    template_name = 'posts/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        uid = self.kwargs.get('pk')
        return Post.objects.get(pk=uid)


class CommentAddView(LoginRequiredMixin, CreateView):
    template_name = 'add_comment.html'
    form_class = AddCommentForm
    login_url = '/sign/login/'
    success_url = '/posts/'

    def post(self, request, *args, **kwargs):
        uid = self.kwargs.get('pk')
        current_post = Post.objects.get(pk=uid)
        new_comment = Comment.objects.create(
            post_comment=current_post,
            author_comment=User.objects.get(pk=request.POST['uid']),
            text_comment=request.POST['text_comment'],
        )
        author_post = User.objects.get(username=current_post.author_post)
        send_mail(
            subject=f'Отклик от пользывателя : {new_comment.author_comment}',
            message=f'Текст отклика : {new_comment.text_comment}\n'
                    f'Для подтверждения отклика перейдите по ссылке:'
                    f'http://127.0.0.1:8000/posts/{uid}/comment_accept/{new_comment.id}/',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[author_post.email]
        )
        return redirect(f'/posts/{uid}')

    def get_object(self, **kwargs):
        uid = self.kwargs.get('pk')
        return Post.objects.get(pk=uid)


def comment_accept(request, pk, ck):
    # current_post = Post.objects.get(pk=pk)
    current_comment = Comment.objects.get(pk=ck)
    current_comment.is_accepted = True
    current_comment.save()
    return redirect(f'/posts/{pk}')



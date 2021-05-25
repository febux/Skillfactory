from datetime import datetime, timedelta

from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from posts.models import Category, Post


@shared_task
def mailing_followers(new_post_id, current_category_id):
    print("Start to mailing...")
    # print(new_post_id)
    # print(current_category_id)

    new_post = Post.objects.get(pk=new_post_id)
    # print(new_post)
    current_category = Category.objects.get(pk=current_category_id)
    # print(current_category)
    for sub in current_category.subscriber.all():
        print(f"Follower - {sub.username}")
        # получем наш html
        html_content = render_to_string(
            'following_mail.html',
            {
                'new': new_post,
                'header': new_post.header_post,
                'user': sub,
                'text': new_post.text_post,
                'category': current_category,
            }
        )
        # отправляем письмо
        msg = EmailMultiAlternatives(
            subject=f'{new_post.header_post}',
            # имя клиента будет в теме для удобства
            body=new_post.text_post,  # сообщение с кратким описанием проблемы
            from_email='davydenkoraar@mail.ru',  # здесь указываете почту, с которой будете отправлять
            to=[sub.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем


# @shared_task
# def weekly_mailing_followers():
#     print('weekly mailing')
#
#     for cat in Category.objects.all():
#         # print(cat)
#         current_week = datetime.today() - timedelta(days=1)
#         current_week = current_week.strftime("%V")
#         # print(current_week)
#         posts = Post.objects.all().filter(category_post=cat, date_post__week=current_week)
#         # print(posts)
#
#         for sub in cat.subscriber.all():
#             print(f"Follower - {sub.username}")
#             # print(sub)
#             # получем наш html
#             html_content = render_to_string(
#                 'following_mail_week.html',
#                 {
#                     'posts': posts,
#                     'user': sub,
#                     'category': cat,
#                 }
#             )
#             # отправляем письмо
#             msg = EmailMultiAlternatives(
#                 subject=f'{sub.username}',
#                 # имя клиента будет в теме для удобства
#                 body=None,  # сообщение с кратким описанием проблемы
#                 from_email='davydenkoraar@mail.ru',  # здесь указываете почту, с которой будете отправлять
#                 to=[sub.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
#             )
#             msg.attach_alternative(html_content, "text/html")  # добавляем html
#
#             msg.send()

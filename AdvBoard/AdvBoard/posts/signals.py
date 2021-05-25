from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, Comment
from .tasks import mailing_followers


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(post_save, sender=Comment)
def notify_author_comment(sender, instance, accepted, **kwargs):
    if accepted:
        subject = f'New comment - Author:{instance.author_comment} Date:{instance.date_comment.strftime("%d %m %Y")}'
    else:
        subject = f'Post - Author:{instance.author_comment} Date:{instance.date_comment.strftime("%d %m %Y")}.'

    # получем наш html
    html_content = render_to_string(
        'comment_accept_email.html',
        {
            'header': instance.header_post,
            'user': instance.author_comment,
            'text': instance.text_comment,
        }
    )
    author_comment = User.objects.get(username=instance.author_comment)
    # отправляем письмо
    msg = EmailMultiAlternatives(
        subject=subject,
        # имя клиента будет в теме для удобства
        body=instance.text_comment,  # сообщение с кратким описанием проблемы
        from_email='davydenkoraar@mail.ru',  # здесь указываете почту, с которой будете отправлять
        to=[author_comment.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()

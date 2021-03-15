from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_subscribers_post(sender, instance, created, **kwargs):
    if created:
        subject = f'New post - Author:{instance.author_post} Date:{instance.date_post.strftime("%d %m %Y")}'
    else:
        subject = f'Post - Author:{instance.author_post} Date:{instance.date_post.strftime("%d %m %Y")}.'

    for cat in instance.category_post.all():
        # print(cat)
        current_category = Category.objects.get(category_name=cat)
        # print(current_category)

        for sub in current_category.subscriber.all():
            # получем наш html
            html_content = render_to_string(
                'following_mail.html',
                {
                    'new': instance,
                    'header': instance.header_post,
                    'user': sub,
                    'text': instance.text_post,
                    'category': current_category,
                }
            )
            # отправляем письмо
            msg = EmailMultiAlternatives(
                subject=subject,
                # имя клиента будет в теме для удобства
                body=instance.text_post,  # сообщение с кратким описанием проблемы
                from_email='davydenkoraar@mail.ru',  # здесь указываете почту, с которой будете отправлять
                to=[sub.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()

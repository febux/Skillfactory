import logging
from datetime import datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    print('weekly mailing')

    for cat in Category.objects.all():
        print(cat)
        current_week = datetime.today().strftime("%V")
        print(current_week)
        posts = Post.objects.all().filter(category_post=cat, date_post__week=current_week)
        print(posts)

        for sub in cat.subscriber.all():
            print(sub)
            # получем наш html
            html_content = render_to_string(
                'following_mail_week.html',
                {
                    'news': posts,
                    'user': sub,
                    'category': cat,
                }
            )
            # отправляем письмо
            msg = EmailMultiAlternatives(
                subject=f'{sub.username}',
                # имя клиента будет в теме для удобства
                body=None,  # сообщение с кратким описанием проблемы
                from_email='davydenkoraar@mail.ru',  # здесь указываете почту, с которой будете отправлять
                to=[sub.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()


# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="*/1"),
            # trigger=CronTrigger(second="*/20"),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи,
            # которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

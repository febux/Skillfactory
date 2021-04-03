from datetime import datetime, timedelta

from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Category, SlackUser, Channel, Post

from bs4 import BeautifulSoup
import requests as request
import lxml.html
from lxml import etree

from .views import client


@shared_task
def find_new_posts():
    response = request.get("https://habr.com/ru/company/skillfactory/blog/")
    res = response.content
    res = lxml.html.document_fromstring(res)

    soup = BeautifulSoup(response.text, 'lxml')

    last_post_categories = soup.find("ul", {'class': 'post__hubs inline-list'}).text
    last_post_categories = last_post_categories.replace("\n", "").split(',         ')
    last_post_header = soup.find("h2", {'class': 'post__title'}).text
    last_post_header = last_post_header.replace("\n", "")
    last_post_link = ''.join(res.xpath('/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/ul/li[1]/article/h2/a/@href'))
    last_post_text = soup.find("div", {'class': 'post__text post__text-html post__text_v2'}).text
    last_post_text = last_post_text.replace("\n", "")

    if Post.check_exist(last_post_link):
        print('Post exists.')
    else:
        last_post = Post.objects.create(post_link=last_post_link,
                                        post_header=last_post_header,
                                        post_text=last_post_text)
        for cat in last_post_categories:
            Category.check_exist(cat)
            last_post.post_category.add(Category.objects.get(category_name=cat))
        last_post.save()
        print('Post was created.')

        for follower in SlackUser.objects.all():
            slack_user = SlackUser.objects.get(slack_user=follower)
            # print(follower)

            for cat in slack_user.get_categories_user():
                # print(cat)
                cat = str(cat)

                if cat in last_post_categories:
                    # print(cat + ' match.')
                    client.chat_postMessage(channel=str(follower), text=f'Всем привет! На нашем '
                                                                        f'хабре появилась новая статья.\n'
                                                                        f'{last_post_link} \n {last_post_header} \n'
                                                                        f'{last_post_text}')
                    break

        for channel in Channel.get_all_channels():
            print(channel)
            if channel.get_categories_channel():
                for cat in channel.get_categories_channel():
                    print(cat)
                    if cat in last_post_categories:
                        client.chat_postMessage(channel=str(channel), text=f'Всем привет! На нашем '
                                                                           f'хабре появилась новая статья.\n'
                                                                           f'{last_post_link} \n '
                                                                           f'{last_post_header} \n'
                                                                           f'{last_post_text}')
                        break
            else:
                client.chat_postMessage(channel=str(channel), text=f'Всем привет! На нашем '
                                                                   f'хабре появилась новая статья.\n'
                                                                   f'{last_post_link} \n '
                                                                   f'{last_post_header} \n'
                                                                   f'{last_post_text}')

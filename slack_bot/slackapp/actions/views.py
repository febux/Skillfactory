from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
import slack
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack import WebClient

import requests
import json
import lxml.html
from lxml import etree

from .models import SlackUser, Category, Channel

client = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)


class DoesNotExist(BaseException):
    pass


@csrf_exempt
def event_hook(request):
    json_dict = json.loads(request.body.decode('utf-8'))
    if json_dict['token'] != settings.VERIFICATION_TOKEN:
        return HttpResponse(status=403)
    if 'type' in json_dict:
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)

    if 'event' in json_dict:
        event_msg = json_dict['event']
        # print(event_msg)

        if 'bot_id' in event_msg:
            return HttpResponse(status=200)

        try:
            user = event_msg['user']
        except:
            pass
        else:
            if event_msg['type'] == 'message' and event_msg['channel_type'] == 'channel' and user:

                req_user = SlackUser.objects.get(slack_user=user)

                if req_user.is_stuff:

                    if 'help' in event_msg['text'].lower():
                        print("help")
                        channel = event_msg['channel']
                        response_msg = "Text 'connect' and then your channel will being " \
                                       "get notifications about new posts." \
                                       "Text 'connect' + your prefer category which you want to add for following." \
                                       "And then your channel will being get " \
                                       "notifications about new posts of that category. "
                        client.chat_postMessage(channel=channel, text=response_msg)
                        return HttpResponse(status=200)

                    if ('include' or 'connect') in event_msg['text'].lower():
                        print("include")
                        category = event_msg['text'].split(' ')
                        print(category)

                        channel = event_msg['channel']

                        try:
                            Channel.objects.get(channel_name=channel)
                        except Channel.DoesNotExist:
                            print('add channel to db')
                            new_channel = Channel.objects.create(channel_name=channel)
                        else:
                            new_channel = Channel.objects.get(channel_name=channel)

                        try:
                            category[2]
                        except IndexError:
                            response_msg = "This channel was added for being notify."
                        else:
                            category = category[2]
                            print(category)
                            Category.check_exist(category)
                            new_channel.channel_category.add(Category.objects.get(category_name=category))
                            response_msg = f"This channel was followed the category {category}."

                        client.chat_postMessage(channel=channel, text=response_msg)
                        return HttpResponse(status=200)

            if event_msg['type'] == 'message' and event_msg['channel_type'] == 'im' and user:

                try:
                    SlackUser.objects.get(slack_user=user)
                except SlackUser.DoesNotExist:
                    # print(user)
                    SlackUser.objects.create(slack_user=user)
                    response_msg = ":wave:, Hello, new <@%s>, text 'help', " \
                                   "if you would like to know how to use this bot." % user
                else:
                    response_msg = ":wave:, Hello <@%s> text 'help', " \
                                   "if you would like to know how to use this bot." % user

                for hi in ['hi', 'hello', 'greetings', 'salutation']:

                    if hi in event_msg['text'].lower():
                        print(event_msg['text'].lower())
                        channel = event_msg['channel']
                        client.chat_postMessage(channel=channel, text=response_msg)
                        return HttpResponse(status=200)

                if 'help' in event_msg['text'].lower():
                    print("help")
                    channel = event_msg['channel']
                    response_msg = "Text 'add' + your prefer category which you want to add for following." \
                                   "And then you will being get notifications about new posts of this category." \
                                   "Text 'delete' + your category which you want to add for unfollowing." \
                                   "And then you will stop to being get notifications about new posts of this category."
                    client.chat_postMessage(channel=channel, text=response_msg)
                    return HttpResponse(status=200)

                if 'add' in event_msg['text'].lower():
                    print("add")
                    category = event_msg['text'].split(' ')
                    category = category[1]
                    # print(category)

                    Category.check_exist(category)

                    slack_user = SlackUser.objects.get(slack_user=user)
                    slack_user.slack_category.add(Category.objects.get(category_name=category))
                    slack_user.save()
                    channel = event_msg['channel']
                    response_msg = f"Your category {category} was added."
                    client.chat_postMessage(channel=channel, text=response_msg)
                    return HttpResponse(status=200)

                if 'delete' in event_msg['text'].lower():
                    print("delete")
                    category = event_msg['text'].split(' ')
                    category = category[1]
                    # print(category)
                    slack_user = SlackUser.objects.get(slack_user=user)

                    try:
                        slack_user.slack_category.get(category_name=category)
                    except Category.DoesNotExist:
                        response_msg = f"The category {category} already has been deleted before."
                        print('doesnt exist')
                    else:
                        slack_user.slack_category.remove(Category.objects.get(category_name=category))
                        slack_user.save()
                        print('was deleted')
                        response_msg = f"The category {category} has been deleted."

                    channel = event_msg['channel']
                    client.chat_postMessage(channel=channel, text=response_msg)
                    return HttpResponse(status=200)

                if ('categories' or 'list') in event_msg['text'].lower():
                    print("list")
                    channel = event_msg['channel']
                    slack_user = SlackUser.objects.get(slack_user=user)
                    response_msg = "Your categories:"  # выдаём список категорий
                    if slack_user.get_categories_user():
                        for key in slack_user.get_categories_user():  # перебираем в цикле ключи словаря с категориями
                            # print(key)
                            response_msg = '\n - '.join((response_msg, str(key),))  # соединяем их в строке
                    else:
                        response_msg += ' Empty'

                    client.chat_postMessage(channel=channel, text=response_msg)
                    return HttpResponse(status=200)

    return HttpResponse(status=200)


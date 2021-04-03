import time

import lxml.html
from lxml import etree
from bs4 import BeautifulSoup
import requests as request
import asyncio


async def get_url():
    response = request.get("https://habr.com/ru/company/skillfactory/blog/")
    res = response.content

    soup = BeautifulSoup(response.text, 'lxml')
    last_post_categories = soup.find("ul", {'class': 'post__hubs inline-list'})
    last_post_header = soup.find("h2",  {'class': 'post__title'})
    # last_post_link = soup.find("a", href=True)["href"]
    res = lxml.html.document_fromstring(res)
    last_post_link = ''.join(res.xpath('/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/ul/li[1]/article/h2/a/@href'))
    last_post_text = soup.find("div",  {'class': 'post__text post__text-html post__text_v2'})

    # print(soup)
    print(last_post_categories.text.replace("\n", "").split(',         '))
    print(last_post_link)
    print(last_post_header.text)
    print(last_post_text.text)

    if 'Python' in last_post_categories.text:
        print(True)
    else:
        print(False)


async def main():
    task1 = asyncio.create_task(
        get_url())

    print(f"started at {time.strftime('%X')}")

    await task1

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())

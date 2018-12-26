import json
import os
import tempfile
import re

import requests
from urllib import parse
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from lxml.html.clean import Cleaner

from pages.models import Rules

# Список общих правил упорядоченных по приоретету
# Применяются в случае, если домен с правилами сайта не найден в таблице Rules
# Правила применяются по-порядку: 1 эл. спсика, если не найдено — 2-й элемент списка и тд.
TITLE_RULES_LIST = [
    {"itemprop": "headline"},
    {"class": ["article__heading", "article__title", "story-body__h1", "post__title-text"]},
    ["h1", "title"],
]

TEXT_RULES_LIST = [
    {"itemprop": "articleBody"},
    {"class": ["entry-content", "post__text-html", "article__text", "article_text", "post__article-text",
               "pagedata", "news-text-full", "js-mediator-article"]},
]


def get_title(soup, rules_list: list=None) -> str or None:
    """ Получить заголовок в соостветсвии с правилами """
    if not rules_list:
        rules_list = TITLE_RULES_LIST
    for rule in rules_list:
        title = None
        if type(rule).__name__ in ("str", "list"):
            title = soup.find(rule)
        elif type(rule).__name__ == "dict":
            title = soup.find(attrs=rule)
        if title:
            return md(f'<h1>{title.text}</h1>')
    return ''


def get_text(soup, rules_list: list=None) -> str or None:
    """ Получить текст статьи в соответсвии с правилами """
    if not rules_list:
        rules_list = TEXT_RULES_LIST
    for rule in rules_list:
        text = None
        if type(rule).__name__ in ("str", "list"):
            text = soup.find(rule)
        elif type(rule).__name__ == "dict":
            text = soup.find(attrs=rule)
        if text:
            """ Почистим html код полученной статьи """
            text = re.sub("^\s+|\n|\r|\s+$", '', str(text))
            text = re.sub("><", '> <', text)
            text = re.sub("<div\s", '<p ', text)
            text = re.sub("</div>", '</p> ', text)
            cleaner = Cleaner(
                allow_tags=['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'b', 'i', 'strong', 'em'],
                remove_unknown_tags=False
            )
            text = md(cleaner.clean_html(text))
            text = re.sub("\s{2,}", '\n\n', text)
            text = re.sub("^\s+|\s+$", '', text)
            return text
    return ''


def from_url(url):
    # Получить текст HTML документа
    text = requests.get(url).text
    # Применяем BeautifulSoup
    soup = BeautifulSoup(text, 'lxml')
    # Парсим ссылку
    url_parsed = parse.urlparse(url)

    # Если ли правила для конкретного сайта?
    try:
        rules = Rules.objects.get(site=url_parsed.netloc)
    except Rules.DoesNotExist:
        rules = None

    article_body = list()

    # Находим и добавляем заголовок
    article_body.append(
        get_title(soup, json.loads(rules.title) if rules else None)
    )
    # Находим и тело статьи
    article_body.append(
        get_text(soup, json.loads(rules.content) if rules else None)
    )

    # Объединяем заголовок и текст
    article = "".join(article_body)

    # Поправляем относительные ссылки
    article = article.replace('](/', f']({url_parsed.scheme}://{url_parsed.netloc}/')

    # Сохраняем текст в формате Markdown
    file_path = os.path.join(tempfile.gettempdir(), 'index.md')
    file = open(file_path, "w")
    file.write(article)
    file.close()

    return file_path, article

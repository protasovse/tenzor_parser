import os
from urllib import parse

from django.db import models
from markdownx.models import MarkdownxField


def url_to_path(instance, filename):
    url_parsed = parse.urlparse(instance.url)
    path = os.path.join(url_parsed.netloc, url_parsed.path[1:], filename)
    return path


class Rules(models.Model):
    site = models.CharField(
        'Шаблон для url сайта',
        max_length=255,
    )

    title = models.CharField(
        'Селектор для заголовка',
        blank=True,
        null=True,
        max_length=255,
    )

    content = models.TextField(
        'Селекторы для содержания',
        blank=True,
        null=True,
        max_length=255,
    )

    class Meta:
        verbose_name = 'Правило'
        verbose_name_plural = 'Правила'

    def __str__(self):
        return self.site


class Content(models.Model):

    url = models.URLField(
        'Ссылка',
        max_length=255,
    )

    content = MarkdownxField(
        'Содержание',
    )

    file = models.FileField(
        'Файл с содержанием',
        upload_to=url_to_path
    )

    class Meta:
        verbose_name = 'Содержание'
        verbose_name_plural = 'Содержание'

    def __str__(self):
        return self.url

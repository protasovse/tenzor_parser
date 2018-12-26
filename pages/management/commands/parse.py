from django.core.files import File
from django.core.management.base import BaseCommand

from pages import parser
from pages.models import Content


class Command(BaseCommand):
    help = 'Выборка полезного содержимого со страницы'

    def handle(self, *args, **options):
        if options['url']:
            file_path, text = parser.from_url(options['url'])
            Content.objects.create(
                url=options['url'],
                content=text,
                file=File(open(file_path, "rb"), 'index.md'),
            )

    def add_arguments(self, _parser):
        _parser.add_argument(
            '-u',
            '--url',
            action='store',
            nargs='?',
            required=True,
            type=str,
            help='URL страницы'
        )

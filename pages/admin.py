from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from pages.models import Content, Rules

admin.site.register(Content, MarkdownxModelAdmin)


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    ...

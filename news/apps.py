from django.utils.translation import pgettext
from django.apps import AppConfig


class JudgeConfig(AppConfig):
        name = 'news'
        verbose_name = pgettext("Plural", "News")

#-*- coding: utf-8 -*-
from django.utils.translation import pgettext_lazy
from django.apps import AppConfig


class NewsConfig(AppConfig):
        name = 'news'
        verbose_name = pgettext_lazy("Plural", "News")

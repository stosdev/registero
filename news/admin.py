#-*- coding: utf-8 -*-
from django.contrib import admin

from models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp')

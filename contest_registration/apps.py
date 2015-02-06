from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class JudgeConfig(AppConfig):
        name = 'contest_registration'
        verbose_name = _("Contest registration")

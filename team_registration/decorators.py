# -*- coding: utf-8 -*-

from django.utils import timezone

from django.core.exceptions import PermissionDenied

from models import TeamRegistrationConfiguration


def team_registration_enabled(function):
    """Checks if team registration is enabled, if not raises an exception."""

    def wrap(*args, **kwargs):
        config = TeamRegistrationConfiguration.get_solo()
        if config.enabled and config.start <= timezone.now() \
           and timezone.now() <= config.end:
            return function(*args, **kwargs)
        raise PermissionDenied()

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

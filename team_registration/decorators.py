# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied

from models import TeamRegistrationConfiguration


def team_registration_active(function):
    """Checks if team registration is active, if not raises an exception."""

    def wrap(*args, **kwargs):
        config = TeamRegistrationConfiguration.get_solo()
        if not config.registration_is_active:
            raise PermissionDenied()
        return function(*args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def team_registration_unfreezed(function):
    """Checks if the team registration is not freezed, raises an exception if is."""

    def wrap(*args, **kwargs):
        config = TeamRegistrationConfiguration.get_solo()
        if config.registration_is_freezed:
            raise PermissionDenied()
        return function(*args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

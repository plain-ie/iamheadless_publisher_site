from django.core.exceptions import SuspiciousOperation
from django.shortcuts import redirect, reverse

from .conf import settings
from . import utils


def has_allowed_language(*args, **kwargs):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):

            allow_none = kwargs.get('allow_none', False)
            language = utils.get_request_language(request)
            allowed_languages = utils.get_allowed_language_codes()
            response = view_func(request, *args, **kwargs)

            if 'favicon.ico' in request.path:
                return response

            if allow_none is True and language is None:
                return response

            if language not in allowed_languages:
                raise SuspiciousOperation('Language is not allowed')

            return response
        return wrap
    return decorator

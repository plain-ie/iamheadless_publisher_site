from django.conf import settings as dj_settings

from .conf import settings
from .loader import load


def get_client():
    return settings.API_CLIENT


def get_request_language(request):
    return request.resolver_match.kwargs.get('language', settings.DEFAULT_LANGUAGE[0])


def get_request_item_type(request):
    return request.resolver_match.kwargs.get('item_type', None)


def get_request_slug(request):
    return request.resolver_match.kwargs.get('slug', None)


def get_url_patterns():
    return settings.ITEM_TYPE_REGISTRY.get_urlpatterns()


def get_allowed_language_codes():
    languages = []
    for x in settings.LANGUAGES:
        languages.append(x[0])
    return languages

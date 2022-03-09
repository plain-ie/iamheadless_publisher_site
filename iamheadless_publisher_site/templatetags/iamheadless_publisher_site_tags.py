import datetime

from django import template

from .conf import settings
from .. import utils


register = template.Library()


@register.simple_tag
def build_id():
    build_id = getattr(settings, 'BUILD_ID', None)
    if build_id is None:
        build_id = datetime.datetime.now().strftime('%Y%m%d%H%M')
    return build_id


@register.simple_tag
def define(value):
    return value


@register.inclusion_tag(settings.FOOTER_TEMPLATE, takes_context=True)
def footer(context):
    request = context['request']
    return {
        'request': request
    }


@register.inclusion_tag(settings.MAIN_MENU_TEMPLATE, takes_context=True)
def main_menu(context):

    request = context['request']

    language = utils.get_request_language(request)

    home_url_kwargs = {}
    if language is not None:
        home_url_kwargs['language'] = language
    home_url = '/'

    language_links = context.get('language_links', [])

    return {
        'brand_image': None,
        'brand_link': home_url,
        'brand_title': settings.PROJECT_TITLE,
        'language': language,
        'language_links': language_links,
        'request': request,
    }


@register.simple_tag
def project_title():
    return settings.PROJECT_TITLE


@register.filter(name='pydantic_model_value')
def pydantic_model_value(model, key):
    return getattr(model, key, None)


@register.filter(name='pydantic_model_content')
def pydantic_model_content(model, language):
    data = model.get_display_data(language)
    return data['title']


@register.filter(name='pydantic_model_url')
def pydantic_model_url(model, language):
    return model.get_item_url(language)


@register.simple_tag
def setting(name):
    return getattr(settings, name)


@register.simple_tag(takes_context=True)
def site_language(context):
    return utils.get_request_language(context['request'])


@register.simple_tag(takes_context=True)
def site_language(context):
    return utils.get_request_language(context['request'])

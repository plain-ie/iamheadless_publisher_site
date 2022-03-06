import datetime

from django import template

from .. import utils


register = template.Library()


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


@register.simple_tag(takes_context=True)
def site_language(context):
    return utils.get_request_language(context['request'])


@register.simple_tag(takes_context=True)
def site_language(context):
    return utils.get_request_language(context['request'])

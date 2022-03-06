import datetime
from typing import List, Optional
from pydantic import BaseModel

from django.core.exceptions import ValidationError

from iamheadless_markdown.conf import settings as iamheadless_markdown_settings

from .conf import settings


class BaseItemContentsPydanticModel(BaseModel):

    @classmethod
    def get_language(cls, data):
        return data['language']

    @classmethod
    def get_title(cls, data):
        return data['title']

    @classmethod
    def get_slug(cls, data):
        return data['slug']

    @classmethod
    def get_content(cls, data):
        return data['content']

    @classmethod
    def get_seo_description(cls, data):
        return data.get('seo_description', '')

    @classmethod
    def get_seo_keywords(cls, data):
        return data.get('seo_keywords', '')


class BaseItemDataPydanticModel(BaseModel):
    pass


class BaseItemPydanticModel(BaseModel):

    _content_model = BaseItemContentsPydanticModel
    _data_model = BaseItemDataPydanticModel
    _display_name_plural = None
    _display_name_singular = None
    _item_type = None
    _primary_language = settings.DEFAULT_LANGUAGE[0]
    _secondary_language = None
    _urlpatterns = []

    #
    id: Optional[str]
    #
    item_type: str
    data: _data_model
    #
    project: str
    tenant: Optional[str]
    #
    updated_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]

    #

    def parse_markdown(self, text, language):
        parser = iamheadless_markdown_settings.WIDGET_REGISTRY
        return parser.parse(text)

    def get_display_data(self, language):
        data = type(self).get_display_content(self.CONTENTS, language)

        title = self._content_model.get_title(data)
        content = self._content_model.get_content(data)
        seo_description = self._content_model.get_seo_description(data)
        seo_keywords = self._content_model.get_seo_keywords(data)

        return {
            'title': self._content_model.get_title(data),
            'slug': self._content_model.get_slug(data),
            'language': self._content_model.get_language(data),
            'content': self.parse_markdown(content, language),
            'seo_description': seo_description,
            'seo_keywords': seo_keywords,
        }

    def get_item_url(self, language):
        return '#'
    #

    @property
    def CONTENTS(self):
        return []

    #

    def get_urls_for_language(self):
        links = []
        for x in settings.LANGUAGES:
            language = x[0]
            links.append({
                'url': self.get_item_url(language),
                'display_name': x[1],
                'language': language,
            })
        return links

    #

    @classmethod
    def get_item_type(cls, data):
        return data.get('item_type', None)

    @classmethod
    def get_display_content(
            cls,
            contents,
            requested_language,
            ):

        _contents = {}

        primary_content = None
        secondary_content = None

        # Change list to dict
        for content in contents:
            language = cls._content_model.get_language(content)
            _contents[language] = content

        try:
            primary_content = _contents[cls._primary_language]
        except KeyError:
            pass

        if cls._secondary_language is not None:
            try:
                secondary_content = _contents[cls._secondary_language]
            except KeyError:
                pass

        try:
            return _contents[requested_language]
        except KeyError:
            pass

        if primary_content is None and secondary_content is None:
            raise ValidationError('No content to display')

        if primary_content is None:
            return secondary_content

        return primary_content

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from ..conf import settings
from .. import utils
from .base import BaseViewSet


class ItemsViewSet(BaseViewSet):

    client = utils.get_client()
    count = 10
    project_id = settings.PROJECT_ID
    template = None
    param_name_page = 'page'

    def get(self, request, language):
        return render(request, self.get_template(), context=self.get_context())

    def get_context(self):

        items = self.get_items()

        total = items['total']
        pages = items['pages']
        results = items['results']

        return {
            'current_page': self.get_page(),
            'language': utils.get_request_language(self.request),
            'next_url': self.get_next_url(pages),
            'page': {
                'title': None,
                'content': None,
                'seo_keywords': None,
                'seo_description': None,
            },
            'previous_url': self.get_previous_url(pages),
            'results': results,
            'total': total,
            'total_pages': pages,
        }

    def get_browsable_item_types(self):
        return []

    def get_items(self):

        browsable_item_types = self.get_browsable_item_types()

        kwargs = {
            'published': True,
            'count': self.count,
            'page': self.get_page(),
        }

        if len(browsable_item_types) != 0:
            kwargs['item_type'] = browsable_item_types

        items = self.client.retrieve_items(
            settings.PROJECT_ID,
            **kwargs,
        )

        return {
            'results': items['results'],
            'page': items['page'],
            'pages': items['pages'],
            'total': items['total'],
        }

    def get_page(self):
        params = getattr(self.request, self.request.method, {})
        page = params.get(self.param_name_page, '1')
        if page.isdigit() is True:
            return int(page)
        return 1

    def get_previous_url(self, pages=1):
        return None

    def get_next_url(self, pages=1):
        return None

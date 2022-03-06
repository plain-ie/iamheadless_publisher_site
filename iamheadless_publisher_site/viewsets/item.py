from django.core.exceptions import ObjectDoesNotExist

from ..conf import settings
from .. import utils
from .base import BaseViewSet


class ItemViewSet(BaseViewSet):

    client = utils.get_client()
    project_id = settings.PROJECT_ID
    template = None

    def get(self, request, language, item_type, slug, ):
        return render(request, self.get_template(), context=self.get_context())

    def get_context(self):

        language = utils.get_request_language(self.request)
        item_type = utils.get_request_item_type(self.request)

        pydantic_model = settings.ITEM_TYPE_REGISTRY.find(item_type)

        item = self.get_item()

        if item is None:
            raise ObjectDoesNotExist('')

        return {
            'instance': item,
            'language': language,
            'language_links': item.get_urls_for_language(),
            'page': item.get_display_data(language),
        }

    def get_item(self):

        item_type = self.get_item_type()
        slug = utils.get_request_slug(self.request)

        return self.client.retrieve_item(
            project_id=self.project_id,
            item_id=slug,
            lookup_field=f'text_lookup_indexes__field_name||slug||{slug}'
        )

    def get_item_type(self):
        item_type = utils.get_request_item_type(self.request)
        try:
            return settings.ITEM_TYPE_MAP[item_type]
        except KeyError:
            pass
        return item_type

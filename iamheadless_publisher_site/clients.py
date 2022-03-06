import json

from .conf import settings


class BaseClient:

    def __init__(self, *args, **kwargs):
        self.dependencies_check()

    def dependencies_check(self):
        pass


# class ApiClient(BaseClient):
#
#     API_URL = settings.API_URL
#
#     def dependencies_check(self):
#         if self.API_URL is None:
#             raise ValueError('API_URL cannot be None')


class ModelClient(BaseClient):

    def dependencies_check(self):
        pass

    def retrieve_items(
            self,
            project_id,
            count=10,
            index_filters=None,
            item_type=None,
            page=1,
            published=None,
            tenant_id=None,
            token=None,
            unpublished=None,
            ):

        from iamheadless_publisher_api.lookups.items_retrieve import retrieve_items as publisher_retrieve_items

        data = publisher_retrieve_items(
            count=count,
            index_filters=index_filters,
            item_ids=None,
            item_types=item_type,
            project_ids=project_id,
            page=page,
            paginate=True,
            published=published,
            tenant_ids=tenant_id,
            unpublished=unpublished,
            format='json'
        )

        data = json.loads(data)

        data['results'] = settings.ITEM_TYPE_REGISTRY.serialize(data['results'], many=True)

        return data

    def retrieve_item(
            self,
            item_id,
            project_id=None,
            tenant_id=None,
            lookup_field='id',
            token=None,
            format='json'
            ):

        from iamheadless_publisher_api.lookups.item_retrieve import retrieve_item as publisher_retrieve_item

        data = publisher_retrieve_item(
            item_id,
            lookup_field=lookup_field,
            format=format
        )

        if data is None:
            return None

        if format == 'dict':
            return data

        data = json.loads(data)

        return settings.ITEM_TYPE_REGISTRY.serialize(data)

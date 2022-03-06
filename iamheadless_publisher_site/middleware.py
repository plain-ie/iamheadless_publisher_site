from django.core.cache import cache
from django.shortcuts import redirect
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

from .conf import settings
from . import utils


class IamheadlessPublisherSiteRedirectMiddleware(MiddlewareMixin):

    def process_request(self, request):

        CHECK = settings.CHECK_REDIRECTS

        if CHECK is True:
            if request.path.startswith('/admin/') is True or 'favicon.ico' in request.path:
                CHECK = False

        if CHECK is True:

            url = request.build_absolute_uri()
            client = utils.get_client()

            cache_key = 'iamheadless_publisher_site__'
            cache_key += 'redirect_middleware__'
            cache_key += 'source_url__'
            cache_key += f'{url}'

            cached_data = cache.get(cache_key, '--unset')

            if cached_data in [None, 'None']:
                return None

            item = client.retrieve_item(
                project_id=settings.PROJECT_ID,
                item_id=url,
                lookup_field=f'text_lookup_indexes__field_name||source_url||{url}',
                format='dict'
            )

            if item is not None:
                cached_data = item['data']['destination_url']
            else:
                cached_data = None

            cache.set(cache_key, cached_data, settings.CACHE_TIMEOUT_REDIRECTS)

            if cached_data is None:
                return None

            return redirect(cached_data)

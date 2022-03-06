from .conf import settings


urlpatterns = settings.ITEM_TYPE_REGISTRY.get_urlpatterns()

from .conf import settings


print(settings.ITEM_TYPE_REGISTRY.item_types)


urlpatterns = settings.ITEM_TYPE_REGISTRY.get_urlpatterns()

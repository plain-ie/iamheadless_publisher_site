from django.conf import settings as dj_settings

from .apps import IamheadlessPublisherSiteConfig
from .loader import load


class Settings:

    _API_CLIENT = None
    _ITEM_TYPE_MAP = None
    _ITEM_TYPE_REGISTRY = None

    APP_NAME = IamheadlessPublisherSiteConfig.name
    VAR_PREFIX = APP_NAME.upper()

    VAR_API_CLIENT = f'{VAR_PREFIX}_API_CLIENT'
    VAR_API_URL = f'{VAR_PREFIX}_API_URL'
    VAR_CHECK_REDIRECTS = f'{VAR_PREFIX}_CHECK_REDIRECTS'
    VAR_DEFAULT_LANGUAGE = f'{VAR_PREFIX}_DEFAULT_LANGUAGE'
    VAR_ITEM_TYPE_REGISTRY_CLASS = f'{VAR_PREFIX}_ITEM_TYPE_REGISTRY_CLASS'
    VAR_LANGUAGES = f'{VAR_PREFIX}_LANGUAGES'
    VAR_PROJECT_ID = f'{VAR_PREFIX}_PROJECT_ID'
    VAR_PROJECT_TITLE = f'{VAR_PREFIX}_PROJECT_TITLE'
    VAR_SERIALIZER_LIST = f'{VAR_PREFIX}_SERIALIZER_LIST'
    VAR_GOOGLE_ANALYTICS_ID = f'{VAR_PREFIX}_GOOGLE_ANALYTICS_ID'
    #
    VAR_FOOTER_TEMPLATE = f'{VAR_PREFIX}_FOOTER_TEMPLATE'
    VAR_MAIN_MENU_TEMPLATE = f'{VAR_PREFIX}_MAIN_MENU_TEMPLATE'
    VAR_TEMPLATE = f'{VAR_PREFIX}_TEMPLATE'

    CACHE_TIMEOUT_REDIRECTS = 10

    @property
    def API_CLIENT(self):

        if self._API_CLIENT is not None:
            return self._API_CLIENT

        client = getattr(
            dj_settings,
            self.VAR_API_CLIENT,
            f'{self.APP_NAME}.clients.ModelClient'
        )

        self._API_CLIENT = load(client)()

        return self._API_CLIENT

    @property
    def DEFAULT_LANGUAGE(self):
        return getattr(
            dj_settings,
            self.VAR_DEFAULT_LANGUAGE,
            ('en', 'English')
        )

    @property
    def CHECK_REDIRECTS(self):
        return getattr(
            dj_settings,
            self.VAR_CHECK_REDIRECTS,
            True
        )

    @property
    def GOOGLE_ANALYTICS_ID(self):
        return getattr(
            dj_settings,
            self.VAR_GOOGLE_ANALYTICS_ID,
            True
        )


    @property
    def LANGUAGES(self):
        return getattr(
            dj_settings,
            self.VAR_LANGUAGES,
            (self.DEFAULT_LANGUAGE, )
        )

    @property
    def ITEM_TYPE_MAP(self):
        if self._ITEM_TYPE_MAP is not None:
            return self._ITEM_TYPE_MAP
        self._ITEM_TYPE_MAP = {}
        return self._ITEM_TYPE_MAP

    @property
    def ITEM_TYPE_REGISTRY_CLASS(self):
        return getattr(
            dj_settings,
            self.VAR_ITEM_TYPE_REGISTRY_CLASS,
            f'{self.APP_NAME}.registry.ItemTypeRegistry'
        )

    @property
    def ITEM_TYPE_REGISTRY(self):
        if self._ITEM_TYPE_REGISTRY is not None:
            return self._ITEM_TYPE_REGISTRY
        self._ITEM_TYPE_REGISTRY = load(self.ITEM_TYPE_REGISTRY_CLASS)()
        return self._ITEM_TYPE_REGISTRY

    @property
    def LANGUAGES(self):
        return getattr(dj_settings, self.VAR_LANGUAGES, None)

    @property
    def PROJECT_ID(self):
        return getattr(dj_settings, self.VAR_PROJECT_ID, None)

    @property
    def PROJECT_TITLE(self):
        return getattr(dj_settings, self.VAR_PROJECT_TITLE, '')

    @property
    def SERIALIZER_LIST(self):
        return getattr(dj_settings, self.VAR_SERIALIZER_LIST, [])

    #
    #
    #

    @property
    def FOOTER_TEMPLATE(self):
        return getattr(
            dj_settings,
            self.VAR_FOOTER_TEMPLATE,
            f'{self.APP_NAME}/footer.html'
        )

    @property
    def MAIN_MENU_TEMPLATE(self):
        return getattr(
            dj_settings,
            self.VAR_MAIN_MENU_TEMPLATE,
            f'{self.APP_NAME}/main_menu.html'
        )

    @property
    def TEMPLATE(self):
        return getattr(
            dj_settings,
            self.VAR_TEMPLATE,
            f'{self.APP_NAME}/item.html'
        )


settings = Settings()

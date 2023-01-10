import logging
from functools import lru_cache
from typing import List

from core.config import get_config
from core.provider.interfaces import IProvider
from core.provider.loader.provider import ProviderLoader


class ProviderManager(object):
    def __init__(self, namespace, provider_list=None):
        self.__providers = {}
        providers = ProviderLoader(namespace, provider_list).load()

        for provider in providers:
            logging.error('Init provider %s', provider.name)
            self.__providers.update({provider.name: provider})

    @property
    def providers(self) -> List[IProvider]:
        return self.__providers.values()

    @property
    def provider_names(self) -> List[str]:
        return list(self.__providers.keys())

    def get_provider(self, name) -> IProvider:
        assert name in self.__providers.keys(), 'No such provider'
        return self.__providers[name]


@lru_cache()
def get_provider_manager() -> ProviderManager:
    return ProviderManager(get_config().provider_namespace)

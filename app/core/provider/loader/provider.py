import logging
import os
from typing import List

import yaml

from core.exceptions.app import AppError
from core.provider.interfaces import IProvider, IProviderConfig
from core.provider.loader.class_loader import ClassLoader


class ProviderLoader:
    def __init__(self, namespace, providers=None) -> None:
        self.namespace = namespace
        self.providers = providers

    def load(self) -> List[IProvider]:
        subdirs = os.listdir(self.namespace)

        config_dict = {}
        providers = []

        for subdir in subdirs:
            try:
                provider_namespace = f'{self.namespace}.{subdir}'
                config_path = os.path.join(
                    self.namespace, subdir, '.config.yaml'
                )
                if not os.path.exists(config_path):
                    raise AppError(
                        f"no \'.config.yaml\' for {provider_namespace}"
                    )

                provider_configs = ClassLoader(
                    recurse=False
                ).load(provider_namespace, subclasses=IProviderConfig)
                provider_classes = ClassLoader(
                    recurse=False
                ).load(provider_namespace, subclasses=IProvider)
                
                if len(provider_configs) != 1:
                    raise AppError(
                        f'configs len in {provider_namespace} \
                            1 but {len(provider_configs)}'
                    )
                if len(provider_classes) != 1:
                    raise AppError(
                        f'providers len in {provider_namespace} \
                            1 but {len(provider_classes)}'
                    )

                config = provider_configs[0]
                provider = provider_classes[0]

                with open(config_path, 'r') as reader:
                    config_dict.update(yaml.safe_load(reader))
                instance = provider(config(**config_dict))
                providers.append(instance)
            except Exception:
                logging.error(
                    'can not import provider from %s', 
                    provider_namespace, exc_info=True
                )

        return providers

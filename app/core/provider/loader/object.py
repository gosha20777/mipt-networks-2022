from core.provider.loader.base import Loader
from core.provider.loader.module import ModuleLoader


class ObjectLoader(Loader):
    """
    Loads classes or objects out of modules in a namespace, based on a
    provided criteria.

    The load() method returns all objects exported by the module.
    """
    def __init__(self, recurse=False):
        super().__init__()
        self.module_loader = ModuleLoader(recurse=recurse)

    def _fill_cache(self, namespace):
        modules = self.module_loader.load(namespace)
        objects = []

        for module in modules:
            for attr_name in dir(module):
                if not attr_name.startswith('_'):
                    objects.append(getattr(module, attr_name))

        self._cache = objects
        return objects

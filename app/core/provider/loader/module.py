import os
import sys
from importlib import import_module

from core.provider.loader.base import Loader


class ModuleLoader(Loader):
    """
    Performs the work of locating and loading straight plugins.
    This looks for plugins in every location in the import path.
    """

    def __init__(self, recurse=False):
        super(ModuleLoader, self).__init__()
        self.recurse = recurse

    @staticmethod
    def __is_package(path):
        pkg_init = os.path.join(path, '__init__.py')
        return os.path.exists(pkg_init)

    def __find_plugin_file_paths(self, namespace):
        already_seen = set()

        # Look in each location in the path
        for path in set(sys.path):

            # Within this, we want to look for a package for the namespace
            namespace_rel_path = namespace.replace('.', os.path.sep)
            namespace_path = os.path.join(path, namespace_rel_path)
            try:
                for possible in os.listdir(namespace_path):
                    poss_path = os.path.join(namespace_path, possible)

                    if self.__is_package(poss_path) and self.recurse:
                        subns = '.'.join(
                            (namespace, possible.split('.py')[0])
                        )
                        for path in self.__find_plugin_file_paths(subns):
                            yield path
                        base = possible
                    else:
                        base, ext = os.path.splitext(possible)
                        if base == '__init__' or ext != '.py':
                            continue

                    if base not in already_seen:
                        already_seen.add(base)
                        yield os.path.join(namespace, possible)
            except (FileNotFoundError, NotADirectoryError):
                pass

    def __find_plugin_modules(self, namespace):
        for filepath in self.__find_plugin_file_paths(namespace):
            path_segments = list(filepath.split(os.path.sep))
            path_segments = [p for p in path_segments if p]
            path_segments[-1] = os.path.splitext(path_segments[-1])[0]
            import_path = '.'.join(path_segments)

            try:
                module = import_module(import_path)
            except ImportError:
                raise Exception(import_path)

            if module is not None:
                yield module

    def _fill_cache(self, namespace):
        """Load all modules found in a namespace."""

        modules = self.__find_plugin_modules(namespace)

        self._cache = list(modules)

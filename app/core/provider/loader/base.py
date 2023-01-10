class Loader:
    """Base loader class. Only used as a base-class for other loaders."""

    def __init__(self, *args, **kwargs):
        self._cache = []
        self.loaded = False

    def _fill_cache(self, *args, **kwargs):
        raise NotImplementedError()

    def load(self, *args, **kwargs):
        if not self.loaded:
            self._fill_cache(*args, **kwargs)
            self._post_fill()
            self._order()
            self.loaded = True
        return self._cache

    def _meta(self, plugin):
        return getattr(plugin, '__plugin__', None)

    def _post_fill(self):
        for plugin in self._cache:
            meta = self._meta(plugin)

            if not getattr(meta, 'load', True):
                self._cache.remove(plugin)

            for implied_namespace in getattr(meta, 'imply_plugins', []):
                plugins = self._cache
                self._cache = self.load(implied_namespace)
                self._post_fill()
                combined = []
                combined.extend(plugins)
                combined.extend(self._cache)
                self._cache = combined

    def _order(self):
        self._cache.sort(key=self._plugin_priority, reverse=True)

    def _plugin_priority(self, plugin):
        meta = self._meta(plugin)
        return getattr(meta, 'priority', 0.0)

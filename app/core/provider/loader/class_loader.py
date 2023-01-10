from core.provider.loader.object import ObjectLoader


class ClassLoader(ObjectLoader):
    """
    Loads classes out of plugin modules which are subclasses of a single
    given base class.
    """
    def _fill_cache(self, namespace, subclasses=None):
        objects = super(ClassLoader, self)._fill_cache(namespace)
        classes = []

        for cls in objects:
            if isinstance(cls, type):  # TODO: добавим AND?
                if issubclass(cls, subclasses) and cls is not subclasses:
                    classes.append(cls)

        self._cache = classes
        return classes

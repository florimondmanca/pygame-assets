"""Utility decorators."""


def loader_function(loader_cls):
    def wrapper(loader_f):
        def load_asset(*args, **kwargs):
            loader = loader_cls()
            return loader.load(*args, **kwargs)
        return load_asset
    return wrapper

"""Provides the ability to handle package index files."""
from typing import List, Type

from dismantle.index._handlers import (
    IndexHandler,
    JsonFileIndexHandler,
    JsonUrlIndexHandler
)

__all__ = [
    'IndexHandler',
    'JsonFileIndexHandler',
    'JsonUrlIndexHandler'
]

indicies_list: List[str] = []
handlers_list: List[Type[IndexHandler]] = []
cache: str


def get_packages():
    """Get the list of package meta from all the provided indexes."""
    packages = {}

    for index in indicies_list:
        for handler in handlers_list:
            if handler.handles(index):
                data = handler(index, cache)
                packages.update(data.packages())

    return packages


def add_indicies(indicies: List[str]) -> None:
    """Add the indicies to be processed."""
    global indicies_list
    indicies_list.extend(indicies)


def set_cache(cache_dir: str) -> None:
    """Set the cache directory to store the index."""
    global cache
    cache = cache_dir


def add_handlers(handlers: List[Type[IndexHandler]]) -> None:
    """Add a handler to the list of supported index handlers."""
    global handlers_list
    handlers_list.extend(handlers)

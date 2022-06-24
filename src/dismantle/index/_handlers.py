"""Base handler classes."""
import abc
import atexit
import json
import tempfile
from hashlib import md5
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Union

import requests


class IndexHandler(metaclass=abc.ABCMeta):
    """Creates a base index handler to be extended."""

    @abc.abstractmethod
    def __init__(self, path: str, cache_dir: Optional[str] = None) -> None:
        """Ensure a string path is provided."""
        ...

    @abc.abstractmethod
    def __getitem__(self, index) -> Any:
        """Add the ability to extend __getitem__."""
        ...

    @abc.abstractmethod
    def __len__(self) -> int:
        """Add the ability to extend __len__."""
        ...

    @abc.abstractmethod
    def __iter__(self) -> Iterator:
        """Add the ability to extend __iter__."""
        ...

    @abc.abstractmethod
    def packages(self) -> Dict:
        """Add the ability to extend __getitem__."""
        ...

    @abc.abstractmethod
    def find(self) -> Union[list, None]:
        """Add interface to index finder."""
        ...

    @abc.abstractmethod
    def update(self) -> bool:
        """Add interface for extendable updater."""
        ...

    @staticmethod
    @abc.abstractmethod
    def handles(index: Union[str, Path]) -> bool:
        """Add interface for checking if a handler can handle index."""
        ...

    @property
    @abc.abstractmethod
    def outdated(self) -> bool:
        """Add interface to check if an index is outdated."""
        ...


class JsonFileIndexHandler(IndexHandler):
    """Local file handler."""

    def __init__(self, path: str, cache_dir: Optional[str] = None) -> None:
        """With the given path, process data and return the results."""
        path = str(path)[7:] if str(path)[:7] == 'file://' else str(path)
        self._path = Path(path)
        if not self._path.exists():
            message = 'index file not found'
            raise FileNotFoundError(message)
        with open(self._path) as json_file:
            self._data = json.load(json_file)

    def __getitem__(self, index) -> Any:
        """Get an item from the _data list read from the json file."""
        return self._data.__getitem__(index)

    def __len__(self) -> int:
        """Return length of _data list returned from the json file."""
        return self._data.__len__()

    def __iter__(self) -> Iterator:
        """Return the list of packages contained within the index."""
        return iter(self._data)

    def packages(self) -> Dict:
        """Return the list of packages defined."""
        return self._data

    def find(self, value: str) -> Union[list, None]:
        """Find packages matching a specified value."""
        return [s for s in self._data if value.lower() in s.lower()]

    def update(self) -> bool:
        """Update the index file."""
        return True

    @staticmethod
    def handles(index: Union[str, Path]) -> bool:
        """Check if the index format is file:// or a path."""
        path = str(index)[7:] if str(index)[:7] == 'file://' else index
        try:
            return Path(str(path)).exists()
        except OSError:
            return False

    @property
    def outdated(self) -> bool:
        """Check if the index is outdated."""
        return False


class JsonUrlIndexHandler(IndexHandler):
    """Use a json file located on a remote server."""

    def __init__(self, index: str, cache_dir: Optional[str] = None) -> None:
        """With given path, process the data and return the results."""
        self._index = index
        if not cache_dir:
            tmp_cache_dir = tempfile.TemporaryDirectory()
            atexit.register(tmp_cache_dir.cleanup)
            cache_dir = str(tmp_cache_dir)
        self._cache = Path(cache_dir)
        self._cache.mkdir(0x777, True, True)
        self._cached_index = Path(self._cache, 'index.json')
        self._cached_index.touch(exist_ok=True)
        self._updated = False
        self.update()
        with open(self._cached_index) as json_file:
            self._data = json.load(json_file)

    def __getitem__(self, index) -> Any:
        """Get an item from the _data list read from the json file."""
        return self._data.__getitem__(index)

    def __len__(self) -> int:
        """Return length of _data list returned from the json file."""
        return self._data.__len__()

    def __iter__(self) -> Iterator:
        """Return the list of packages contained within the index."""
        return iter(self._data)

    def packages(self) -> Dict:
        """Return the list of packages defined."""
        return self._data

    def find(self, value: str) -> Union[list, None]:
        """Find packages matching a specified value."""
        return [s for s in self._data if value.lower() in s.lower()]

    def update(self) -> None:
        """Update the index file if its outdated."""
        self._updated = False
        headers = {'If-None-Match': self._digest}
        req = requests.get(self._index, headers=headers, allow_redirects=True)
        if req.status_code not in [200, 304]:
            raise FileNotFoundError(req.status_code)
        elif req.status_code == 200:
            with open(self._cached_index, 'wb') as cached_index:
                cached_index.write(req.content)
            self._updated = True

    @staticmethod
    def handles(index: Union[str, Path]) -> bool:
        """Check if the index format is file:// or a path."""
        return str(index)[0:4] == 'http'

    @property
    def outdated(self) -> bool:
        """Check if an index is outdated.

        Execute a head request using the requests library to check that
        the ETag matches.
        """
        headers = {'If-None-Match': self._digest}
        req = requests.head(self._index, headers=headers, allow_redirects=True)
        if req.status_code not in [200, 304]:
            raise FileNotFoundError(req.status_code)
        elif req.status_code == 200:
            return True
        else:
            return False

    @property
    def _digest(self) -> str:
        """Return the md5 digest of the currently cached index file."""
        digest = md5()  # noqa: S303
        with open(self._cached_index, 'rb') as cached_index:
            for block in iter(lambda: cached_index.read(65536), b''):
                digest.update(block)
        return digest.hexdigest()

# Copyright 2021 Gary Stidston-Broadbent
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import abc
import atexit
import json
import tempfile
from hashlib import md5
from pathlib import Path
from typing import Any, Iterator, Union
import requests


class IndexHandler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __getitem__(self, index) -> Any:
        ...

    @abc.abstractmethod
    def __len__(self) -> int:
        ...

    @abc.abstractmethod
    def __iter__(self) -> Iterator:
        ...

    @abc.abstractmethod
    def find(self) -> Union[list, None]:
        ...

    @abc.abstractmethod
    def update(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def outdated(self) -> bool:
        ...


class JsonFileIndexHandler(IndexHandler):
    """Local file handler."""
    def __init__(self, path: str) -> None:
        """With the given path, process the data and return the results."""
        path = str(path)[7:] if str(path)[:7] == 'file://' else str(path)
        self._path = Path(path)
        if not self._path.exists():
            message = 'index file not found'
            raise FileNotFoundError(message)
        with open(self._path) as json_file:
            self._data = json.load(json_file)

    def __getitem__(self, index) -> any:
        """Get an item from the _data list read from the json file."""
        return self._data.__getitem__(index)

    def __len__(self) -> int:
        """Return the length of the _data list returned from the json file."""
        return self._data.__len__()

    def __iter__(self) -> Iterator:
        """Return the list of packages contained within the index."""
        return iter(self._data)

    def find(self, value: str) -> Union[list, None]:
        """Find packages matching a specified value."""
        return [s for s in self._data if value.lower() in s.lower()]

    def update(self) -> bool:
        """As the file is referenced directly, there is no need to update the
        index.
        """
        return True

    @property
    def outdated(self) -> bool:
        """As the file is referenced directly, there is no need to check the
        age.
        """
        return False


class JsonUrlIndexHandler(IndexHandler):
    """Use a json file located on a remote server."""
    def __init__(self, index: str, cache_dir: str = None) -> None:
        """With the given path, process the data and return the results."""
        self._index = index
        if not cache_dir:
            cache_dir = tempfile.TemporaryDirectory()
            atexit.register(cache_dir.cleanup)
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
        """Return the length of the _data list returned from the json file."""
        return self._data.__len__()

    def __iter__(self) -> Iterator:
        """Return the list of packages contained within the index."""
        return iter(self._data)

    def find(self, value: str) -> Union[list, None]:
        """Find packages matching a specified value."""
        return [s for s in self._data if value.lower() in s.lower()]

    def update(self) -> bool:
        """Using the requests module, download the latest index."""
        self._updated = False
        headers = {'If-None-Match': self._digest}
        req = requests.get(self._index, headers=headers, allow_redirects=True)
        if req.status_code not in [200, 304]:
            raise FileNotFoundError(req.status_code)
        elif req.status_code == 200:
            with open(self._cached_index, 'wb') as cached_index:
                cached_index.write(req.content)
            self._updated = True

    @property
    def outdated(self) -> bool:
        """Execute a head request using the requests library to check that the
        ETag matches.
        """
        headers = {'If-None-Match': self._digest}
        req = requests.head(self._index, headers=headers, allow_redirects=True)
        if req.status_code not in [200, 304]:
            raise FileNotFoundError(req.status_code)
        elif req.status_code == 200:
            return True
        elif req.status_code == 304:
            return False

    @property
    def _digest(self) -> str:
        """Return the md5 digest of the currently cached index file."""
        digest = md5()  # noqa: S303
        with open(self._cached_index, "rb") as cached_index:
            for block in iter(lambda: cached_index.read(65536), b""):
                digest.update(block)
        return digest.hexdigest()

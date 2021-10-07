import abc
import atexit
import json
import shutil
import tempfile
from hashlib import md5
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse
import requests
from ._formats import DirectoryPackageFormat, PackageFormat, ZipPackageFormat


Formats = Optional[List[PackageFormat]]


class PackageHandler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __getattr__(self, name) -> object:
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def installed(self) -> bool:
        ...

    @staticmethod
    @abc.abstractmethod
    def grasps(path: any) -> bool:
        """Return a boolean value describing weither the package source can be
        processed.
        """
        ...

    @abc.abstractmethod
    def install(self, path: str, version: str = None) -> bool:
        """Install a specific package version."""
        ...

    @abc.abstractmethod
    def uninstall(self) -> bool:
        """Uninstall a package."""
        ...

    @abc.abstractmethod
    def verify(self, signature: str) -> bool:
        """Verify a packages hash with the provided signature."""
        ...


class LocalPackageHandler(PackageHandler):
    """Directory package structure."""
    def __init__(self, name: str, src: str, formats: Optional[Formats] = None):
        """initialise the package."""
        self._meta = {}
        self._meta['name'] = name
        self._path = None
        self._installed = False
        self._src = str(src)[7:] if str(src)[:7] == 'file://' else src
        if formats is None:
            formats = [DirectoryPackageFormat]
        for current_format in formats:
            if current_format.grasps(self._src):
                self._format = current_format
                break
        else:
            message = 'unable to process source format'
            raise FileNotFoundError(message)

    @property
    def name(self) -> str:
        """Return the name of the package from the meta data."""
        return self.meta['name']

    @property
    def path(self) -> str:
        """Return the path the package is installed into."""
        return self._path

    def __getattr__(self, name):
        """Return an attribute from the meta data if the data doesnt exist."""
        if name not in self._meta:
            message = f'{name} is an invalid attribute'
            raise AttributeError(message)
        return self._meta[name]

    @property
    def installed(self) -> bool:
        """Return the current installation state."""
        return self._installed

    @staticmethod
    def grasps(path: any) -> bool:
        """Check if a directory on the local filesystem has been provided."""
        path = str(path)[7:] if str(path)[:7] == 'file://' else path
        return Path(str(path)).exists()

    def install(self, path: str = None, version: str = None) -> bool:
        """The local package handler does not install the package. No version
        control exists for the directory package type.
        """
        path = str(path)[7:] if str(path)[:7] == 'file://' else path
        self._path = path if path else self._src
        self._format.extract(self._src, self._path)
        self._meta = {**self._meta, **self._load_metadata(self._path)}
        self._installed = True
        return True

    def uninstall(self) -> bool:
        """Uninstall the package."""
        if self._path != self._src:
            self._remove_files(self._path)
        self._path = None
        self._installed = False
        return True

    def verify(self, digest: str = None) -> bool:
        """Verify the package hasn't been tampered with."""
        if digest is None:
            return True
        message = 'the local package handler does not support verification'
        raise ValueError(message)

    def _load_metadata(self, path: Path):
        """Load the package.json file into memory."""
        path = Path(str(path)[7:] if str(path)[:7] == 'file://' else path)
        try:
            with open(path / 'package.json') as package:
                meta = json.load(package)
                if 'name' not in meta:
                    message = 'meta file missing name value'
                    raise ValueError(message)
                if self._meta['name'] != meta['name']:
                    message = 'meta name does not match provided package name'
                    raise ValueError(message)
                if 'version' not in meta:
                    message = 'meta file missing version value'
                    raise ValueError(message)
                return meta
        except JSONDecodeError:
            message = 'invalud package file format'
            raise ValueError(message)

    @staticmethod
    def _remove_files(path: Path) -> None:
        """Recursively remove the path and all its sub items."""
        path = str(path)[7:] if str(path)[:7] == 'file://' else path
        try:
            shutil.rmtree(path)
        except OSError:
            FileNotFoundError('unable to remove files')


class HttpPackageHandler(PackageHandler):
    """Url package structure."""
    def __init__(
        self,
        name: str,
        src: str,
        formats: Formats = None,
        cache_dir: str = None
    ):
        """initialise the package."""
        self._meta = {}
        self._meta['name'] = name
        self._path = None
        self._installed = False
        self._src = src
        if not cache_dir:
            tmp_cache = tempfile.TemporaryDirectory()
            cache_dir = Path(tmp_cache.name)
            atexit.register(tmp_cache.cleanup)
        else:
            cache_dir.mkdir(0x777, True, True)
        parts = urlparse(src)
        ext = ''.join(Path(parts.path).suffixes)
        self._cache = Path(cache_dir / Path(name + ext))
        if not HttpPackageHandler.grasps(src):
            message = 'invalid handler format'
            raise ValueError(message)
        if formats is None:
            formats = [ZipPackageFormat]
        for current_format in formats:
            if current_format.grasps(self._src):
                self._format = current_format
                break
        else:
            message = 'a valid source is required'
            raise FileNotFoundError(message)

    @property
    def name(self) -> str:
        """Return the name of the package from the meta data."""
        return self.meta['name']

    def __getattr__(self, name):
        """Return an attribute from the meta data if the data doesnt exist."""
        if name not in self._meta:
            message = f'{name} is an invalid attribute'
            raise AttributeError(message)
        return self._meta[name]

    @property
    def installed(self) -> bool:
        """Return the current installation state."""
        return self._installed

    @staticmethod
    def grasps(path: any) -> bool:
        """Check if a directory on the local filesystem has been provided."""
        parts = urlparse(str(path))
        if parts.scheme not in ['http', 'https']:
            return False
        return True

    def install(self, path: str, version: str = None) -> bool:
        """The local package handler does not install the package. No version
        control exists for the directory package type.
        """
        self._path = path
        self._updated = False
        headers = {'If-None-Match': self._digest}
        req = requests.get(self._src, headers=headers, allow_redirects=True)
        if req.status_code not in [200, 304]:
            raise FileNotFoundError(req.status_code)
        elif req.status_code == 200:
            self._cache.parents[0].mkdir(parents=True, exist_ok=True)
            with open(self._cache, 'wb') as cached_package:
                cached_package.write(req.content)
            self._updated = True
        self._format.extract(self._cache, self._path)
        self._meta = {**self._meta, **self._load_metadata(self._path)}
        self._installed = True
        return True

    def uninstall(self) -> bool:
        """Uninstall the package."""
        if self._path != self._src:
            self._remove_files(self._path)
        self._path = None
        self._installed = False
        return True

    def verify(self, digest: str = None) -> bool:
        """Verify the package hasn't been tampered with."""
        if digest is None:
            return True
        message = 'the http package handler does not support verification'
        raise ValueError(message)

    def _load_metadata(self, path: Path):
        """Load the package.json file into memory."""
        try:
            with open(path / 'package.json') as package:
                meta = json.load(package)
                if 'name' not in meta:
                    message = 'meta file missing name value'
                    raise ValueError(message)
                if self._meta['name'] != meta['name']:
                    message = 'meta name does not match provided package name'
                    raise ValueError(message)
                if 'version' not in meta:
                    message = 'meta file missing version value'
                    raise ValueError(message)
                return meta
        except JSONDecodeError:
            message = 'invalud package file format'
            raise ValueError(message)

    @staticmethod
    def _remove_files(path: Path) -> None:
        """Recursively remove the path and all its sub items."""
        try:
            shutil.rmtree(path)
        except OSError:
            FileNotFoundError('unable to remove files')

    @property
    def outdated(self) -> bool:
        """Execute a head request using the requests library to check that the
        ETag matches.
        """
        headers = {'If-None-Match': self._digest}
        req = requests.head(self._src, headers=headers, allow_redirects=True)
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
        if not self._cache.exists():
            return digest.hexdigest()
        with open(self._cache, "rb") as cached_package:
            for block in iter(lambda: cached_package.read(65536), b""):
                digest.update(block)
        return digest.hexdigest()

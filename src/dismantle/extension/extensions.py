"""Extensions locator."""
import importlib.util
import os
import sys
from contextlib import suppress
from pathlib import Path
from . import IExtension


class Extensions:
    """Search through the installed packages and find extensions."""
    def __init__(self, types, packages, prefix) -> None:
        """Search through all provided extensions and register them."""
        self._packages = packages
        self._extensions = {}
        self._directory = 'extensions'
        self._prefix = prefix
        self._imports = {}
        self._exclude = (['__pycache__', '.git'])
        self._include = ('.py', '.cpython-37.pyc')
        # check that the types are a subclass of IExtension
        if not all([issubclass(i, IExtension) for i in types]):
            raise ValueError('all exntesion types must extend IExtension')
        self._types = types
        for category in self._types:
            self._extensions[category._category] = {}
        self._find()
        self._register()

    def _find(self) -> None:
        """Search through the packages and find all extensions. """
        for package in self._packages.values():
            # set the package prefix
            _prefix = package.name
            # check if the package has an init file
            with suppress(KeyError):
                root, paths, _ = next(os.walk(package._path))
            # check if we have an extensions directory
            if self._directory in paths:
                ext_files = os.path.join(root, self._directory)
                for root, dirs, files in os.walk(ext_files, topdown=True):
                    dirs[:] = [d for d in dirs if d not in self._exclude]
                    files[:] = [f for f in files if f.endswith(self._include)]
                    for name in files:
                        path = Path(root, name)
                        if len(path.suffixes) >= 2:
                            n_length = len(path.stem) - len(path.suffixes[0])
                            ext_name = path.stem[:n_length]
                        else:
                            ext_name = path.stem
                        prefix = _prefix + '.extension.' + ext_name
                        self._imports[prefix] = self._load(path, prefix)
                        self._imports[prefix].prefix = prefix

    def _load(self, path: Path, prefix: str):
        """Python 3.5 and up. (I hate you package system)."""
        spec = importlib.util.spec_from_file_location(prefix, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[prefix] = module
        try:
            spec.loader.exec_module(module)
        except Exception as e:  # NOQA: E722
            raise ModuleNotFoundError(f'error in {prefix} ({e})')
        return module

    def _register(self) -> None:
        """Register extensions."""
        for i in self._imports.values():
            for cls, cls_name in ((getattr(i, name), name) for name in dir(i)):
                if isinstance(cls, type):
                    for subclass in self._types:
                        if issubclass(cls, subclass) and cls is not subclass:
                            name = '.'.join([i.prefix, cls_name])
                            self._extensions[subclass._category][name] = cls

    def category(self, category) -> list:
        return self._extensions[category]

    @property
    def types(self) -> list:
        return list(self._extensions.keys())

    @property
    def extensions(self) -> dict:
        return self._extensions

    @property
    def imports(self) -> dict:
        return self._imports

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
"""Extensions locator."""

import importlib.util
import logging
import os
from logging import NullHandler
from . import IExtension


log = logging.getLogger(__name__).addHandler(NullHandler())


class Extensions:
    """Search through the installed packages and find extensions."""
    def __init__(self, types, packages, prefix):
        """ """
        self._packages = packages
        self._extensions = {}
        self._directory = 'extensions'
        self._prefix = prefix
        self._imports = {}
        self._exclude = (['__pycache__'])

        # check that the types are a subclass of IExtension
        if not all([issubclass(i, IExtension) for i in types]):
            raise ValueError('all exntesion types must extend IExtension')
        self._types = types
        for category in self._types:
            self._extensions[category._category] = {}
        self._find()
        self._register()

    def _find(self):
        """Search through the packages and find all extensions. """
        for x in self._packages.values():
            # set the package prefix
            _prefix = x.name
            # check if the package has an init file
            try:
                root, paths, filenames = next(os.walk(x.path))
            except KeyError:
                continue
            # check if we have an extensions directory
            if self._directory in paths:
                ext_files = os.path.join(root, self._directory)
                for root, dirs, files in os.walk(ext_files, topdown=True):
                    dirs[:] = [d for d in dirs if d not in self._exclude]

                    for name in files:
                        # get the path from the beginning of the module
                        fd = os.path.splitext(name)[0]
                        full_path = os.path.join(root, fd)
                        v = full_path[len(ext_files):].replace(os.sep, '.')
                        prefix = _prefix + '.extension' + v
                        self._imports[prefix] = self._load(full_path, prefix)
                        self._imports[prefix].prefix = prefix

    def _load(self, path, prefix):
        """ Python 3.5 and up. (I hate you package system). """
        if os.path.isdir(path):
            path = path + '/__init__.py'
        else:
            path = path + '.py'

        spec = importlib.util.spec_from_file_location(prefix, path)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:  # NOQA: E722
            log.error('error in {} ({})'.format(prefix, e))
        return module

    def _register(self):
        """Register extensions."""
        for i in self._imports.values():
            for cls, cls_name in ((getattr(i, name), name) for name in dir(i)):
                if isinstance(cls, type):
                    for subclass in self._types:
                        if issubclass(cls, subclass) and cls is not subclass:
                            name = '.'.join([i.prefix, cls_name])
                            self._extensions[subclass._category][name] = cls

    def category(self, category):
        return self._extensions[category]

    @property
    def types(self) -> list:
        return list(self._extensions.keys())

    @property
    def extensions(self):
        return self._extensions

    @property
    def imports(self):
        return self._imports

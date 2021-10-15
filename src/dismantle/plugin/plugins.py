"""Plugins locator."""

import logging
import os


try:
    from importlib.abc import Loader as imp
except ImportError:
    import imp  # NOQA: F401

from . import IPlugin, _plugins


# enable logging
log = logging.getLogger(__name__)


class Plugins:
    """Search through the installed packages and find plugins."""

    def __init__(self, types, packages, prefix):
        """ """
        self._packages = packages
        self._plugins = _plugins
        self._directory = 'plugins'
        self._prefix = prefix
        self._imports = {}
        self._exclude = set(['__pycache__'])

        # check that the types are a subclass of IPlugin
        if all([issubclass(i, IPlugin) for i in types]):
            self._types = types
        else:
            raise ValueError('all plugin types must extend IPlugin')
        self._find()

    def _find(self):
        """search through the packages and find all plugins."""
        for x in self._packages.enabled.values():
            _prefix = x['name']
            # check if the package has an init file
            try:
                root, paths, filenames = next(os.walk(x['directory']))
            except KeyError:
                continue
            # check if we have an extensions directory
            if self._directory in paths:
                plg_files = os.path.join(root, self._directory)
                for root, dirs, files in os.walk(plg_files, topdown=True):
                    dirs[:] = [d for d in dirs if d not in self._exclude]

                    for name in files:
                        # get the path from the beginning of the module
                        fd = os.path.splitext(name)[0]
                        full_path = os.path.join(root, fd)
                        v = full_path[len(plg_files):].replace(os.sep, '.')
                        prefix = _prefix + '.plugin' + v
                        self._imports[prefix] = self._import(full_path, prefix)

    def _import(self, path, prefix):
        """ Import a file or module into our imports list. """

        # use imp to correctly load the plugin as a module
        if os.path.isdir(path):
            spec = ("py", "r", imp.PKG_DIRECTORY)
            module = imp.load_module(prefix, None, path, spec)
        else:
            with open(path + ".py", "r") as plugin_file:
                spec = ("py", "r", imp.PY_SOURCE)
                module = imp.load_module(
                    prefix,
                    plugin_file,
                    path + ".py",
                    spec
                )
        return module

    @property
    def plugins(self):
        return self._plugins

    @property
    def imports(self):
        return self._imports

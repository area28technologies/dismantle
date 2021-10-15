"""Dismantle package manager system with support for extensions and plugins."""

# IDEAS: --- plugins ----------------------------
# IDEAS: Function hook to provide plugin (process content before / after)
# IDEAS: List plugins for a function

_plugins = {}

from .iplugin import IPlugin
from .plugin import plugin
from .plugins import Plugins
from .register import register


__all__ = [
    'IPlugin',
    'register',
    'plugin',
    'Plugins',
    '_plugins'
]

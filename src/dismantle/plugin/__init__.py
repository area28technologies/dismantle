"""Plugin management."""
from .iplugin import IPlugin
from .plugin import plugin
from .plugins import Plugins
from .register import register

_plugins = {}

__all__ = [
    'IPlugin',
    'register',
    'plugin',
    'Plugins',
    '_plugins'
]

# IDEAS: --- plugins ----------------------------
# IDEAS: Func hook to provide plugin (process content before / after)
# IDEAS: List plugins for a function

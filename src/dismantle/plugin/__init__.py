"""Plugin management."""
_plugins = {}

from dismantle.plugin.iplugin import IPlugin  # noqa: E402
from dismantle.plugin.plugin import plugin  # noqa: E402
from dismantle.plugin.plugins import Plugins  # noqa: E402
from dismantle.plugin.register import register  # noqa: E402

__all__ = [
    '_plugins',
    'IPlugin',
    'register',
    'plugin',
    'Plugins'
]

# IDEAS: --- plugins ----------------------------
# IDEAS: Func hook to provide plugin (process content before / after)
# IDEAS: List plugins for a function

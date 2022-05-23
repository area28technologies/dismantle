"""Provide the ability to decorate functions with a plugin decorator."""
import logging

from dismantle.plugin import _plugins

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class plugin:  # noqa: N801
    """Plugin decorator to register plugins."""

    def __init__(self, name, priority=100):
        """Get the name of the registered method.

        To add the plugin to and set the evecution priority. Priority
        less than zero executes before the main method, priority above
        zero executes afterwards.
        """
        log.debug(f'plugin.__init__: ({priority}) {name}')

        # ensure the priority is numeric
        if not isinstance(priority, int):
            raise ValueError('Priority needs to be numeric')
        self._priority = priority

        # check the name is printable
        if not name.isprintable():
            raise ValueError('Name needs to be printable')

        # check the plugin registration exists
        self._name = name
        if name not in _plugins:
            log.warning(f'function "{name}" not registered')
            _plugins[name] = {'original': None}
            _plugins[name]['plugins'] = []

    def __call__(self, extend_function):
        """Call wrapper to be executed when a function is wrapped."""
        log.debug(f'plugin.__call__: {extend_function}')
        self._function = extend_function
        global _plugins
        _plugins[self._name]['plugins'].append({
            'function': self._function,
            'priority': self._priority
        })

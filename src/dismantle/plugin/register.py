import functools
import logging
from logging import NullHandler
from . import _plugins


log = logging.getLogger(__name__).addHandler(NullHandler())


def register(name=None):
    """Register a function to add plugins to."""
    log.debug('register: {}'.format(name))
    if not name:
        raise ValueError

    def decorator(_func=None):
        log.debug('register.decorator: {}'.format(_func))
        _plugins[name] = {'original': _func}
        _plugins[name]['plugins'] = []

        @functools.wraps(_func)
        def caller(self, *args, **kwargs):
            """ Execute the registered plugin in order of priority. """

            # store the previous result
            _plugins[name]['result'] = args[0]

            # get the list of before and after plugins
            before = [p for p in _plugins[name]['plugins'] if p['priority'] < 0]  # NOQA: E501
            after = [p for p in _plugins[name]['plugins'] if p['priority'] >= 0]  # NOQA: E501

            # execute all the before plugins
            for _name in before:
                _args = (self, _plugins[name]['result'])
                _plugins[name]['result'] = _name['function'](*_args)

            # execute the actual method that was registered
            _args = (self, _plugins[name]['result'])
            _plugins[name]['result'] = _plugins[name]['original'](*_args)

            # execute all the after plugins
            for _name in after:
                _args = (self, _plugins[name]['result'])
                _plugins[name]['result'] = _name['function'](*_args)

            return _plugins[name]['result']
        return caller
    return decorator

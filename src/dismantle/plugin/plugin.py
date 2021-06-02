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
import logging
from logging import NullHandler
from . import _plugins


log = logging.getLogger(__name__).addHandler(NullHandler())


class plugin:  # noqa: N801
    """Plugin decorator to register plugins."""

    def __init__(self, name, priority=100):
        """Get the name of the registered method to add the plugin to and set
        the evecution priority. Priority less than zero executes before the
        main method, priority above zero executes afterwards.
        """
        log.debug('plugin.__init__: ({}) {}'.format(priority, name))

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
            log.warning('function "{}" not registered'.format(name))
            _plugins[name] = {'original': None}
            _plugins[name]['plugins'] = []

    def __call__(self, extend_function):
        """"""
        log.debug('plugin.__call__: {}'.format(extend_function))
        self._function = extend_function
        global _plugins
        _plugins[self._name]['plugins'].append({
            'function': self._function,
            'priority': self._priority
        })

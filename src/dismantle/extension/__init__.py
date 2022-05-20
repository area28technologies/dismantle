"""Provide the ability to extend a module.

Extensions provide the abiity to add additional functionality to a
defined module by providing an interface that can be extended by
multiple classes each with a new provider.
"""

# TODO: activate, deactivate, active

__all__ = [
    'IExtension',
    'Extensions'
]

from dismantle.extension.extensions import Extensions
from dismantle.extension.iextension import IExtension

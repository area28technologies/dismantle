"""Dismantle package manager system with support for extensions and plugins."""

# IDEAS: --- extension --------------------------
# IDEAS: Class Hook to provide extensions (add new abilities such as log types)
# IDEAS: activate, deactivate, active

__all__ = [
    'IExtension',
    'Extensions'
]

from .iextension import IExtension
from .extensions import Extensions  # noqa: I001 (needs to be after iextension)

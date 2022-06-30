"""Provides an extension to be used for testing."""
from dismantle.extension import IExtension


class ColorExtension(IExtension):
    """An example extension defining a set of colors."""

    _category = 'color'

    def color(self) -> None:
        """Set a color for the test extension."""
        ...

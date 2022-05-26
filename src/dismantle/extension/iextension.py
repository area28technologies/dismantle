"""Creates an interface to allow all other extensions to extend."""


class IExtension:
    """Extension interface to recognise what needs to be processed."""

    _name: str = 'default'
    _category: str = 'default'

    def __init__(self) -> None:
        """Initialise with default activity set to false."""
        self._active: bool = False

    def activate(self) -> bool:
        """Activate an extension."""
        self._active = True
        return self._active

    def deactivate(self) -> bool:
        """Deactivate an extension."""
        self._active = False
        return not self._active

    @property
    def name(self) -> str:
        """Return the extensions name."""
        return self._name

    @property
    def category(self) -> str:
        """Return the extensions category."""
        return self._category

    @property
    def active(self) -> bool:
        """Return the extensions active state."""
        return self._active

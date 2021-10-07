class IExtension:
    """Extension interface to recognise what needs to be processed."""

    _name: str = "default"
    _category: str = "default"

    def __init__(self) -> None:
        self._active: bool = False

    def activeate(self) -> bool:
        self._active = True
        return self._active

    def deactivate(self) -> bool:
        self._active = False
        return not self._active

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> str:
        return self._category

    @property
    def active(self) -> bool:
        return self._active

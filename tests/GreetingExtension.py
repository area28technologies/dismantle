"""Simple extension to provide greetings."""
from dismantle.extension import IExtension


class GreetingExtension(IExtension):
    """A test extension to provide greetings."""

    _category = 'greeting'

    def greet(self, person: str) -> None:
        """Test method to greet a person."""
        ...

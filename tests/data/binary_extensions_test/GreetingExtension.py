from dismantle.extension import IExtension


class GreetingExtension(IExtension):
    _category = 'greeting'

    def greet(self, person: str) -> None:
        ...

from tests.GreetingExtension import GreetingExtension


class HelloColorExtension(GreetingExtension):
    _name = 'hello'

    def greet(self, person: str) -> None:
        print(f'{self._name} {person}')

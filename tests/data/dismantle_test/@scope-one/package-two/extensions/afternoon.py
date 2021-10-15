from tests.GreetingExtension import GreetingExtension


class AfternoonColorExtension(GreetingExtension):
    _name = 'afternoon'

    def greet(self, person: str) -> None:
        print(f'{self._name} {person}')

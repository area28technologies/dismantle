from tests.GreetingExtension import GreetingExtension


class GoodbyeColorExtension(GreetingExtension):
    _name = 'goodbye'

    def greet(self, person: str) -> None:
        print(f'{self._name} {person}')

from tests.WrongExtension import WrongExtension


class WrongBrokenExtension(WrongExtension):
    _name = 'broken'

    def wrong(self, person: str) -> None:
        print(f'{self._name} {person}')

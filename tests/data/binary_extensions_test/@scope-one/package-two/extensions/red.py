from tests.ColorExtension import ColorExtension


class RedColorExtension(ColorExtension):
    _name = 'red'

    def color(self) -> None:
        print(f'color is {self._name}')

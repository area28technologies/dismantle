from tests.ColorExtension import ColorExtension


class BlueColorExtension(ColorExtension):
    _name = 'blue'

    def color(self) -> None:
        print(f'color is {self._name}')

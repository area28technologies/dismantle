from tests.ColorExtension import ColorExtension


class GreenColorExtension(ColorExtension):
    _name = 'green'

    def color(self) -> None:
        print(f'color is {self._name}')

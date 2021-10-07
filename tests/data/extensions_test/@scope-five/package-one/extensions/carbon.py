from tests.ColorExtension import ColorExtension


class CarbonColorExtension(ColorExtension):
    _name = 'carbon'

    def color(self) -> None:
        print(f'color is {self._name}')

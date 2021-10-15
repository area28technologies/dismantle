from dismantle.extension import IExtension


class ColorExtension(IExtension):
    _category = 'color'

    def color(self) -> None:
        ...

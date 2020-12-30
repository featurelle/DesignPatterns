from __future__ import annotations

from colorama import Fore, init


class Shape:

    def draw(self) -> None:
        raise NotImplementedError

    def color(self, color: str) -> None:
        self._color = color

    def clone(self):
        raise NotImplementedError


class Dot(Shape):

    def __init__(self, color: str):
        self._color = color

    def draw(self):
        print(self._color + '.' + Fore.RESET, end='')

    def clone(self):
        return Dot(self._color)


class Brush(Shape):

    def __init__(self, color: str, radius: int, transparent: bool = False):
        self._color = color
        self._radius = radius
        self._transparent = transparent

    def draw(self):
        print(self._color + '\n /```\\ \n'
                           '| ooo |\n'
                           ' \\.../ ' + Fore.RESET, end='')

    def clone(self):
        params = self._color, self._radius, self._transparent
        return Brush(*params)


class Stencil(Shape):

    def __init__(self, shapes: list[Shape]):
        self.shapes = shapes

    def color(self, color: str):
        for shape in self.shapes:
            shape.color(color)

    def draw(self):
        for shape in self.shapes:
            shape.draw()

    def clone(self):
        shapes = []
        for shape in self.shapes:
            shapes.append(shape.clone())
        return Stencil(shapes)


class ShapesRegister:

    def __init__(self):
        self.__items = dict()

    def load(self):
        self.__items['simple_dot'] = Dot(Fore.BLACK)
        self.__items['small_brush'] = Brush(Fore.BLACK, 10)
        self.__items['big_brush'] = Brush(Fore.BLACK, 30)
        self.__items['composite_shape'] = Stencil(list(self.__items.values()))

    def save(self, shape: Shape, name: str):
        self.__items[name] = shape.clone()

    def search_shape(self, name: str):
        if name in self.__items.keys():
            return self.__items[name].clone()
        else:
            return None


def demo():

    init()

    saved = ShapesRegister()
    saved.load()

    brush = saved.search_shape('small_brush')
    brush.draw()
    print()
    brush.color(Fore.GREEN)
    brush.draw()
    print()
    saved.save(brush, 'my_brush')

    com = saved.search_shape('composite_shape')
    com.draw()
    print()
    com.shapes[2] = brush
    dot = saved.search_shape('simple_dot')
    com.shapes.append(dot)
    com.draw()
    print()

    saved.save(com, 'my_composite')
    com.color(Fore.BLUE)
    com.draw()
    saved.save(com, 'blue_composite')


if __name__ == '__main__':
    demo()

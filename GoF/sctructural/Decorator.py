from __future__ import annotations
from abc import ABC, abstractmethod


# Абстрактный класс Tag - общий для всех
class Tag(ABC):

    @abstractmethod
    def string(self):
        pass


# Конкретные тэги
class Plain(Tag):

    def string(self):
        return '<p></p>'


class Div(Tag):

    def string(self):
        return '<div></div>'


class Span(Tag):

    def string(self):
        return '<span></span>'


# Абстрактный класс Attribute декорирует тэги, оборачивая их в себя
class Attribute(Tag):

    def __init__(self, tag: Tag, atr: str):
        self.__tag = tag
        self.__atr = atr

    @property
    def tag(self):
        return self.__tag

    @property
    def atr(self):
        return self.__atr

    @abstractmethod
    def string(self):
        pass


# Конкретные тэги и их конкретное поведение
class Role(Attribute):

    def string(self):
        split_string = self.tag.string().split('>', 1)
        split_string[0] += f' role="{self.atr}">'
        return ''.join(split_string)


class Class(Attribute):

    def string(self):
        split_string = self.tag.string().split('>', 1)
        split_string[0] += f' class="{self.atr}">'
        return ''.join(split_string)


class Id(Attribute):

    def string(self):
        split_string = self.tag.string().split('>', 1)
        split_string[0] += f' id="{self.atr}">'
        return ''.join(split_string)


def tag_constructor():
    plain = Plain()
    print('1. Pure plain: ' + plain.string())
    plain = Class(plain, 'regular')
    plain = Id(plain, '1000123')
    plain = Role(plain, 'readme')
    print('2. Decorated plain: ' + plain.string())
    div = Div()
    div = Role(div, 'letterbox')
    div = Class(div, 'main black')
    div = Id(div, '900192')
    print('3. Decorated div: ' + div.string())
    span = Span()
    span = Class(span, 'white')
    print('4. Decorated span: ' + span.string())


if __name__ == "__main__":
    tag_constructor()

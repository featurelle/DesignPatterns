from __future__ import annotations
from functools import singledispatchmethod
from abc import ABC, abstractmethod


class Offer:

    def __init__(self, name):
        self.name = name


class SmallStore(Offer):
    pass


class LargeStore(Offer):
    pass


class Mall(Offer):
    pass


class GasStation(Offer):
    pass


class Card(ABC):

    @singledispatchmethod
    @abstractmethod
    def cashback(self, offer) -> str:
        pass

    @cashback.register
    @abstractmethod
    def _(self, offer: GasStation):
        pass

    @cashback.register
    @abstractmethod
    def _(self, offer: Mall):
        pass

    @cashback.register
    @abstractmethod
    def _(self, offer: LargeStore):
        pass

    @cashback.register
    @abstractmethod
    def _(self, offer: SmallStore):
        pass


class GoldenCard(Card):

    @singledispatchmethod
    def cashback(self, offer) -> str:
        pass

    @cashback.register
    def _(self, offer: GasStation):
        pass

    ...


# В общем, идея ясна, и почему это ужасно выглядит, тоже ясно... Куча декораторов, куча методов, копипаст руками,
# Классы разбухают, подсказки как надо не работают, легко забыть про какой-то метод,
# А глаза от этого зрелища начинают разбегаться выкатываться на лоб.
# Хотя математически это не приведет к большему количеству работы, это приведет Психологически!

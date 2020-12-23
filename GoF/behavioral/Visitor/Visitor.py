# К сожалению, в Пайтоне перегруженные методы реализуются как-то совсем дико и неудобно.
# И трудно заставить классы-наследники наследовать все Перегруженные методы.
# Поэтому смысл Посетителя в Пайтоне немного теряется/видоизменяется.
# Как, впрочем, теряется и смысл других паттернов, вроде Итератора, которого легко заменяют генераторы и функция iter()

from __future__ import annotations
from abc import ABC, abstractmethod

from colorama import Fore, init


class Visitor(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def cashback_golden(self, card: GoldenCard) -> None:
        pass

    @abstractmethod
    def cashback_silver(self, card: SilverCard) -> None:
        pass

    @abstractmethod
    def cashback_regular(self, card: RegularCard) -> None:
        pass


class SmallStore(Visitor):

    def cashback_golden(self, card: GoldenCard) -> None:
        print(f'{card.name} card gives you %3 cashback in a small store')

    def cashback_silver(self, card: SilverCard) -> None:
        print(f'{card.name} card gives you %2 cashback in a small store')

    def cashback_regular(self, card: RegularCard) -> None:
        print(f'{card.name} card gives you %1 cashback in a small store')


class Card(ABC):

    @abstractmethod
    @property
    def name(self):
        pass

    @abstractmethod
    def accept(self, v: Visitor) -> None:
        pass


class GoldenCard(Card):

    @property
    def name(self):
        return Fore.YELLOW + 'golden'

    def accept(self, v: Visitor) -> None:
        # Смысл давать визитору свой тип здесь умозрительный, потому что метод и так определен строго для этого типа.
        # Тут это лежит просто для красоты:
        # "А вот в языках с удобными перегрузками визитор бы сам определял, какой метод вызвать, опираясь на тип..."
        v.cashback_golden(self)


class SilverCard(Card):

    @property
    def name(self):
        return Fore.WHITE + 'silver'

    def accept(self, v: Visitor) -> None:
        v.cashback_silver(self)


class RegularCard(Card):

    @property
    def name(self):
        return Fore.GREEN + 'regular'

    def accept(self, v: Visitor) -> None:
        v.cashback_regular(self)

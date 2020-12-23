# К сожалению, в Пайтоне перегруженные методы реализуются как-то совсем дико и неудобно.
# И трудно заставить классы-наследники наследовать все Перегруженные методы.
# Поэтому смысл Посетителя в Пайтоне немного теряется/видоизменяется.
# Как, впрочем, теряется и смысл других паттернов, вроде Итератора, которого легко заменяют генераторы и функция iter()

from __future__ import annotations
from abc import ABC, abstractmethod

from colorama import Fore, init


class Visitor(ABC):

    @abstractmethod
    def __init__(self, name, g_cb, s_cb, r_cb) -> None:
        pass

    # Тут еще должны быть сеттеры для назначения новых кэшбеков и тп
    @property
    def name(self):
        return self._name

    # Эти методы лучше бы были абстрактными, а поведение наследников - разное, но тут проще было так сделать
    def cashback_golden(self, card: GoldenCard) -> None:
        print(f'{card.name} card gives you %{self.g_cb} cashback in a {self.name}')

    def cashback_silver(self, card: SilverCard) -> None:
        print(f'{card.name} card gives you %{self.s_cb} cashback in a {self.name}')

    def cashback_regular(self, card: RegularCard) -> None:
        print(f'{card.name} card gives you %{self.r_cb} cashback in a {self.name}')


class SmallStore(Visitor):


class LargeStore(Visitor):



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

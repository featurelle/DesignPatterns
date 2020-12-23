# К сожалению, в Пайтоне перегруженные методы реализуются как-то совсем дико и неудобно.
# И трудно заставить классы-наследники наследовать все Перегруженные методы.

from __future__ import annotations
from abc import ABC, abstractmethod

from colorama import Fore, init


class Visitor:

    def __init__(self, name, g_cb, s_cb, r_cb) -> None:
        self._name = name
        self._g_cb = g_cb
        self._s_cb = s_cb
        self._r_cb = r_cb

    # Тут еще должны быть сеттеры для назначения новых кэшбеков и тп
    @property
    def name(self):
        return self._name

    @property
    def g_cb(self):
        return self._g_cb

    @property
    def s_cb(self):
        return self._s_cb

    @property
    def r_cb(self):
        return self._r_cb

    # Эти методы лучше бы были абстрактными, а поведение наследников - разное, но... Разное поведение еще написать надо)
    def cashback_golden(self, card: GoldenCard) -> None:
        print(f'{card.name} card gives you %{self.g_cb} cashback in a {self.name}')

    def cashback_silver(self, card: SilverCard) -> None:
        print(f'{card.name} card gives you %{self.s_cb} cashback in a {self.name}')

    def cashback_regular(self, card: RegularCard) -> None:
        print(f'{card.name} card gives you %{self.r_cb} cashback in a {self.name}')


class SmallStore(Visitor):

    def __init__(self):
        super().__init__('Small store', 3, 2, 1)


class LargeStore(Visitor):

    def __init__(self):
        super().__init__('Large store', 4, 3, 2)


class Mall(Visitor):

    def __init__(self):
        super().__init__('Big mall', 5, 4, 3)


class Card(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def accept(self, v: Visitor) -> None:
        pass


class GoldenCard(Card):

    @property
    def name(self):
        return Fore.YELLOW + 'Golden' + Fore.RESET

    def accept(self, v: Visitor) -> None:
        # Смысл давать визитору свой тип здесь умозрительный, потому что метод и так определен строго для этого типа.
        # Тут это лежит просто для красоты:
        # "А вот в языках с удобными перегрузками визитор бы сам определял, какой метод вызвать, опираясь на тип..."
        v.cashback_golden(self)


class SilverCard(Card):

    @property
    def name(self):
        return Fore.WHITE + 'Silver' + Fore.RESET

    def accept(self, v: Visitor) -> None:
        v.cashback_silver(self)


class RegularCard(Card):

    @property
    def name(self):
        return Fore.CYAN + 'Regular' + Fore.RESET

    def accept(self, v: Visitor) -> None:
        v.cashback_regular(self)


def demo():
    init()

    market = [SmallStore(),
              LargeStore(),
              Mall()]

    cards = [GoldenCard(),
             SilverCard(),
             RegularCard()]

    for store in market:
        for card in cards:
            card.accept(store)
        print('-' * 30)


if __name__ == "__main__":
    demo()

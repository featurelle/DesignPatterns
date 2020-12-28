from __future__ import annotations
from typing import List


class ATMInterface:

    def cash_out(self, amount: int) -> None:
        raise NotImplementedError

    def available(self) -> tuple:
        raise NotImplementedError


class ATM(ATMInterface):

    def __init__(self, modules: List[Module]):
        self.__modules = modules
        self.__first = modules[0]

    def cash_out(self, amount: int):
        print('\nBzzzzt!!! Cashing out...')
        self.__first.give_out(amount)

    def available(self):
        print('This message is printed when the real ATM is processing.')
        return tuple(i.banknote for i in self.__modules if i.remaining > 0)

    def total(self) -> int:
        total = 0
        for module in self.__modules:
            total += module.total()
        return total


class Module:

    def __init__(self, banknote: int, remaining: int = 0, next_: Module = None):
        self._banknote = banknote
        self._remaining = remaining
        self._next = next_

    def total(self):
        return self._banknote * self._remaining

    @property
    def remaining(self):
        return self._remaining

    @property
    def banknote(self):
        return self._banknote

    def give_out(self, amount):

        remainder = amount
        bills = 0

        while bills < self._remaining and remainder >= self._banknote:
            bills += 1
            remainder -= self._banknote

        if bills > 0:
            self._remaining -= bills
            print(f'{self._banknote} UAH: {bills} bills')

        # Обязанность передается дальше
        if self._next:
            self._next.give_out(remainder)

    def then(self, mod: Module):
        self._next = mod
        return self._next


def demo():

    modules = [Module(i, 20) for i in [500, 200, 100, 50, 20]]
    modules[0].then(modules[1]).then(modules[2]).then(modules[3]).then(modules[4])

    atm = ATM(modules)
    atm.cash_out(120)
    atm.cash_out(5000)
    atm.cash_out(3250)
    atm.cash_out(7400)
    atm.cash_out(5750)
    atm.cash_out(400)


if __name__ == "__main__":
    demo()

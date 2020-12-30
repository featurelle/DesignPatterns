from __future__ import annotations
from typing import List


class ATM:

    def __init__(self, modules: List[Module], software: Software):
        self.__modules = modules
        self.__software = software
        self.__handlers = software.create_handlers(self.__modules)
        self.__main_handler = self.__handlers[0]

    def cash_out(self, amount: int):
        if query := self.__main_handler.check_request(amount, []):
            print('\nBzzzzt!!! Cashing out...')
            for request in query:
                print(request.execute())
            print('\n')
        else:
            print("I can't give you this sum of money. Try again, please!")

    def available(self):
        return tuple(i.banknote for i in self.__modules if i.remaining > 0)


class ATMProxyGuard:

    def __init__(self, atm: ATM):
        self.__atm = atm

    # Помимо всего прочего...
    def cash_out(self, amount):
        minimum = min(self.__atm.available())
        if amount % minimum != 0:
            print(f'Sorry, wrong sum. Minimum available banknote is {minimum}.')
        else:
            self.__atm.cash_out(amount)


# Ну прям фабрика
class Software:

    def create_handlers(self, modules: List[Module]):

        handlers = []

        for module in modules:
            handlers.append(MoneyHandler(module))

        last = len(handlers) - 1

        for n in range(last):
            handlers[n].then(handlers[n + 1])

        handlers[last].then(RemainderGuard())

        return handlers


class Module:

    def __init__(self, banknote: int, remaining: int = 0):
        self._banknote = banknote
        self._remaining = remaining

    def total(self):
        return self._banknote * self._remaining

    @property
    def remaining(self):
        return self._remaining

    @property
    def banknote(self):
        return self._banknote

    def give_out(self, quantity):
        self._remaining -= quantity
        return f'{self._banknote} UAH: {quantity} bills'


class ModuleHandler:

    def check_request(self, request: int, query: list):
        raise NotImplementedError


class MoneyHandler(ModuleHandler):

    def __init__(self, module: Module, then: ModuleHandler = None):
        self._module = module
        self._then = then

    def check_request(self, request: int, query: list):

        remainder = request
        bills = 0

        while bills < self._module.remaining and remainder >= self._module.banknote:
            bills += 1
            remainder -= self._module.banknote

        if bills > 0:
            query.append(Cashing(self._module, bills))

        return self._then.check_request(remainder, query)

    def then(self, then: ModuleHandler):
        self._then = then
        return self._then


class RemainderGuard(ModuleHandler):

    def check_request(self, remainder: int, query: list):
        if not remainder:
            return query
        else:
            return None


class Cashing:

    def __init__(self, module: Module, quantity: int):
        self._module = module
        self._quantity = quantity

    def execute(self):
        return self._module.give_out(self._quantity)


def demo():

    modules = [Module(i, 20) for i in [500, 200, 100, 50]]
    software = Software()
    atm = ATM(modules, software)
    atm_proxy = ATMProxyGuard(atm)
    atm_proxy.cash_out(120)
    atm_proxy.cash_out(5000)
    atm_proxy.cash_out(3250)
    atm_proxy.cash_out(7400)
    atm_proxy.cash_out(5750)
    atm_proxy.cash_out(400)


if __name__ == "__main__":
    demo()

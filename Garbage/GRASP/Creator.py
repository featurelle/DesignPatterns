"""Schematic implementation of the Creator pattern

Back to the previous example
An instance of a class (a card) is created by the class (an owner) which makes use of it"""


class Human:
    pass


class CardOwner(Human):
    def __init__(self, birth_name):
        self.__cards: list[CreditCard] = list()
        self.name = birth_name
        ...
    ...

    def create_card(self):
        new_card = CreditCard(self.name)
        self.__cards.append(new_card)
    ...


class CreditCard:
    def __init__(self, holder_name):
        self.__transactions = dict()
        self.holder_name = holder_name
        ...
    ...

"""Schematic implementation of the Info Expert pattern

CardOwner doesn't calculate total for every card.
Each card does it itself, because It keeps all the info about transactions.
The Owner calculates total on All the cards that He owns."""


class CardOwner:
    def __init__(self):
        self.__cards: list[CreditCard] = list()
        ...
    ...

    def total_flow(self):
        return sum(card.total_cash for card in self.__cards)


class CreditCard:
    def __init__(self):
        self.__transactions = dict()
        ...
    ...

    def total_cash(self):
        return sum(self.__transactions.values())

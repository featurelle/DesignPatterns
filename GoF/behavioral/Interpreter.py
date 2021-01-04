from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty


# sentence = '(3 - 15 + 99 - 247 * (20 - ((12 - 2 * (20 / (10 + 4))) - 14)) / 15 - -(10 - 2) + 100) * 2 + 10000 / 250'


class Expression(ABC):

    @abstractmethod
    def interpret(self):
        pass

    
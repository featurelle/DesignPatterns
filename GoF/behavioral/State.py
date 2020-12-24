# Смысл: делигровать работу, зависящую от состояния, отдельным классам Состояний
# Переключение из состояния теряет смысл в данном примере, если состояний больше двух
# TODO: Отличие от Стратегии? То, что состояние знает о своем контексте? А практическяа польза?

from __future__ import annotations
from abc import ABC, abstractmethod


class State(ABC):

    def __init__(self, machine: TextType):
        self.machine = machine

    @abstractmethod
    def type(self, *args):
        pass


class AllUpper(State):

    def type(self, string: str):
        print(string.upper())

    def switch_style(self):
        self.machine.style = self.machine.low


class AllLower(State):

    def type(self, string: str):
        print(string.lower())

    def switch_style(self):
        self.machine.style = self.machine.up


class TextType:

    def __init__(self):
        self.up = AllUpper(self)
        self.low = AllLower(self)
        self.style = self.low

    def switch(self):
        self.style.switch_style()

    def type(self, string: str):
        self.style.type(string)


if __name__ == "__main__":

    machine = TextType()
    machine.type('Hello')
    machine.switch()
    machine.type('Hello')

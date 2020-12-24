from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


# Единственное, что требуется от Итерируемого класса - уметь возвращать свой Итератор
class Iterable(ABC):

    def __iter__(self) -> Iterator:
        return self.iterate()

    @abstractmethod
    def iterate(self) -> Iterator:  # Метод конкретной коллекции должен возвращать конкретного Итератора
        pass


class Iterator(ABC, Iterable):

    # С помощью дефолтных значений позволяю тонко настраивать создаваемый итератор, но Только если захочется
    # При этом остается возможность ничего о них не знать и использовать только базовый функционал
    def __init__(self,
                 sequence: Iterable,
                 step: int = 1,
                 reverse: bool = False,
                 finite: bool = True):
        self.__sequence = sequence
        self._step = step
        self._reverse = reverse
        self._finite = finite
        self._current: Any

    # C помощью сеттеров позволяю изменять поведение Итератора на ходу (тут бы подошел паттерн State или вроде того)
    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step: int):
        self._step = step

    @property
    def finite(self):
        return self._finite

    @finite.setter
    def finite(self, finite: bool):
        self._finite = finite

    def reverse(self):
        self._reverse = not self._reverse

    @abstractmethod
    def current(self) -> Any:
        pass

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def remove(self) -> None:
        pass

    @abstractmethod
    def next(self) -> Any:
        pass

    @abstractmethod
    def prev(self) -> Any:
        pass

    # __next__ позволяет работать как через свой метод, так и через встроенную функцию next([GeneratorIterator])
    # Поведенние как и у встроенных - когда следующего элемента нет, выплевывает ошибку StopIteration
    def __next__(self):
        if not self.has_next():
            raise StopIteration
        else:
            self.next()

    # Итератор сам по себе также можно итерировать. Он просто возвращает самого себя.
    def __iter__(self) -> Iterator:
        return self


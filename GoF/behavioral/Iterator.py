from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union, Optional
from functools import singledispatchmethod
import random


# Задача: Посчитать количество пены, необходимое для герметизации всех деревянных окон в нескольких домах.
# Окна приведены к одному классу, но вот проблема: классы домов сруктурируют и хранят окна по-разному!
# При сохранении Mutability - вторая выполнимая задача - поменять все деревянные окна на пластиковые.
# В моем примере сами Итераторы - тоже Коллекции, которые можно проитерировать.


# Единственное, что требуется от Итерируемого класса - уметь возвращать свой Итератор
class Iterable(ABC):

    def __iter__(self) -> Iterator:
        return self.iterate()

    @abstractmethod
    def iterate(self) -> Iterator:  # Метод конкретной коллекции должен возвращать конкретный Итератор
        pass


class Window:

    def __init__(self, width: int, length: int, plastic: bool = False):
        self.width = width
        self.length = length
        self.plastic = plastic


# Old House хранит окна в виде списков окон внутри списка этажей
class OldHouse(Iterable):

    def __init__(self, floors: int, windows_per_floor: int):
        self.floors = list()
        for _ in range(floors):
            plastic = random.choice([False] * 2 + [True] * 5)   # 5 к 2, что на этаже пластиковые окна
            self.floors.append([Window(300, 200, plastic) for _ in range(windows_per_floor)])

    def iterate(self) -> RecursiveWindowListIterator:
        return RecursiveWindowListIterator(self.floors)


# VeryOldHouse хранит окна в виде словаря этажей
class VeryOldHouse(Iterable):

    def __init__(self, floors: int, windows_per_floor: int):
        self.floors = dict()
        for i in range(floors):
            plastic = random.choice([False] * 9 + [True] * 2)   # 9 к 2, что на этаже деревянные окна
            self.floors[i + 1] = ([Window(200, 150, plastic) for _ in range(windows_per_floor)])

    def iterate(self) -> VeryOldHouseIterator:
        return VeryOldHouseIterator(self.floors)


class Iterator(ABC):

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def has_next(self):
        pass


class SimpleWindowListIterator(Iterator):

    def __init__(self, seq: list[Window]):
        self.seq = seq
        self.current = 0

    def next(self) -> Window:
        if self.has_next():
            item = self.seq[self.current]
            self.current += 1
            return item
        else:
            raise StopIteration

    def has_next(self):
        if self.current < len(self.seq) - 1:
            return True
        else:
            return False


class RecursiveWindowListIterator(Iterator):

    def __init__(self, seq: list):
        self.current = 0
        self.floors = [SimpleWindowListIterator(i) for i in seq]

    def next(self) -> Window:
        if self.has_next():
            try:
                return self.floors[self.current].next()
            except StopIteration:
                self.current += 1
                return self.next()
        else:
            raise StopIteration

    def has_next(self):
        if self.current < len(self.floors) - 1:
            return True
        else:
            return False


class VeryOldHouseIterator(Iterator):

    def __init__(self, seq: dict):
        self.current = 0
        self.floors = [SimpleWindowListIterator(i) for i in seq.values()]

    def next(self) -> Window:
        if self.has_next():
            try:
                return self.floors[self.current].next()
            except StopIteration:
                self.current += 1
                return self.next()
        else:
            raise StopIteration

    def has_next(self):
        if self.current < len(self.floors) - 1:
            return True
        else:
            return False


def demo():

    house1 = OldHouse(9, 5)
    house2 = VeryOldHouse(5, 12)

    iterator1 = house1.iterate()
    iterator2 = house2.iterate()

    while True:
        try:
            print(iterator1.next().plastic)
        except StopIteration:
            break

    print(('-' * 50 + '\n') * 3)

    while True:
        try:
            print(iterator2.next().plastic)
        except StopIteration:
            break


if __name__ == "__main__":
    demo()

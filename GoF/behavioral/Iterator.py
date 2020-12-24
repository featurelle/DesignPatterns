from __future__ import annotations
from abc import ABC, abstractmethod
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

    def iterate(self) -> OldHouseIterator:
        return OldHouseIterator(self.floors)    # Для меня важный момент: передается копия, а не оригинал этажей


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


# Тут что-то вроде небольшой рекурсии получилось
class ListIterator(Iterator):

    def __init__(self, seq: list):
        self.seq = seq
        self.current = 0

    @abstractmethod
    def next(self):
        pass

    def has_next(self):
        if self.current < len(self.seq) - 1:
            return True
        else:
            return False


class SimpleListIterator(ListIterator):     # Мб тут другой паттерн использовать для замены наследования)

    def __init__(self, seq: list[Window]):
        super().__init__(seq)

    def next(self) -> Window:
        if self.has_next():
            item = self.seq[self.current]
            self.current += 1
            return item
        else:
            raise StopIteration


class OldHouseIterator(ListIterator):

    def __init__(self, seq: list[list[Window]]):
        super().__init__(seq)

    def next(self) -> Window:
        if self.has_next():
            try:
                nested_iterator = SimpleListIterator(self.seq[self.current])
                yield nested_iterator.next()
            except StopIteration:
                self.current += 1
        else:
            raise StopIteration


class VeryOldHouseIterator(Iterator):

    def __init__(self, floors: dict):
        self.floors = floors
        self.floor_keys = list(self.floors.keys())
        self.current = 0

    def next(self) -> Window:
        if self.has_next():
            try:
                nested_iterator = SimpleListIterator(self.floors[self.current + 1])
                yield nested_iterator.next()
            except StopIteration:
                self.current += 1
        else:
            raise StopIteration

    def has_next(self):
        if self.current < len(self.floor_keys) - 1:
            return True
        else:
            return False


def demo():

    house1 = OldHouse(9, 5)
    house2 = VeryOldHouse(5, 12)

    iterator1 = house1.iterate()
    iterator2 = house2.iterate()

    while iterator1.has_next():
        print(iterator1.next().plastic)

    print(('-' * 50 + '\n') * 3)

    while True:
        try:
            print(iterator2.next().plastic)
        except StopIteration:
            break


if __name__ == "__main__":
    demo()

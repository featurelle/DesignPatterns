from __future__ import annotations
from abc import ABC, abstractmethod
import random


# Задача: Посчитать расходы на замену всех деревянных окон в нескольких домах.
# Окна приведены к одному классу, но вот проблема: классы домов сруктурируют и хранят окна по-разному!
# При сохранении Mutability - вторая выполнимая задача - поменять все деревянные окна на пластиковые во время прохода.


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

    # Как на самом деле надо было это решать (по крайней мере в данном случае):
    #
    # def iterate(self) -> RecursiveWindowListIterator:
    #     return RecursiveWindowListIterator(self.floors.values())
    #
    # И никакой третий вид Итераторов был бы не нужен.


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


# А это адаптер, по большому счету
class VeryOldHouseIterator(RecursiveWindowListIterator):

    def __init__(self, seq: dict):
        super().__init__(list(seq.values()))


def calc_expenses(house):

    iterator = house.iterate()
    expenses = 0
    while True:
        try:
            if not (window := iterator.next()).plastic:
                expenses += (window.width + window.length) * 2
        except StopIteration:
            return expenses


def stolen_money():

    return random.choice([True, False])


def put_plastic(house):

    iterator = house.iterate()
    while True:
        try:
            if not (window := iterator.next()).plastic:
                window.plastic = True   # Тут меняется состояние исходного объекта
        except StopIteration:
            break


# А вот тут легкий вариант Композита мог бы сам выдавать подобный метод.
# Или Посетитель мог бы посещать дома и делать свои делишки, обращаясь к дереву объектов.
def is_job_done(house):

    iterator = house.iterate()
    while True:
        try:
            if not iterator.next().plastic:
                return False
        except StopIteration:
            return True


def demo():

    budget = 30000

    print()

    houses = OldHouse(9, 5), VeryOldHouse(5, 12)

    for house in houses:

        exp = calc_expenses(house)
        print('Total expenses on the old house will be: ', exp, '$')

        if exp <= budget:
            budget -= exp
            if not stolen_money():
                put_plastic(house)
            print('Well done!' if is_job_done(house) else 'Wow, someone must have stolen all our taxes. Typical UA :(')
        else:
            print('Unfortunately, we have no funds to renovate this old house.')

        print(('\n' + ('-' * 50) + '\n') * 3)


if __name__ == "__main__":
    demo()

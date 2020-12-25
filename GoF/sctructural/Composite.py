import random
from abc import ABC, abstractmethod

# Другой взгляд на задачу, описанную у меня в Итераторе


class TownComponent(ABC):
    pass


class Window(TownComponent):

    def __init__(self, width: int, length: int, plastic: bool = False):
        self.width = width
        self.length = length
        self.plastic = plastic


class Composite(TownComponent):
    pass


class Floor(Composite):
    pass


# Old House хранит окна в виде списков окон внутри списка этажей
class OldHouse(Composite):

    def __init__(self, floors: int, windows_per_floor: int):
        self.floors = list()
        for _ in range(floors):
            plastic = random.choice([False] * 2 + [True] * 5)   # 5 к 2, что на этаже пластиковые окна
            self.floors.append([Window(300, 200, plastic) for _ in range(windows_per_floor)])


# VeryOldHouse хранит окна в виде словаря этажей
class VeryOldHouse(Composite):

    def __init__(self, floors: int, windows_per_floor: int):
        self.floors = dict()
        for i in range(floors):
            plastic = random.choice([False] * 9 + [True] * 2)   # 9 к 2, что на этаже деревянные окна
            self.floors[i + 1] = ([Window(200, 150, plastic) for _ in range(windows_per_floor)])


class Town:
    pass
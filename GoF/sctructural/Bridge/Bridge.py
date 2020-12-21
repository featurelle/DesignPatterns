from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime


import pyperclip as clip


# Отчет является абстракцией, которую мы хотим отделить от конкретных вещей: источников информации
# Мы также хотим компоновать любого вида отчет на основании любого вида информации.
class Report(ABC):

    def __init__(self, resource: Resource):
        self._resource = resource

    @abstractmethod
    def make(self):
        pass


# Ресурсам желательно приделать name, чтобы было понятно от кого это
class ReportToFile(Report):

    def __init__(self, resource, path):
        super().__init__(resource)
        self.__path = path

    def make(self):
        id_ = self._resource.id()
        time = self._resource.time()
        event = self._resource.event()
        info = f'{id_}: {event} ||| at {time}'
        with open(file=self.__path, mode='w') as file:
            print(info, file=file)


class ReportToString(Report):

    def make(self):
        time = self._resource.time()
        event = self._resource.event()
        info = f'{time}: {event}'
        print(info)


class ReportToBuffer(Report):

    def make(self):
        clip.copy(self._resource.event())


# Ресурс - интерфейс, который необходимо поддерживать классам, чтобы по ним можно было создавать репорты
# Ресурсы могут быть какие угодно, благодаря интерфейсу мы даем им общее поведение, которое нас интересует, без
# Вникания в различия между кокнретными источниками информации. Pure Fabrication!
class Resource(ABC):

    @abstractmethod
    def event(self) -> str:
        pass

    @abstractmethod
    def time(self) -> str:
        pass

    @abstractmethod
    def id(self) -> str:
        pass


# Кокнетные ресурсы отличаются и своим поведением и типом информации, которую они хранят и обрабатывают
class CheckType1(Resource):

    __checks = []

    def __init__(self, money, client, cashier):
        self.__money = money
        self.__client = client
        self.__cashier = cashier
        self.__class__.__checks.append(self)
        self.__id = self.__class__.__checks.index(self)
        self.__time = datetime.now()

    def id(self):
        return str(self.__id)

    def time(self):
        return str(self.__time)

    def event(self):
        return f'Money received: {self.__money}'


class CheckType2(Resource):

    __last = 0

    def __init__(self, money, cashier, table):
        self.__money = money
        self.__table = table
        self.__cashier = cashier
        self.__class__.__last += 1
        self.__id = self.__class__.__last
        self.__time = datetime.now()

    def event(self) -> str:
        return f'Money received: {self.__money}'

    def time(self) -> str:
        return str(self.__time)

    def id(self):
        return str(self.__id)


class Collection(Resource):

    def __init__(self, amount, time, collector, number):
        self.__amount = amount
        self.__time = time
        self.__collector = collector
        self.__number = number

    def event(self) -> str:
        return f'Collection: -{self.__amount} by {self.__collector}'

    def time(self) -> str:
        return str(self.__time)

    def id(self) -> str:
        return str(self.__number)


def demo():
    col1 = Collection(1000, datetime.now(), 'Steve Jobs', 2)
    col2 = Collection(3000, datetime.now(), 'Bill Gates', 3)
    check1 = CheckType1(300, None, None)
    check2 = CheckType1(400, None, None)
    check3 = CheckType2(250, None, None)
    check4 = CheckType2(300, None, None)

    reports = [
               ReportToFile(col1, '../rep1.txt'),
               ReportToFile(check1, '../check.txt'),
               ReportToString(col2),
               ReportToString(check3),
               ReportToBuffer(check2),
               ReportToBuffer(check4)
    ]

    for report in reports:
        report.make()
    else:
        print(clip.paste())


if __name__ == "__main__":
    demo()

from __future__ import annotations
from abc import ABC, abstractmethod


class ServerInterface(ABC):

    @abstractmethod
    def load(self, *args):
        pass

    @abstractmethod
    def response(self, *args):
        pass

    @abstractmethod
    def status(self, *args):
        pass


# Есть разные виды Прокси, тут показана простая абстрактная солянка из всех
# Не очень понятно, зачем что-то "скрывать" от клиента, которым являюсь я сам...
# Разве что Сервер мне недоступен и я не могу на нем сделать нужные проверки
# Но тогда неясно, зачем мне интерфейс отдельный, можно же по честному наследовать прокси от сервера...
class Server(ServerInterface):

    def load(self):
        pass    # Трудоемкий процесс запуска

    def response(self, request):
        return f'{request} proceeded'    # Ответ на какой-то запрос, простой, но требует запуска

    def status(self):
        return 'Hello World'    # В некоторых случаях не требует запуска, возвращая что-то стандартное


# Класс Прокси имитирует сервер для клиента
class Proxy(ServerInterface):

    def __init__(self):
        self.server = Server()    # Хоть убей, не вижу смысла в паттерне, если бы клиент передавал настоящий сервис
        self.cash = dict()   # Кэш с последними вызовами и параметрами

    def load(self, auth_keys, ip):
        if auth_keys != 'some_injection':   # Прокси защищает сервер от хакерских атак
            print('Loading...')
            self.server.load()
        else:
            print('Oops...')
            self.block(ip)

    def block(self, ip):
        pass

    def response(self, request):
        if request not in self.cash['response']:    # Сервер вызывается, только если ответ на запрос нельзя взять из кэш
            self.cash['response'][request] = self.server.response(request)
        return self.cash['response'][request]

    def status(self, id):
        if self.cash['status'][id]:
            ...     # Та же самая логика

# И все-таки вопрос: Зачем интерфейс, если можно наследовать прокси от Сервера? Что этим решается?
# TODO: лучше было бы сделать Прокси для какой-то библиотеки,
#  которая выдает ошибки и ложит программу, если клиент что-то не так ввел
#  например, этот Прокси может проверять, правильно ли введены аргументы для функций и тп

from __future__ import annotations
import random
from string import ascii_lowercase, ascii_uppercase, digits

chars = ascii_lowercase + ascii_uppercase + digits


class Mediator:

    def notify(self, user: User, message: str):
        raise NotImplementedError


class User:

    def __init__(self, mediator: Mediator, name: str):
        self._mediator = mediator
        self._history = []
        self.name = name

    def seng_message(self, msg):
        self._mediator.notify(self, msg)

    def receive_message(self, sender: str, msg: str):
        self._history.append((sender, msg))

    def show_history(self):
        print(*self._history, sep='\n')


class Chat(Mediator):

    def __init__(self, admins: list[Admin], users: list[RegularUser], hidden: list[HiddenUser], name: str):
        self._admins = admins
        self._users = users
        self._hidden = hidden
        self._name = name

    # Сообщения с вызовом бота (от админа запрос - ответ один, от юзера - ответ другой) разукрасят этот скучный пример!
    def notify(self, user: User, message: str):
        if type(user) == RegularUser or type(user) == Admin:
            self.to_all(user, message)
        elif type(user) == HiddenUser:
            self.to_hidden(user, message)

    def to_all(self, user: User, message: str):
        for each in self._users + self._admins + self._hidden:
            each.receive_message(user.name, message)

    def to_hidden(self, user: User, message: str):
        for each in self._admins + self._hidden:
            each.receive_message(user.name, message)








class Admin(User):

    pass


class RegularUser(User):

    pass


class HiddenUser(User):

    pass


def random_name():
    length = random.randint(5, 12)
    name = ''.join(random.choice(chars) for _ in range(length))
    return name


def demo():

    users, admins, hidden = [], [], []

    for _ in range(20):
        users.append(RegularUser(random_name()))
    # Печалька произошла((
    for _ in range(7):
        admins.append

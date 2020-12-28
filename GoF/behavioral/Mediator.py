from __future__ import annotations
import random
from string import ascii_lowercase, ascii_uppercase, digits

chars = ascii_lowercase + ascii_uppercase + digits


class Mediator:

    def notify(self, user: User, message: str):
        raise NotImplementedError

    def show_users(self, user: User):
        raise NotImplementedError


class User:

    type: str

    def __init__(self, name: str):
        self._mediator = None
        self._history = []
        self.name = name

    def send_message(self, msg):
        self._mediator.notify(self, msg)

    def receive_message(self, sender: str, msg: str):
        self._history.append((sender, msg))

    def show_history(self):
        print('\n\n>>>>' + self.name + '\'s ' + f'({self.type})' + ' chat history:')
        print(*self._history, sep='\n')

    def who_i_see(self):
        print('\n\n>>>>' + self.name + '\'s ' + f'({self.type})' + ' visible users:')
        print(*self._mediator.show_users(self), sep='\n')

    def mediator(self, mediator: Mediator):
        self._mediator = mediator


class Chat(Mediator):

    def __init__(self, name: str):
        self._admins = list()
        self._users = list()
        self._hidden = list()
        self._name = name

    def add_admin(self, admin: Admin):
        admin.mediator(self)
        self._admins.append(admin)

    def add_user(self, user: RegularUser):
        user.mediator(self)
        self._users.append(user)

    def add_hidden(self, hidden: HiddenUser):
        hidden.mediator(self)
        self._hidden.append(hidden)

    def show_users(self, user: User):
        if type(user) == RegularUser:
            return self._users + self._admins
        else:
            return self._users + self._admins + self._hidden

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

    type = 'Admin'


class RegularUser(User):

    type = 'User'


class HiddenUser(User):

    type = 'Hidden'


def random_name():
    length = random.randint(5, 12)
    name = ''.join(random.choice(chars) for _ in range(length))
    return name


def demo():

    chat = Chat("Super chat")

    users, admins, hidden = [], [], []

    for _ in range(20):
        users.append(RegularUser(random_name()))

    for _ in range(7):
        admins.append(Admin(random_name()))

    for _ in range(15):
        hidden.append(HiddenUser(random_name()))

    for each in users:
        chat.add_user(each)

    for each in admins:
        chat.add_admin(each)

    for each in hidden:
        chat.add_hidden(each)

    users[0].who_i_see()
    hidden[0].who_i_see()
    admins[0].who_i_see()

    users[6].send_message('Hi everyone! How are you doing?')
    hidden[1].send_message('Lmao lamer')
    hidden[2].send_message('Yeah')
    hidden[10].send_message('Absolutely')
    users[15].send_message('Hi! All okay! We were just starting!')
    admins[4].send_message('Please attention everybody! New rules... Blah-blah-blah')
    users[0].send_message('Welll okaaaayy')
    hidden[2].send_message('I knew we will end up like this. Lame...')

    users[6].show_history()
    admins[6].show_history()
    hidden[6].show_history()


if __name__ == "__main__":
    demo()

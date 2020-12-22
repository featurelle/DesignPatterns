from __future__ import annotations
from abc import ABC, abstractmethod


class Smartphone:

    def __init__(self, implementation: OperationalSystem):
        self.os = implementation

    def lockscreen(self):
        print(f'Some smartphone: lockscreen looks like {self.os.lockscreen_implementation()}')


class SuperSmartphone(Smartphone):

    def lockscreen(self):
        super(SuperSmartphone, self).lockscreen()
        print('And it does something super at the same time!')


class OperationalSystem(ABC):

    @abstractmethod
    def lockscreen_implementation(self):
        pass


class Android(OperationalSystem):

    def lockscreen_implementation(self):
        return 'Android Lockscreen'


class WindowsPhone(OperationalSystem):
    def lockscreen_implementation(self):
        return 'Windows Lockscreen'


def buy_phones():
    android = Android()
    windows = WindowsPhone()

    combinations = Smartphone(android), SuperSmartphone(android), Smartphone(windows), SuperSmartphone(windows)

    for phone in combinations:
        phone.lockscreen()
        print()


if __name__ == "__main__":
    buy_phones()

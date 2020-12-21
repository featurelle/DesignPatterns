from GoF.behavioral.Observer import Observer, Observable
import functools


# В принципе синглтон можно создать и с помощью декоратора
def singleton(cls):
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton


@singleton
class LogDecorated(Observer):

    def __init__(self):
        self.__changes = []

    def show_log(self):
        ending_line = '\n' + '.' * 10 + '\n\n'
        print(*self.__changes, sep='\n', end=ending_line)

    def update(self, source, change):
        self.__changes.append(f'At {source.name}: {change}.')


class Singleton:

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance:
            pass
        else:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __str__(self):
        return 'I am the only one!'


class Log(Observer, Singleton):

    def __init__(self):
        self.__changes = []

    def show_log(self):
        ending_line = '\n' + '.' * 10 + '\n\n'
        print(*self.__changes, sep='\n', end=ending_line)

    def update(self, source, change):
        self.__changes.append(f'At {source.name}: {change}.')


class SomeClass(Observable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.state = 'New object'
        self.add_observer(Log())    # Можно также обеспечить обязательное создание лога без вызова метода извне

    def change_state(self, new_state):
        self.state = new_state
        self.notify_observers(self.state)

    @property
    def log(self):
        return self._observers[0]


def demo():
    log1 = Log()
    o1 = SomeClass('Object1')
    o1.add_observer(log1)

    log2 = Log()
    o2 = SomeClass('Object2')
    o2.add_observer(log2)

    print(log1 == log2)
    print(o1.log == o2.log)
    print(log1 == o2.log)

    log1.show_log()
    o1.change_state('Now I have changed')
    log2.show_log()
    o2.change_state('And me too')
    log1.show_log()
    log2.show_log()

    print(log1 == log2)
    print(log1)

    print('Now with decorator')
    log3, log4 = LogDecorated(), LogDecorated()
    print(log3 == log4)
    print(str(log3))    # Но классы удобнее использовать, ведь во-первых они понятнее, во-вторых их функционал богаче.
    # Я бы много времени потратил, пытаясь обернуть еще и метод __str__ с помощью декоратора. А зачем, если есть классы?


if __name__ == "__main__":
    demo()

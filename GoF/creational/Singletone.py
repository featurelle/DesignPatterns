from GoF.behavioral.Observer.Observer import Observer, Observable


class Log(Observer):

    __instance = None

    def __init__(self):
        self.__changes = []

    def __new__(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance

        else:
            cls.__instance = object.__new__(cls)
            return cls.__instance

    def __str__(self):
        return 'I am the only one!'

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

    def change_state(self, new_state):
        self.state = new_state
        self.notify_observers(self.state)


def demo():
    log1 = Log()
    o1 = SomeClass('Object1')
    o1.add_observer(log1)

    log2 = Log()
    o2 = SomeClass('Object2')
    o2.add_observer(log2)

    print(log1 == log2)

    log1.show_log()
    o1.change_state('Now I am old')
    log2.show_log()
    o2.change_state('And me too')
    log1.show_log()
    log2.show_log()


if __name__ == "__main__":
    demo()

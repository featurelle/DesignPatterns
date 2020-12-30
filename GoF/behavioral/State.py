from __future__ import annotations
from abc import ABC, abstractmethod

# А если еще стэп добавить, то классу вообще *** настанет)


# Один абстрактный стейт, который в свою очередь тоже имеет Свое состояние - конечность и бесконечность!
class IteratorState(ABC):

    def __init__(self, iterator: ListIterator):
        self.iterator = iterator

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def inverse(self):
        pass

    @abstractmethod
    def accept(self, v: StateVisitor):
        pass


class StateVisitor(ABC):
    # Обязанности Стейта:
    def __init__(self, iterator: ListIterator):
        self.iterator = iterator

    @abstractmethod
    def toggle_finite(self):
        pass

    # Обязанности Визитора:
    @abstractmethod
    def forward(self, state: ForwardDirectionIter):
        pass

    @abstractmethod
    def backward(self, state: BackwardDirectionIter):
        pass


class FiniteStateVisitor(StateVisitor):

    def forward(self, state: ForwardDirectionIter):
        return state.next()

    def backward(self, state: BackwardDirectionIter):
        return state.next()

    def toggle_finite(self):
        self.iterator.finite = InfiniteStateVisitor(self.iterator)


class InfiniteStateVisitor(StateVisitor):

    def forward(self, state: ForwardDirectionIter):
        try:
            return state.next()
        except StopIteration:
            state.iterator.current = -1
            return state.next()

    def backward(self, state: BackwardDirectionIter):
        try:
            return state.next()
        except StopIteration:
            state.iterator.current = len(state.iterator.seq)
            return state.next()

    def toggle_finite(self):
        self.iterator.finite = FiniteStateVisitor(self.iterator)


# Конкретные Стейты с разными функциями
class ForwardDirectionIter(IteratorState):

    def next(self):
        if self.has_next():
            self.iterator.current += 1
            item = self.iterator.seq[self.iterator.current]
            return item
        else:
            raise StopIteration

    def has_next(self):
        if self.iterator.current < len(self.iterator.seq) - 1:
            return True
        else:
            return False

    def inverse(self):
        self.iterator.direction = BackwardDirectionIter(self.iterator)

    def accept(self, v: StateVisitor):
        return v.forward(self)


class BackwardDirectionIter(IteratorState):

    def next(self):
        if self.has_next():
            self.iterator.current -= 1
            item = self.iterator.seq[self.iterator.current]
            return item
        else:
            raise StopIteration

    def has_next(self):
        if self.iterator.current > 0:
            return True
        else:
            return False

    def inverse(self):
        self.iterator.direction = ForwardDirectionIter(self.iterator)

    def accept(self, v: StateVisitor):
        return v.backward(self)


class ListIterator:

    def __init__(self, seq: list):
        self.seq = seq
        self.current = -1
        self.direction = ForwardDirectionIter(self)
        self.finite = FiniteStateVisitor(self)

    def next(self):
        return self.direction.accept(self.finite)

    def has_next(self):
        return self.direction.has_next()

    def change_direction(self):
        self.direction.inverse()

    def toggle_finite(self):
        self.finite.toggle_finite()


def demo():
    sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    iterator = ListIterator(sequence)

    while True:
        try:
            print(iterator.next())
        except StopIteration:
            print('Switching direction!')
            iterator.change_direction()
            break

    # Работает через ***, поменять!
    while True:
        try:
            print(iterator.next())
        except StopIteration:
            print('Now making it infinite!')
            iterator.toggle_finite()
            break

    for _ in range(100):
        print(iterator.next())
    else:
        print('Now backwards again in infinite mode!')
        iterator.change_direction()

    for _ in range(100):
        print(iterator.next())


if __name__ == "__main__":
    demo()

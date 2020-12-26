from __future__ import annotations
from abc import ABC, abstractmethod

# Один абстрактный стейт
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


# Конкретные Стейты с разными функциями
class ForwardDirectionIter(IteratorState):

    def next(self):
        if self.has_next():
            item = self.iterator.seq[self.iterator.current]
            self.iterator.current += 1
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


class BackwardDirectionIter(IteratorState):

    def next(self):
        if self.has_next():
            item = self.iterator.seq[self.iterator.current]
            self.iterator.current -= 1
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




class FiniteIter(IteratorState):

    def next(self):
        # Обращаюсь к методу Итератора, а не другого вида Стейт, таким образом позволяю менять виды Стейт независимо
        if self.iterator.has_next():
            self.iterator.next()
        else:
            self.ite




class ListIterator:

    def __init__(self, seq: list):
        self.seq = seq
        self.current = 0
        self.direction = ForwardDirectionIter(self)

    def next(self):
        self.direction

    def has_next(self):
        self.direction.has_next()

    def change_direction(self):
        pass

    def toggle_finite(self):
        pass

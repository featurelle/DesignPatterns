from abc import ABC, abstractmethod

from GoF.behavioral.Iterator import Iterator


class AverageCalculator(ABC, Iterator):

    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def next_item(self):
        pass

    def average(self):
        try:
            num_items = 0
            total_sum = 0
            while self.has_next():
                total_sum += self.next_item()
                num_items += 1

            return round(total_sum / num_items, 3)

        except ZeroDivisionError:
            raise RuntimeError("Can not calculate the average of an empty sequence")

        finally:
            self.dispose()

    def dispose(self):
        pass


class FileAverageCalculator(AverageCalculator):

    def __init__(self, file):
        self.file = file
        self.last_line = self.file.readline()

    def has_next(self):
        return self.last_line != ''

    def next_item(self):
        item = float(self.last_line)
        self.last_line = self.file.readline()
        return item

    def dispose(self):
        self.file.close()


class ListAverageCalculator(AverageCalculator):

    def __init__(self, seq):
        self.seq = seq

    def has_next(self):
        return bool(self.seq)

    def next_item(self):
        return self.seq.pop()


def demo():

    seq = [19, 20, 11, 0, 5, 7, 3]
    seq_file = open('sequence.txt')

    calc1 = FileAverageCalculator(seq_file)
    print('Average from a file: ', calc1.average())

    calc2 = ListAverageCalculator(seq)
    print('Average from a list: ', calc2.average())


if __name__ == "__main__":
    demo()


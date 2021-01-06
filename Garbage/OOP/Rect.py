class IArea:

    @property
    def area(self):
        raise NotImplementedError


class Rectangle(IArea):

    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    @property
    def area(self):
        return self.a * self.b


class Square(IArea):

    pass

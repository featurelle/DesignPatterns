from functools import singledispatchmethod


class A:

    def __init__(self):
        self.name = 'A'


class B:

    def __init__(self):
        self.foo = 'bar'


class C:

    @singledispatchmethod
    def fun(self, number):
        print(number)

    @fun.register(A)
    def _(self, number):
        print(number.name)

    @fun.register(B)
    def _(self, b):
        print(b.foo)


a = A()
b = B()
x = 5
c = C()

c.fun(a)
c.fun(b)
c.fun(x)

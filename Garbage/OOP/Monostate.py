class CatInterface:

    def eat(self):
        raise NotImplementedError


class Cat(CatInterface):

    shared_attributes = {
        'breed': 'regular',
        'color': 'pockmarked'
    }

    def __init__(self, name):
        self.__dict__ = Cat.shared_attributes
        self.name = name


cat = Cat("Bob")
print(dir(cat))

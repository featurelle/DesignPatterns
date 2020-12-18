from __future__ import annotations
from abc import ABC, abstractmethod


class Router(ABC):

    def __init__(self, name, movement):
        self._name = name
        self._movement = movement

    @abstractmethod
    def find_route(self, a, b):
        pass

    @property
    def name(self):
        return self._name

    @property
    def movement(self):
        return self._movement


class CarRouter(Router):

    def __init__(self):
        super().__init__('Car', 'Driving by')

    def find_route(self, a, b):
        return (a + b, ) * 2


class BikeRouter(Router):

    def __init__(self):
        super().__init__('Bike', 'Riding on')

    def find_route(self, a, b):
        return a + b, (a + b) * 3


class BusRouter(Router):

    def __init__(self):
        super().__init__('Bus', 'Going by')

    def find_route(self, a, b):
        return a + b, (a + b) * 2


class Navigator:

    def __init__(self, router: Router):
        self._router = router

    @property
    def router(self):
        return self._router

    @router.setter
    def router(self, new_router):
        self._router = new_router

    def show_route_time(self, a, b):
        kms, time = self.router.find_route(a, b)
        print(f'{self.router.movement} a {self.router.name} will take {kms} kms in {time} hours.\n')


def demo():
    bus = BusRouter()
    bike = BikeRouter()
    car = CarRouter()

    navigator = Navigator(bus)
    navigator.show_route_time(10, 35)

    navigator.router = bike
    navigator.show_route_time(20, 35)

    navigator.router = car
    navigator.show_route_time(5, 40)


if __name__ == "__main__":
    demo()

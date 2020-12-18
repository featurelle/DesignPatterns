"""Шуточная демонстрация того, как можно положить квадратный брусок в круглое отверстие с помощью Адаптера
Благодаря Адаптеру можно класть квадратные бруски в круглое отвертстие, представляя их как... круглые!"""

import math


class RoundPeg:
    def __init__(self, radius: int):
        self.radius = radius

    def get_radius(self):
        return self.radius


class SquarePeg:
    def __init__(self, width):
        self.width = width

    def get_width(self):
        return self.width


class RoundHole:
    def __init__(self, radius: int):
        self.radius = radius

    def get_radius(self):
        return self.radius

    def fits(self, peg: RoundPeg) -> bool:
        return self.radius >= peg.get_radius()


class PegAdapter(RoundPeg):
    def __init__(self, peg: SquarePeg):
        radius = peg.get_width() * math.sqrt(2) / 2
        super().__init__(radius)


def client_code():
    hole = RoundHole(7)
    r_peg = RoundPeg(5)

    print(hole.fits(r_peg))

    small_sq_peg = SquarePeg(5)
    large_sq_peg = SquarePeg(12)

    # print(hole.fits(small_sq_peg))   на этом программа умерла и компьютер взорвался из-за неверного типа, ай...

    small_sq_peg_adapter = PegAdapter(small_sq_peg)
    large_pq_peg_adapter = PegAdapter(large_sq_peg)

    print(hole.fits(small_sq_peg_adapter))
    print(hole.fits(large_pq_peg_adapter))


if __name__ == '__main__':
    client_code()

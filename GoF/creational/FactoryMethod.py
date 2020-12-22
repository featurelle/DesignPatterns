from abc import ABC, abstractmethod
import random
from colorama import init, Fore


class Monster(ABC):

    def __init__(self, x, y, skin=Fore.GREEN):
        self.pos = [x, y]
        self.skin = skin

    @abstractmethod
    def attack(self):
        pass


class GiantBat(Monster):

    def attack(self):
        print(self.skin + 'Bat' + Fore.RESET + ' is flying around and throws acid at you')


class GiantBear(Monster):

    def attack(self):
        print(self.skin + 'Bear' + Fore.RESET + ' is attacking you from the ground.')


class RandomMonsterFactory(ABC):

    @abstractmethod
    def create(self):
        pass


class FullyRandomMonsterFactory(ABC):

    def create(self):
        pos = random.randint(0, 255), random.randint(0, 255)
        skin = random.choice([Fore.GREEN, Fore.RED, Fore.CYAN])
        return random.choice([GiantBat, GiantBear])(*pos, skin)


class MySkinRandomMonsterFactory(ABC):

    def create(self, skin):
        if skin == Fore.BLUE:
            possible = [GiantBat]
        else:
            possible = [GiantBat, GiantBear]
        pos = random.randint(0, 255), random.randint(0, 255)
        return random.choice(possible)(*pos, skin)


def demo():

    init()

    fr_fac = FullyRandomMonsterFactory()
    msr_fac = MySkinRandomMonsterFactory()

    m1 = fr_fac.create()
    m2 = msr_fac.create(Fore.BLUE)
    m3 = fr_fac.create()

    m1.attack()
    m2.attack()
    m3.attack()


if __name__ == "__main__":
    demo()

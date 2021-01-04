class Square:

    def __init__(self, side: float):
        self.__side: float = side
        self.__area: float = side ** 2

    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, value: float):
        self.__side = value
        self.__area = value ** 2

    @property
    def area(self):
        return self.__area

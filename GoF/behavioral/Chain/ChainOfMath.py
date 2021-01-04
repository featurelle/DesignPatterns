from __future__ import annotations
import re


NUMBER = r'-?\d+(\.\d+)?'


class MathParser:

    def __init__(self, then: MathParser = None):
        self.then = then

    def parse(self, math: str):
        raise NotImplementedError

    def then(self, parser: MathParser):
        self.then = parser


# Рекурсивные вызовы - это всегда ̶г̶о̶л̶о̶в̶н̶а̶я̶ ̶б̶о̶л̶ь̶ весело!
class BracketsParser(MathParser):

    def parse(self, math: str):
        search = re.search(r'\([0-9 +*/.-]+\)', math)
        if search:
            match = search.group(0).strip('()')
            result = self.then.parse(match)
            modified = math.replace('(' + match + ')', str(result))
            return self.parse(modified)    # Вот здесь рекурсия
        else:
            return float(self.then.parse(math))    # Вот здесь выход из рекурсии // Скобок больше нет


# Привет паттернам Команда/Шаблон и принципу Dependency Injection
class Arithmetics:

    @property
    def regex(self) -> str:
        raise NotImplementedError

    def calculate(self, x: float, y: float) -> float:
        raise NotImplementedError


class Addition(Arithmetics):

    @property
    def regex(self) -> str:
        return r'\+'

    def calculate(self, x: float, y: float) -> float:
        return x + y


class Subtraction(Arithmetics):

    @property
    def regex(self) -> str:
        return r'-'

    def calculate(self, x: float, y: float) -> float:
        return x - y


class Division(Arithmetics):

    @property
    def regex(self) -> str:
        return r'[/:]'

    def calculate(self, x: float, y: float) -> float:
        return x / y


class Multiplication(Arithmetics):

    @property
    def regex(self) -> str:
        return r'\*'

    def calculate(self, x: float, y: float) -> float:
        return x * y


# Путем композиции создаем парсеры для арифметических операций (изначально было 4 больших Почти одинаковых класса)
class ArithmeticParser(MathParser):

    def __init__(self, arithmetics: Arithmetics, then: MathParser = None):
        super().__init__(then)
        self._processor = arithmetics

    def parse(self, math: str):
        search = re.search(fr'{NUMBER} {self._processor.regex} {NUMBER}', math)
        if search:
            match = search.group(0)
            x = float(re.search(fr'^{NUMBER}', match).group(0))
            y = float(re.search(fr'{NUMBER}$', match).group(0))
            result = self._processor.calculate(x, y)
            modified = math.replace(match, str(result))
            return self.parse(modified)
        else:
            return float(self.then.parse(math))


# Последний 'парсер' получает то, что не смогли обработать все остальные. Это либо готовое число, либо ошибка в строке.
class ErrorHandler(MathParser):

    def parse(self, math: str):
        if not re.fullmatch(fr'{NUMBER}', math):
            raise RuntimeError('Invalid syntax!')
        else:
            return float(math)


def do_math():

    arithmetics = [Division(), Multiplication(), Subtraction(), Addition()]

    parsers = [BracketsParser()] + [ArithmeticParser(action) for action in arithmetics] + [ErrorHandler()]

    for n in range(len(parsers) - 1):
        parsers[n].then = parsers[n + 1]

    calculator = parsers[0]

    math_str = '(3 - 15 + 99 - 247 * (20 - ((12 - 2 * (20 / (10 + 4))) - 14)) / 15 - -(10 - 2) + 100) * 2 + 10000 / 250'
    print('I say : ' + math_str + ' = ', end='')

    result = calculator.parse(math_str)

    # Печатаю результаты своего Парсера и стандартного eval(). Результаты совпадают.
    print(round(result, 2))
    print('And python\'s eval() says: ' + str(round(eval(math_str), 2)))


if __name__ == "__main__":
    do_math()

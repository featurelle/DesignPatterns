from __future__ import annotations
import re


NUMBER = r'-?\d+(\.\d+)?'


class MathParser:

    def __init__(self, then: MathParser = None):
        self._then = then

    def parse(self, math: str):
        raise NotImplementedError

    def then(self, parser: MathParser):
        self._then = parser


class BracketsParser(MathParser):

    def parse(self, math: str):
        search = re.search(r'\([0-9 +*/.-]+\)', math)
        if search:
            match = search.group(0).strip('()')
            result = self._then.parse(match)
            modified = math.replace('(' + match + ')', str(result))
            return self.parse(modified)
        else:
            return float(self._then.parse(math))


class Substraction(MathParser):

    def parse(self, math: str):
        search = re.search(fr'{NUMBER} - {NUMBER}', math)
        if search:
            match = search.group(0)
            x = float(re.search(fr'^{NUMBER}', match).group(0))
            y = float(re.search(fr'{NUMBER}$', match).group(0))
            result = x - y
            modified = math.replace(match, str(result))
            return self.parse(modified)
        else:
            return float(self._then.parse(math))


class Addition(MathParser):

    def parse(self, math: str):
        search = re.search(fr'{NUMBER} \+ {NUMBER}', math)
        if search:
            match = search.group(0)
            x = float(re.search(fr'^{NUMBER}', match).group(0))
            y = float(re.search(fr'{NUMBER}$', match).group(0))
            result = x + y
            modified = math.replace(match, str(result))
            return self.parse(modified)
        else:
            return float(self._then.parse(math))


class Multiplication(MathParser):

    def parse(self, math: str):
        search = re.search(fr'{NUMBER} \* {NUMBER}', math)
        if search:
            match = search.group(0)
            x = float(re.search(fr'^{NUMBER}', match).group(0))
            y = float(re.search(fr'{NUMBER}$', match).group(0))
            result = x * y
            modified = math.replace(match, str(result))
            return self.parse(modified)
        else:
            return float(self._then.parse(math))


class Division(MathParser):

    def parse(self, math: str):
        search = re.search(fr'{NUMBER} [/:] {NUMBER}', math)
        if search:
            match = search.group(0)
            x = float(re.search(fr'^{NUMBER}', match).group(0))
            y = float(re.search(fr'{NUMBER}$', match).group(0))
            result = x / y
            modified = math.replace(match, str(result))
            return self.parse(modified)
        else:
            return float(self._then.parse(math))


class ErrorHandler(MathParser):

    def parse(self, math: str):
        if not re.fullmatch(fr'{NUMBER}', math):
            raise RuntimeError('Invalid syntax!')
        else:
            return float(math)


def do_math():
    math_str = '(3 - 15 - (20 - ((12 - 2 * (20 / (10 + 4))) - 14)) - -(10 - 2) + 100) * 2 + 10000 / 250'
    print(math_str + ' = ', end='')
    calculator = BracketsParser(Multiplication(Division(Substraction(Addition(ErrorHandler())))))
    result = calculator.parse(math_str)
    print(round(result, 2))


if __name__ == "__main__":
    do_math()

from __future__ import annotations
import re


class MathParser:

    def __init__(self, then: MathParser = None):
        self._then = then

    def parse(self, math: str):
        raise NotImplementedError

    def then(self, parser: MathParser):
        self._then = parser


class BracketsParser(MathParser):

    def parse(self, math: str):
        search = str(re.search(r'(.+)', math)).strip('()')
        if search:
            result = self.parse(search)
            modified = math.replace('(' + search + ')', str(result))
            return self.parse(modified)
        else:
            return int(self._then.parse(search))


class Substitution(MathParser):

    def parse(self, math: str):
        search = str(re.search(r'\d+ - \d+', math)).strip('()')
        if search:
            x = int(str(re.search(r'^\d+', search)))
            y = int(str(re.search(r'\d+$', search)))
            result = x + y
            modified = math.replace(search, str(result))
            return self.parse(modified)
        else:
            return int(math)



math_str = '3 - 15 - (20 - (12 - 14)) - 1'
bracket_parser = BracketsParser(Substitution())
bracket_parser.parse(math_str)

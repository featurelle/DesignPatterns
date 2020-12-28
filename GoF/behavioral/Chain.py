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
        search = re.search(r'\([0-9 +*/-]+\)', math)
        if search:
            match = search.group(0).strip('()')
            print(match)
            result = self._then.parse(match)
            print(result)
            modified = math.replace('(' + match + ')', str(result))
            print(modified)
            return self.parse(modified)
        else:
            return int(self._then.parse(math))


class Substitution(MathParser):

    def parse(self, math: str):
        search = re.search(r'-?\d+ - -?\d+', math)
        if search:
            match = search.group(0)
            print(match)
            x = int(re.search(r'^-?\d+', match).group(0))
            y = int(re.search(r'-?\d+$', match).group(0))
            result = x - y
            print(result)
            modified = math.replace(match, str(result))
            print(modified)
            return self.parse(modified)
        else:
            return int(math)



math_str = '3 - 15 - (20 - (12 - 14)) - 1'
bracket_parser = BracketsParser(Substitution())
bracket_parser.parse(math_str)

from __future__ import annotations
from abc import ABC, abstractmethod
import re


# А чем же это от декоратора отличается?
# Получился прям в точности декоратор


class BadPassword(Exception):
    pass


class NewPassword:

    def __init__(self, password: str):
        self._password = password

    @property
    def password(self):
        return self._password


class PasswordValidation(ABC):

    def __init__(self, then: PasswordValidation = None):
        self.__then = then

    @abstractmethod
    def check(self, password: NewPassword) -> None:
        pass

    def next(self, password: NewPassword) -> None:
        if self.__then:
            self.__then.check(password)
        else:
            return  # В рекурсии это бы называлось Base Case или терминальная ветка


class PasswordLengthValidation(PasswordValidation):

    def check(self, password: NewPassword) -> None:
        if len(password.password) < 8:
            raise BadPassword('Proper password should have at least 8 symbols')
        else:
            self.next(password)


class PasswordBothCasesValidation(PasswordValidation):

    def check(self, password: NewPassword) -> None:
        if password.password.upper() == password or password.password.lower() == password:
            raise BadPassword('Proper password should have both Upper and Lower cases')
        else:
            self.next(password)


class PasswordDigitsValidation(PasswordValidation):

    def check(self, password: NewPassword) -> None:
        if not re.search(r'\d', password.password):
            raise BadPassword('Proper password should contain digits')
        else:
            self.next(password)


class PasswordSpecSymbolsValidation(PasswordValidation):

    def check(self, password: NewPassword) -> None:
        if not re.search(r'[\W_]', password.password):
            raise BadPassword('Proper password should contain special symbols')
        else:
            self.next(password)


def demo():
    validation1 = PasswordLengthValidation()
    validation2 = PasswordBothCasesValidation(validation1)
    validation3 = PasswordDigitsValidation(validation2)
    validation4 = PasswordSpecSymbolsValidation(validation3)

    passwords = [NewPassword(r'AlfBdfjkhuiwe3123[]\'.)'),
                 NewPassword('Password...'),
                 NewPassword('password123')]

    for password in passwords:
        try:
            validation4.check(password)
        except BadPassword as e:
            print(e)


if __name__ == "__main__":
    demo()

from __future__ import annotations
from abc import ABC, abstractmethod


# Класс Инвокера. Может быть кто угодно, главное чтобы он принимал какую-то команду и мог ее вызывать.
class Invoker:

    def __init__(self):
        self._command = None

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        self._command = command

    def invoke(self):
        if self._command:
            self.command.execute()


# TODO: прибраться тут!
class GUI(ABC):

    def __init__(self):
        self._onclick = OnClick()
        self._onkeypress = OnKeyPress()

    @property
    def onclick(self):
        return self._onclick

    @property
    def onkeypress(self):
        return self._onkeypress

    @onclick.setter
    def onclick(self, invoker: Invoker):
        self._onclick = invoker

    @onkeypress.setter
    def onkeypress(self, invoker: Invoker):
        self._onkeypress = invoker


class Button:

    def __init__(self):
        self.onclick = None
        self.onkeypress = None


class Picture:
    pass


class OnClick(Invoker):

    def invoke(self):
        print('Button was pressed')
        super().invoke()


class OnKeyPress(Invoker):

    def invoke(self):
        print('A picture darkened')
        super().invoke()


# Интерфейс команды задает только метод, с которым умеют работать инвоукеры и необходимость иметь какой-то ресивер.
# Строго говоря, последнее можно и не делать, команда может быть достаточно простой, чтобы выполняться без ресивера.
class Command(ABC):

    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        pass


# Конкретные команды многочисленны и разнообразны, как и их ресиверы
class GetTextFromBuffer(Command):

    def execute(self):
        self.receiver.paste()


class SayGoodbyeToBuffer(Command):

    def execute(self):
        self.receiver.copy("Goodbye!")


class OpenMyLink(Command):

    def __init__(self, receiver, link):
        super().__init__(receiver)
        self.__link = link

    def execute(self):
        self.receiver.open_link(self.__link)


# Один ресивер - это буфер
# Важно, что результат возвращает именно ресивер, в данном случае - печатает в консоль
class TextBuffer:

    def __init__(self):
        self._text = "Hello World"

    def paste(self):
        print(self._text)

    def copy(self, text):
        self._text = text
        print('Copied to the clipboard!')


# Другой может быть вообще чем угодно, например браузером
class Browser:

    ...

    def open_link(self, link):
        print('Opening https://' + link)


# Остается только насоздавать кнопок и картинок, команд и присвоить кнопкам и картинкам команды
# Команды можно менять на ходу, не меняя код инвокеров и ресиверов и не засоряя клиентский код простынями условий elif
if __name__ == "__main__":
    buffer = TextBuffer()

    get_text = GetTextFromBuffer(buffer)
    button1 = OnClick(get_text)

    gb_com = SayGoodbyeToBuffer(buffer)
    button2 = OnClick(gb_com)

    link_opener = Browser()
    link_command = OpenMyLink(link_opener, 'google.com')
    picture = OnKeyPress(link_command)

    button1.invoke()
    button2.invoke()
    picture.invoke()

    picture.command = get_text

    picture.invoke()

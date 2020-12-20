from __future__ import annotations
from abc import ABC, abstractmethod


# Класс Инвокера. Может быть кто угодно, главное чтобы он принимал какую-то команду и мог ее вызывать.
class Invoker:

    def __init__(self, command: OnClick):
        self._command = command

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self):
        return self._command

    def invoke(self):
        self.command.execute()


# TODO: Написать элементам интерфейса разных инвокеров onclick, onkeydown и тп для реализма. И пусть наследуют.
# Конкретные инвокеры могут быть разные и вести себя во время исполнения команды могут по-разному.
# Если сравнивать с пультом, то кнопки имеют разную форму, могут быть сенсорными или обычными, светиться или пищать.
class Button(Invoker):

    def invoke(self):
        return 'Button was pressed\n' + str(super().invoke())


class Picture(Invoker):

    def invoke(self):
        return 'A picture darkened\n' + str(super().invoke())


# Интерфейс команды задает только метод, с которым умеют работать инвоукеры и необходимость иметь какой-то ресивер.
# Строго говоря, последнее можно и не делать, команда может быть достаточно простой, чтобы выполняться без ресивера.
class OnClick(ABC):

    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        pass


# Конкретные команды многочисленны и разнообразны, как и их ресиверы
class GetTextFromBuffer(OnClick):

    def execute(self):
        return self.receiver.text


class SayGoodbyeToBuffer(OnClick):

    def execute(self):
        self.receiver.text = "Goodbye!"


class OpenMyLink(OnClick):

    def __init__(self, receiver, link):
        super().__init__(receiver)
        self.__link = link

    def execute(self):
        self.receiver.open_link(self.__link)


# Один ресивер - это буфер
class TextBuffer:

    def __init__(self):
        self.__text = "Hello World"

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text


# Другой может быть вообще чем угодно, например браузером (открывателем линков)
class LinkOpener:

    def open_link(self, link):
        return 'Opening https://' + link


# Остается только насоздавать кнопок и картинок, команд и присвоить кнопкам и картинкам команды
# Команды можно менять на ходу, не меняя код инвокеров и ресиверов и не засоряя клиентский код простынями условий elif
if __name__ == "__main__":
    buffer = TextBuffer()

    get_text = GetTextFromBuffer(buffer)
    button1 = Button(get_text)

    gb_com = SayGoodbyeToBuffer(buffer)
    button2 = Button(gb_com)

    link_opener = LinkOpener()
    link_command = OpenMyLink(link_opener, 'google.com')
    picture = Picture(link_command)

    print(button1.invoke())
    print(button2.invoke())
    print(picture.invoke())

    picture.command = get_text

    print(picture.invoke())

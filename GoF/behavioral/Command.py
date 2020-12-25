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
    def command(self, command):
        self._command = command

    def invoke(self):
        self.command.execute()


# TODO: Написать элементам интерфейса разных инвокеров onclick, onkeydown и тп для реализма. И пусть наследуют.
# Инвокеры как кнопки на пульте, а данный класс Button скорее пульт в целом, содержащий список своих кнопок (слушатели?)
# Конкретные инвокеры могут быть разные и вести себя во время исполнения команды могут по-разному.
# Если сравнивать с пультом, то кнопки имеют разную форму, могут быть сенсорными или обычными, светиться или пищать.
class Button(Invoker):

    def invoke(self):
        print('Button was pressed')
        super().invoke()


class Picture(Invoker):

    def invoke(self):
        print('A picture darkened')
        super().invoke()


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
        self.receiver.paste()


class SayGoodbyeToBuffer(OnClick):

    def execute(self):
        self.receiver.copy("Goodbye!")


class OpenMyLink(OnClick):

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
    button1 = Button(get_text)

    gb_com = SayGoodbyeToBuffer(buffer)
    button2 = Button(gb_com)

    link_opener = Browser()
    link_command = OpenMyLink(link_opener, 'google.com')
    picture = Picture(link_command)

    button1.invoke()
    button2.invoke()
    picture.invoke()

    picture.command = get_text

    picture.invoke()

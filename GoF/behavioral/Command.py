from __future__ import annotations
from abc import ABC, abstractmethod


class GUI(ABC):

    def __init__(self, onclick: Command = None, onkeypress: Command = None):
        self._onclick = onclick or NullCommand()
        self._onkeypress = onkeypress or NullCommand()

    @property
    def onclick(self):
        return self._onclick

    @property
    def onkeypress(self):
        return self._onkeypress

    @onclick.setter
    def onclick(self, command: Command):
        self._onclick = command

    @onkeypress.setter
    def onkeypress(self, command: Command):
        self._onkeypress = command

    @abstractmethod
    def click(self):
        pass

    @abstractmethod
    def press(self):
        pass


class Button(GUI):

    def click(self):
        self.animate()
        self._onclick.execute()

    def press(self):
        self.animate()
        self._onkeypress.execute()

    def animate(self):
        print('Button was touched')


class Picture(GUI):

    def click(self):
        self.animate()
        self._onclick.execute()

    def press(self):
        self.animate()
        self._onkeypress.execute()

    def animate(self):
        print('Picture darkened')


# Интерфейс команды задает только метод, с которым умеют работать инвоукеры и необходимость иметь какой-то ресивер.
# Строго говоря, последнее можно и не делать, команда может быть достаточно простой, чтобы выполняться без ресивера.
class Command(ABC):

    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        pass


# Коротко про Нулл-обджект паттерн:
class NullCommand(Command):

    def __init__(self):
        pass

    def execute(self):
        print('Nothing happened')


# Конкретные команды многочисленны и разнообразны, как и их ресиверы
class GetTextFromClipboard(Command):

    def execute(self):
        self.receiver.paste()


class SayGoodbyeToClipboard(Command):

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
class Clipboard:

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

    # /// Ресиверы
    clipboard = Clipboard()
    browser = Browser()

    # /// Команды
    get_text = GetTextFromClipboard(clipboard)
    goodbye_command = SayGoodbyeToClipboard(clipboard)
    link_command = OpenMyLink(browser, 'google.com')

    # /// Инвоукеры
    button = Button(onclick=get_text)
    picture = Picture(onkeypress=link_command)

    # Слот пустой
    button.press()
    button.onkeypress = goodbye_command
    button.press()
    button.click()

    # И так далее
    picture.press()
    picture.click()
    picture.onclick = 0  # Exception должен был бы быть, ан-нет!
    # А зачем сеттеры с объявленными типами, если они все равно позволяют любую чушь назначить?

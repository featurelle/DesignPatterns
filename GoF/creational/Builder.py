from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from colorama import init, Fore


# Интерфейс Билдеров
class AppFrameBuilder(ABC):

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def result(self):
        pass

    @abstractmethod
    def create_window(self):
        pass

    @abstractmethod
    def create_tools(self):
        pass

    @abstractmethod
    def create_animation(self):
        pass

    @abstractmethod
    def create_buttons(self):
        pass

    @abstractmethod
    def create_toolbar(self):
        pass

    @abstractmethod
    def result(self):
        pass


class AppFrameBuilderPhone(AppFrameBuilder):

    def __init__(self):
        self.__gui = PhoneGUI()

    def reset(self):
        self.__gui = PhoneGUI()

    def result(self):
        result = self.__gui
        self.reset()
        return result

    def create_window(self):
        self.__gui.add('Frame')

    def create_tools(self):
        self.__gui.add('Gestures')

    def create_animation(self):
        self.__gui.add('Animation')

    def create_buttons(self):
        self.__gui.add('Bottom Panel')

    def create_toolbar(self):
        self.__gui.add('Top Panel')

    def fit_notch(self):
        self.__gui.apply_notch()


class AppFrameBuilderPC(AppFrameBuilder):

    def __init__(self):
        self.__gui = ComputerGUI()

    def reset(self):
        self.__gui = ComputerGUI()

    def result(self):
        result = self.__gui
        self.reset()
        return result

    def create_window(self):
        self.__gui.append('Window')

    def create_tools(self):
        self.__gui.append('Tools')

    def create_animation(self):
        self.__gui.append('Animation')

    def create_hotkeys(self):
        self.__gui.append('Hotkeys')

    def create_buttons(self):
        self.__gui.append('Buttons')

    def create_toolbar(self):
        self.__gui.append('Toolbar')


# Необязательный класс Директора для быстрой сборки по шаблонам
class Director:

    def __init__(self, builder: AppFrameBuilder):
        self.__builder = builder

    def make_full_app_gui(self):
        self.builder.create_window()
        self.builder.create_tools()
        self.builder.create_animation()
        self.builder.create_toolbar()
        self.builder.create_buttons()

    def make_low_requirements_gui(self):
        self.builder.create_window()
        self.builder.create_buttons()

    @property
    def builder(self):
        return self.__builder

    @builder.setter
    def builder(self, builder: AppFrameBuilder):
        self.__builder = builder


# Продукты могут быть слабо связанными между собой, как и конкретные строители
class PhoneGUI:

    def __init__(self):
        self.__elements = []
        self.__appearance = "-----------------\n" + \
                            "|               |\n" * 10 + \
                            "-----------------"

    def add(self, element: Any):
        self.__elements.append(Fore.RED + element + Fore.RESET)

    def demo(self):
        for elem in self.__elements:
            print(f'I have got {elem}')

        print(f'Appearance: \n{self.__appearance}')

    def apply_notch(self):
        self.__appearance = "-----------------\n" \
                           r"|    \\___//    |" + '\n' + \
                            "|               |\n" * 9 + \
                            "-----------------"


class ComputerGUI:

    def __init__(self):
        self.__elements = dict()

    def append(self, element: Any):
        self.__elements[Fore.BLUE + str(len(self.__elements)) + Fore.RESET] = Fore.CYAN + element + Fore.RESET

    def show(self):
        for part, elem in self.__elements.items():
            print(f'I have got {elem} at {part}')


def client():
    ph_b = AppFrameBuilderPhone()
    pc_b = AppFrameBuilderPC()
    d = Director(ph_b)

    d.make_low_requirements_gui()
    ph_b.fit_notch()
    app1 = ph_b.result()
    app1.demo()

    d.make_full_app_gui()
    app2 = ph_b.result()
    app2.demo()

    d.builder = pc_b
    d.make_full_app_gui()
    pc_b.create_hotkeys()
    app3 = pc_b.result()
    app3.show()


if __name__ == "__main__":
    client()

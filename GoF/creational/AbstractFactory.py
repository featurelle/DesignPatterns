from abc import ABC, abstractmethod
import random
from colorama import init, Fore


class GUIFactory(ABC):

    def create_gui_env(self):
        button = self.create_button()
        window = self.create_window()
        return button, window

    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_window(self):
        pass


class WindowsGUIFactory(GUIFactory):

    def create_window(self):
        return WindowsWindow()

    def create_button(self):
        return WindowsButton()


class LinuxGUIFactory(GUIFactory):

    def create_button(self):
        return LinuxButton()

    def create_window(self):
        return LinuxWindow()


class Button(ABC):

    @abstractmethod
    def __str__(self):
        pass


class Window(ABC):

    @abstractmethod
    def __str__(self):
        pass


class WindowsButton(Button):

    def __str__(self):
        return Fore.BLUE + "WinButton" + Fore.RESET


class WindowsWindow(Window):

    def __str__(self):
        return Fore.CYAN + "WinWindow" + Fore.RESET


class LinuxButton(Button):

    def __str__(self):
        return Fore.RED + "LinButton" + Fore.RESET


class LinuxWindow(Window):

    def __str__(self):
        return Fore.RED + "LinWindow" + Fore.RESET


class SomeUserApp:

    def __init__(self):
        self.os = random.choice([WindowsGUIFactory, LinuxGUIFactory])()

    def start(self):
        button, window = self.os.create_gui_env()
        init(autoreset=True)
        print(f"This button: {button} placed in that window: {window}")


def main():
    for _ in range(3):
        app = SomeUserApp()
        app.start()


if __name__ == '__main__':
    main()

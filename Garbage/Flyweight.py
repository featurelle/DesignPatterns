from __future__ import annotations
from datetime import datetime


class FileSystem:

    def full_path(self) -> str:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError

    def show(self) -> str:
        raise NotImplementedError

    def modified(self, when: datetime):
        raise NotImplementedError


class Directory(FileSystem):

    def __init__(self, root: Directory, name: str, visible: bool = True):
        self.root = root
        self.name = name
        self.leaves = []
        self._visible = visible
        self._date_modified = None
        self.modified(datetime.now())

    def modified(self, when: datetime):
        self._date_modified = when
        self.root.modified(when)

    def create_folder(self, name: str):
        new_folder = Directory(self, name)
        self.leaves.append(new_folder)
        return new_folder

    def create_file(self, name: str):
        new_file = File(self, name, str())
        self.leaves.append(new_file)
        return new_file

    def add(self, leaf: FileSystem):
        self.leaves.append(leaf)
        self.modified(datetime.now())

    def full_path(self) -> str:
        return self.root.full_path() + '/' + self.name

    def show(self, indent=0) -> str:
        indentation = '----' * indent
        string = indentation + self.name + '\n'
        for leaf in self.leaves:
            if leaf.visible:
                string += indentation + leaf.show(indent + 1) + '\n'
        return string

    def size(self) -> int:
        total = 0
        for leaf in self.leaves:
            total += leaf.size()
        return total

    def delete(self, leaf: FileSystem):
        try:
            self.leaves.remove(leaf)
            self.modified(datetime.now())
        except ValueError:
            print('Cannot delete non-existing leaf')

    def move(self, directory: Directory):
        directory.add(self)
        self.root.delete(self)
        self.root = directory
        self.modified(datetime.now())

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, visible: bool):
        self._visible = visible


# Singleton
class SystemRoot(Directory):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__(self, '%%')

    def full_path(self) -> str:
        return self.name

    def modified(self, when: datetime):
        self._date_modified = when

    @property
    def visible(self) -> bool:
        return True

    @visible.setter
    def visible(self, value):
        self._visible = value


class File(FileSystem):

    def __init__(self, root: Directory, name: str, inside: str, visible: bool = True):
        self.root = root
        self.name = name
        self.inside = inside
        self._visible = visible
        self._date_modified = None
        self.modified(datetime.now())

    def modified(self, when: datetime):
        self._date_modified = when
        self.root.modified(when)

    def edit(self, inside):
        self.inside = inside
        self.modified(datetime.now())

    def open(self):
        print('>>> ' + self.name + ' : ' + self.inside)

    def full_path(self) -> str:
        return self.root.full_path() + '/' + self.name

    def show(self, indent=0) -> str:
        return '----' * indent + self.name

    def move(self, directory: Directory):
        directory.add(self)
        self.root.delete(self)
        self.root = directory
        self.modified(datetime.now())

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, visible: bool):
        self._visible = visible

    def size(self) -> int:
        return len(self.inside)


class SearchSystem:

    pass


def demo():

    root = SystemRoot()
    photos = root.create_folder('Photos')
    my = photos.create_folder('My')
    my.create_file('Empty.txt')
    vacation = File(my, 'Vacation.img', 'My vacation photo')
    my.add(vacation)

    print(my.show())
    print(photos.show())
    print(root.show())
    print(vacation.full_path())
    print(root.full_path())

    print()
    my.visible = False
    print(root.show())
    my.visible = True

    new = photos.create_folder('New_folder')
    print(root.show())

    ott = new.create_folder('123')
    file = ott.create_file('new_text.txt')
    file.edit('HELLO WORLD!!!!!!')
    print(str(root.size()) + ' bytes\n')
    print(root.show())

    print('\nNow moving in another directory\n')
    ott.move(my)
    print(root.show())

    print('All: ' + str(root.size()) + ' bytes\n')
    print('new_text: ' + str(file.size()) + ' bytes\n')
    ott.delete(file)
    print('Now deleting this file')
    print(root.show())
    print('All: ' + str(root.size()) + ' bytes\n')


if __name__ == '__main__':

    demo()

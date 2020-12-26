from abc import ABC, abstractmethod


class FileSystem(ABC):

    pass


class Directory(FileSystem):
    pass


class File(FileSystem):

    def __init__(self):


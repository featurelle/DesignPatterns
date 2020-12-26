from abc import ABC, abstractmethod


class FileSystem(ABC):

    def op(self):
        raise NotImplementedError


class Directory(FileSystem):
    pass


class File(FileSystem):

    def __init__(self):


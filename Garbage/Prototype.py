from __future__ import annotations
from abc import ABC, abstractmethod


class Cloneable:

    def __new__(cls, prototype: Cloneable = None, *args, **kwargs):
        if prototype:
            clone = prototype.clone()
            for arg, val in kwargs.items():
                pass



    @abstractmethod
    def clone(self, obj_):
        pass


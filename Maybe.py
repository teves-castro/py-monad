from typing import Callable, TypeVar

from Monad import Monad

A = TypeVar("A")
B = TypeVar("B")


class Maybe(Monad["Maybe", A]):
    def __init__(self, value: A):
        self.value = value

    @classmethod
    def unit(cls, value: A):
        return cls(value)

    @classmethod
    def nothing(cls):
        return cls(None)

    def is_nothing(self):
        return self.value is None

    def bind(self, f: Callable[[A], Monad["Maybe", B]]) -> Monad["Maybe", B]:
        if self.value is None:
            return Maybe[B].nothing()

        return f(self.value)

from typing import Callable, Generator, Generic, Protocol, TypeVar

from returns.primitives.hkt import Kind2

from Monad import Monad, Monad2

A = TypeVar("A")
B = TypeVar("B")
R = TypeVar("R")


class Reader(Monad2["Reader", R, A]):
    def __init__(self, run: Callable[[R], A]):
        self._run = run

    @classmethod
    def unit(cls, value: A):
        return cls(lambda deps: value)

    def bind(self, f: Callable[[A], "Reader[R, A]"]):
        return Reader[R, B](lambda deps: f(self._run(deps))._run(deps))

    def __call__(self, deps: R) -> A:
        return self._run(deps)

    @classmethod
    def ask(cls):
        return Reader[R, R](lambda deps: deps)

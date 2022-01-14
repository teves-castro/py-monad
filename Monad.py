from typing import Any, Callable, Generator, Generic, TypeVar

from returns.primitives.hkt import Kind1, Kind2, SupportsKind1, SupportsKind2, kinded

M = TypeVar("M")
A = TypeVar("A")
B = TypeVar("B")
R = TypeVar("R")


class Monad(SupportsKind1[M, A]):
    # unit :: a -> M a
    @staticmethod
    @kinded
    def unit(x):
        raise Exception("unit method needs to be implemented")

    # bind :: # M a -> (a -> M b) -> M b
    @kinded
    def bind(self, f: Callable[[A], Kind1[M, B]]) -> Kind1[M, B]:
        raise Exception("bind method needs to be implemented")

    # map :: # M a -> (a -> b) -> M b
    @kinded
    def map(self, f):
        return self.bind(lambda x: self.unit(f(x)))

    def __iter__(self) -> Generator[A, A, A]:
        raise Exception("__iter__ method needs to be implemented")


class Monad2(SupportsKind2[M, R, A]):
    # unit :: a -> M a
    @staticmethod
    @kinded
    def unit(a: A) -> Kind2[M, R, A]:
        raise Exception("unit method needs to be implemented")

    # bind :: # M a -> (a -> M b) -> M b
    @kinded
    def bind(self, f: Callable[[A], Kind2[M, R, B]]) -> Kind2[M, R, B]:
        raise Exception("bind method needs to be implemented")

    # map :: # M a -> (a -> b) -> M b
    @kinded
    def map(self, f: Callable[[A], B]):
        return self.bind(lambda x: self.unit(f(x)))

    def __iter__(self) -> Generator[A, A, A]:
        raise Exception("__iter__ method needs to be implemented")

from typing import Any

from Comprehension import monad
from Maybe import Maybe
from Reader import Reader

m1 = Maybe.unit("hello")
m1.bind(lambda x: Maybe.unit(x + " World"))


@monad(Maybe)
def f():
    m1 = [(x + y) for x in Maybe(5) for y in Maybe(6)]
    return [v1 * v2 for v1 in m1 for v2 in Maybe(v1)]


print(f())  # outputs `Just 11`


greeting = Reader[str, str].unit("hello")


def greet(n: str):
    return Reader[str, str].ask().map(lambda d: f"{n} {d}")


print(greeting.bind(greet)("World"))


@monad(Reader[str, str])
def f2():
    return [f"{n} {d}" for n in greeting for d in Reader.ask()]


print(f2()("World"))

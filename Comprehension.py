import ast
import inspect
from typing import Any, Callable, Iterable, ParamSpec, Type, TypeVar

from Monad import Monad, Monad2


class ComprehensionTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        for n in node.body:
            self.visit(n)
        node.decorator_list = []
        return node

    def visit_ListComp(self, node):
        def build_call(generators, elt):
            if generators == []:
                return ast.Call(
                    func=ast.Name(id="__unit__", ctx=ast.Load()),
                    args=[node.elt],
                    keywords=[],
                )
            else:
                first_generator, *rest = generators
                return ast.Call(
                    func=ast.Name(id="__bind__", ctx=ast.Load()),
                    args=[
                        first_generator.iter,
                        ast.Lambda(
                            args=ast.arguments(
                                args=[
                                    ast.arg(
                                        arg=first_generator.target.id, annotation=None
                                    )
                                ],
                                vararg=None,
                                kwonlyargs=[],
                                kw_defaults=[],
                                kwarg=None,
                                defaults=[],
                                posonlyargs=[],
                            ),
                            body=build_call(rest, elt),
                        ),
                    ],
                    keywords=[],
                )

        return build_call(node.generators, node.elt)


P = ParamSpec("P")
M = TypeVar("M", bound=Monad | Monad2)


def monad(cls: Type[M]):
    def decorator(f: Callable[P, Iterable[Any]]) -> Callable[P, M]:
        # first, uncompile the code into an ast
        source = inspect.getsource(f)
        tree = ast.parse(source)

        # transform the tree -> replace list comprehension syntax with bind /
        # unit expression
        tree.body[0] = ComprehensionTransformer().visit(tree.body[0])
        ast.fix_missing_locations(tree)

        # recompile itÎ
        code = compile(tree, "", "exec")
        globs = {
            **f.__globals__,
            "__unit__": cls.unit,
            "__bind__": cls.bind,
        }
        context = {}
        # exec the code: effectively replaces the former implementation of the
        # function
        exec(code, globs, context)
        return context[f.__name__]

    return decorator

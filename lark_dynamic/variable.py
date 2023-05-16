from typing import Callable, Iterable

from .constants import ContextType
from .token import Renderable, Token


class Variable(Token):
    def __init__(self, callback: Callable[[ContextType], Renderable]):
        self.callback = callback

    def render(self, context: ContextType) -> Iterable[str]:
        yield from Token.render_str(self.callback(context), context)

    def repr_children(self) -> str:
        return str(self.callback.__doc__ if self.callback.__doc__ else self.callback)


class BoolVariable(Variable):
    def __init__(
        self, callback: Callable[[bool], Renderable], key: str, default: bool = False
    ):
        self.callback = lambda context: callback(bool(context.get(key, default)))


def makeBoolVariable(
    key: str, true: Renderable, false: Renderable, default: bool = False
) -> BoolVariable:
    return BoolVariable(lambda value: true if value else false, key, default)

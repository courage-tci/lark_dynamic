from __future__ import annotations

from typing import Iterable

from lark_dynamic.utils import render_all, separated, wrap
from .constants import ContextType
from .token import Renderable, Token


class Combinator(Token):
    def __init__(self, *children: Renderable):
        self.children = children

    def repr_children(self) -> str:
        return "\n".join(map(repr, self.children))


class PostfixCombinator(Combinator):
    postfix: str

    def render(self, context: ContextType) -> Iterable[str]:
        yield from Group(*self.children).render(context)
        yield self.postfix


class Some(PostfixCombinator):
    postfix = "*"


class Many(PostfixCombinator):
    postfix = "+"


class Maybe(PostfixCombinator):
    postfix = "?"


class Optional(Combinator):
    def render(self, context: ContextType) -> Iterable[str]:
        yield from wrap(
            "[]",
            separated(render_all(self.children, context), " "),
        )


class Group(Combinator):
    def render(self, context: ContextType) -> Iterable[str]:
        yield from wrap(
            "()",
            separated(render_all(self.children, context), " "),
        )


class Option(Combinator):
    def render(self, context: ContextType) -> Iterable[str]:
        yield from separated(render_all(self.children, context), " | ")


def OptionG(*children: Renderable) -> Group:
    return Group(Option(*children))


def ManySeparated(sep: Renderable, token: Renderable) -> Group:
    return Group(token, Many(sep, token))


def SomeSeparated(sep: Renderable, token: Renderable) -> Group:
    return Group(token, Some(sep, token))


# aliases
class Star(Some):
    pass


class Plus(Many):
    pass


class QuestionMark(Maybe):
    pass


class Brackets(Optional):
    pass


class Parens(Group):
    pass


class Repeat(Token):
    def __init__(
        self,
        content: Renderable,
        number_or_range: Range | int | list[int] | tuple[int, int],
    ):
        self.content = content
        self.number_or_range = number_or_range

    def render(self, context: ContextType) -> Iterable[str]:
        yield from Group(self.content).render(context)
        yield " ~ "
        yield from self.render_range(context)

    def render_range(self, context: ContextType) -> Iterable[str]:
        if not self.number_or_range:
            raise ValueError("Cannot create a range of 0 occurences")

        if isinstance(self.number_or_range, (list, tuple)):
            if len(self.number_or_range) == 2:
                yield from Range(*self.number_or_range).render(context)
                return

            yield str(self.number_or_range[-1])
            return

        if isinstance(self.number_or_range, Range):
            yield from self.number_or_range.render(context)
            return

        yield str(self.number_or_range)

    def repr_children(self) -> str:
        context: ContextType = {}
        return "".join([repr(self.content), " ~ ", *self.render_range(context)])


class Range(Token):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def render(self, context: ContextType) -> Iterable[str]:
        yield str(self.start)
        yield ".."
        yield str(self.end)

    def repr_children(self) -> str:
        return "\n".join(map(repr, [self.start, self.end]))

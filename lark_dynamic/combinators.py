from __future__ import annotations

from typing import Iterable
from .constants import ContextType
from .token import Renderable, Token


class Combinator(Token):
    def __init__(self, *children: Renderable):
        self.children = children

    def repr_children(self) -> str:
        return "\n".join(map(repr, self.children))


class Some(Combinator):
    def render(self, context: ContextType) -> Iterable[str]:
        yield from Group(*self.children).render(context)
        yield "*"


class Many(Combinator):
    def render(self, context: ContextType) -> Iterable[str]:
        yield from Group(*self.children).render(context)
        yield "+"


class Maybe(Combinator):
    def render(self, context: ContextType) -> Iterable[str]:
        yield from Group(*self.children).render(context)
        yield "?"


class Optional(Combinator):
    def render(self, context: ContextType) -> Iterable[str]:
        yield "["
        yield " "
        for child in self.children:
            yield from Token.render_str(child, context)
            yield " "
        yield "]"


class Group(Combinator):
    def render(self, context: ContextType) -> Iterable[str]:
        yield "("
        yield " "
        for child in self.children:
            yield from Token.render_str(child, context)
            yield " "
        yield ")"


class Option(Combinator):
    def render(self, context: ContextType) -> Iterable[str]:
        for child in self.children[:-1]:
            yield from Token.render_str(child, context)
            yield " | "
        yield from Token.render_str(self.children[-1], context)


class OptionG(Combinator):
    def render(self, context: ContextType) -> Iterable[str]:
        yield "("
        for child in self.children[:-1]:
            yield from Token.render_str(child, context)
            yield " | "
        yield from Token.render_str(self.children[-1], context)
        yield ")"


class ManySeparated(Combinator):
    def __init__(self, sep: Renderable, token: Renderable):
        self.sep = sep
        self.token = token

    def render(self, context: ContextType) -> Iterable[str]:
        yield "("
        yield " "
        yield from Token.render_str(self.token, context)
        yield " "
        yield from Group(self.sep, self.token).render(context)
        yield "+"
        yield " "
        yield ")"

    def repr_children(self) -> str:
        return "".join([repr(self.token), " (", '","', repr(self.token), ")*"])


class SomeSeparated(Combinator):
    def __init__(self, sep: Renderable, token: Renderable):
        self.sep = sep
        self.token = token

    def render(self, context: ContextType) -> Iterable[str]:
        yield "("
        yield " "
        yield from Token.render_str(self.token, context)
        yield " "
        yield from Group(self.sep, self.token).render(context)
        yield "*"
        yield " "
        yield ")"

    def repr_children(self) -> str:
        return "".join([repr(self.token), " (", repr(self.sep), repr(self.token), ")*"])


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

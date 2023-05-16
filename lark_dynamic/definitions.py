from __future__ import annotations

from typing import Iterable, Sequence

from .utils import add_tab, comma_separated, render_all, spaced, wrap
from .constants import ContextType
from .token import Renderable, Token
from .combinators import Group


class Definition(Token):
    def __init__(
        self, name: str, tokens: Renderable, modifier: str = "", priority: int = 1
    ):
        self.name = name
        if not isinstance(tokens, tuple):
            tokens = (tokens,)
        self.tokens = tokens
        self.modifier = modifier
        self.priority = priority

    def render(self, context: ContextType) -> Iterable[str]:
        yield self.modifier
        yield self.name
        if self.priority != 1:
            yield "."
            yield str(self.priority)
        yield ": "

        yield from spaced(render_all(self.tokens, context))

    def repr_children(self) -> str:
        return "\n".join(map(repr, self.tokens))


class RuleDef(Definition):
    pass


class TerminalDef(Definition):
    pass


class DirectiveDef(Definition):
    def __init__(self, name: str, content: Token | str):
        self.name = name
        self.content = content

    def render(self, context: ContextType) -> Iterable[str]:
        yield "%"
        yield self.name
        yield " "
        if isinstance(self.content, Token):
            yield from self.content.render(context)
        else:
            yield self.content

    def repr_children(self) -> str:
        return repr(self.content)


class TemplateDef(Definition):
    def __init__(
        self,
        name: str,
        args: Renderable,
        tokens: tuple[Renderable, ...],
        modifier: str = "",
    ):
        self.name = name
        self.args = args
        self.tokens = tokens
        self.modifier = modifier

    def render(self, context: ContextType) -> Iterable[str]:
        yield self.modifier
        yield self.name

        args: Sequence[Renderable]

        if isinstance(self.args, Group):
            args = self.args.children[:]
        elif isinstance(self.args, (tuple, list)):
            args = self.args[:]
        else:
            args = (self.args,)

        yield from wrap(
            "{}",
            comma_separated(render_all(args, context)),
        )

        yield ": "

        yield from spaced(render_all(self.tokens, context))


class MetaAlias(type):
    def __getattr__(self, attr: str) -> Alias:
        return Alias(attr, ())


class Alias(Token, metaclass=MetaAlias):
    def __init__(self, name: str, tokens: tuple[Renderable, ...]):
        self.name = name
        self.tokens = tokens

    def __call__(self, *tokens: Renderable) -> Alias:
        return Alias(self.name, tokens)

    def render(self, context: ContextType) -> Iterable[str]:
        yield from spaced(render_all(self.tokens, context))
        yield " -> "
        yield self.name

    def __repr__(self) -> str:
        return f"{self.get_name()}:{self.name}({add_tab(self.repr_children())})"

    def repr_children(self) -> str:
        return "\n".join(map(repr, self.tokens))

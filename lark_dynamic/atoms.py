from __future__ import annotations
from typing import Iterable
import warnings

from .utils import comma_separated
from .constants import ContextType
from .token import Renderable, Token


class Literal(Token):
    def __init__(self, string: str, flags: str = ""):
        self.string = string
        self.flags = flags

    def render(self, context: ContextType) -> Iterable[str]:
        string = self.string.replace('"', '\\"')
        yield f'"{string}"'
        if self.flags:
            yield self.flags

    def __getattr__(self, attr: str) -> Literal:
        return Literal(self.string, self.flags + attr)

    def repr_children(self) -> str:
        context: ContextType = {}
        return "".join(self.render(context))


class RegExp(Token):
    def __init__(self, regexp: str, flags: str = ""):
        self.regexp = regexp
        self.flags = flags

    def render(self, context: ContextType) -> Iterable[str]:
        yield f"/{self.regexp}/{self.flags}"

    def __getattr__(self, attr: str) -> RegExp:
        return RegExp(self.regexp, self.flags + attr)

    def repr_children(self) -> str:
        context: ContextType = {}
        return "".join(self.render(context))


class Regexp(RegExp):
    pass


class Prerendered(Token):
    def __init__(self, string: str):
        self.string = string

    def render(self, context: ContextType) -> Iterable[str]:
        yield self.string

    def repr_children(self) -> str:
        return self.string


class Rule(Prerendered):
    def __init__(self, string: str, grammar: Grammar):
        self.string = string
        self.grammar = grammar

    def __getitem__(self, item: Renderable) -> Template:
        if not isinstance(item, tuple):
            item = (item,)
        return Template(self.string, item)

    def __setitem__(
        self, item: Renderable | int, value: Renderable
    ) -> RuleDef | TemplateDef:
        if isinstance(item, int):
            return self.grammar.make_rule(self.string, value, "", item)
        return self.grammar.make_template(self.string, item, value)


class Terminal(Prerendered):
    def __init__(self, string: str, grammar: Grammar):
        self.string = string
        self.grammar = grammar

    def __getitem__(self, item: Renderable) -> Template:
        warnings.warn(
            f"You are trying to make a terminal template: {self.string}[{item}]`, this won't work"
        )
        if not isinstance(item, tuple):
            item = (item,)
        return Template(self.string, item)

    def __setitem__(self, item: Renderable | int, value: Renderable) -> TerminalDef:
        if isinstance(item, int):
            return self.grammar.make_terminal(self.string, value, "", item)
        raise TypeError(
            f"Priority must be an integer, not {type(item).__name__}. If you're trying to create a template, use a rule (lowercase name), not a terminal."
        )


class Template(Token):
    def __init__(self, name: str, args: tuple[Renderable, ...]):
        self.name = name
        self.args = args

    def render(self, context: ContextType) -> Iterable[str]:
        yield self.name
        yield "{"
        yield from comma_separated(
            [Token.render_str(arg, context) for arg in self.args]
        )
        yield "}"

    def repr_children(self) -> str:
        return "\n".join(map(repr, self.args))


Empty = Prerendered("")


from .grammar import Grammar
from .definitions import RuleDef, TemplateDef, TerminalDef

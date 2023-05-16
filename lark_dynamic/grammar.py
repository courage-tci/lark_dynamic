from __future__ import annotations
from typing import Any, Iterable


class Grammar:
    def __init__(self) -> None:
        self.__rules__: dict[str, RuleDef] = {}
        self.__terminals__: dict[str, TerminalDef] = {}
        self.__directives__: list[DirectiveDef] = []
        self.__templates__: dict[str, TemplateDef] = {}
        self.__wrapper__: GrammarWrapper = GrammarWrapper(self)

    def generate(self, **context: Any) -> str:
        return "".join(self.build_grammar(context)).strip()

    def build_grammar(self, context: ContextType) -> Iterable[str]:
        for terminal in self.__terminals__.values():
            yield from terminal.render(context)
            yield "\n"
        yield "\n"
        for rule in self.__rules__.values():
            yield from rule.render(context)
            yield "\n"
        yield "\n"
        for directive in self.__directives__:
            yield from directive.render(context)
            yield "\n"
        yield "\n"
        for template in self.__templates__.values():
            yield from template.render(context)
            yield "\n"
        yield "\n"

    def make_rule(
        self,
        name: str,
        tokens: Renderable | Modifier,
        modifier: str = "",
        priority: int = 1,
        replace: bool = False,
    ) -> RuleDef:
        if not is_rule(name):
            raise ValueError(
                f"Invalid rule name: '{name}'. Rule names must only contain chars [a-z0-9_] and cannot start with a digit"
            )
        if name in self.__rules__ and not replace:
            raise NameError(f"Rule '{name}' already exists")

        if isinstance(tokens, Modifier):
            modifier = tokens.type
            tokens = tokens.tokens

        ruledef = RuleDef(name, tokens, modifier, priority)
        self.__rules__[name] = ruledef
        return ruledef

    def make_terminal(
        self,
        name: str,
        tokens: Renderable | Modifier,
        modifier: str = "",
        priority: int = 1,
    ) -> TerminalDef:
        if not is_term(name):
            raise ValueError(
                f"Invalid terminal name: '{name}'. Terminal names only contain chars [A-Z0-9_] and cannot start with a digit"
            )
        if name in self.__terminals__:
            raise NameError(f"Terminal '{name}' already exists")

        if isinstance(tokens, Modifier):
            modifier = tokens.type
            tokens = tokens.tokens

        termdef = TerminalDef(name, tokens, modifier, priority)
        self.__terminals__[name] = termdef
        return termdef

    def make_directive(self, name: str, content: Token | str) -> DirectiveDef:
        directivedef = DirectiveDef(name, content)
        self.__directives__.append(directivedef)
        return directivedef

    def make_template(
        self,
        name: str,
        args: Renderable,
        tokens: Renderable | Modifier,
        modifier: str = "",
    ) -> TemplateDef:
        if isinstance(tokens, Modifier):
            modifier = tokens.type
            tokens = tokens.tokens

        if not isinstance(tokens, tuple):
            tokens = (tokens,)

        templatedef = TemplateDef(name, args, tokens, modifier)
        self.__templates__[name] = templatedef
        return templatedef

    def __setattr__(self, attr: str, value: Renderable | Modifier) -> None:
        if not attr.startswith("__"):
            if is_rule(attr):
                self.make_rule(attr, value)
                return
            if is_term(attr):
                self.make_terminal(attr, value)
                return
        super().__setattr__(attr, value)

    def __getattr__(self, attr: str) -> Rule | Terminal:
        if is_rule(attr):
            return Rule(attr, self)
        if is_term(attr):
            return Terminal(attr, self)
        raise AttributeError(attr)

    def __repr__(self) -> str:
        return "\n\n".join(
            [
                *[repr(rule) for rule in self.__rules__.values()],
                *[repr(term) for term in self.__terminals__.values()],
                *[repr(directive) for directive in self.__directives__],
            ]
        )

    def use_wrapper(self) -> GrammarWrapper:
        return self.__wrapper__


class GrammarWrapper:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    def get_def(self, key: str) -> RuleDef | TerminalDef | TemplateDef | None:
        return self.rules.get(key) or self.terminals.get(key) or self.templates.get(key)

    @property
    def rules(self) -> dict[str, RuleDef]:
        return self.grammar.__rules__

    @property
    def terminals(self) -> dict[str, TerminalDef]:
        return self.grammar.__terminals__

    @property
    def templates(self) -> dict[str, TemplateDef]:
        return self.grammar.__templates__

    @property
    def directives(self) -> list[DirectiveDef]:
        return self.grammar.__directives__

    def extend(self, key: str, *alternatives: Renderable) -> None:
        definition = self.get_def(key)

        if not definition:
            raise AttributeError(f"No definition by the name '{key}'")

        definition.tokens = (Option(*definition.tokens, *alternatives),)

    def replace(self, key: str, tokens: Renderable) -> None:
        definition = self.get_def(key)
        if not definition:
            raise AttributeError(f"No definition by the name '{key}'")

        if not isinstance(tokens, tuple):
            tokens = (tokens,)

        definition.tokens = tokens

    def edit(
        self, key: str, modifier: Modifier | None = None, priority: int | None = None
    ) -> None:
        definition = self.get_def(key)

        if not definition:
            raise AttributeError(f"No definition by the name '{key}'")

        if modifier is not None:
            definition.modifier = modifier.type

        if priority is not None:
            definition.priority = priority


from .constants import ContextType
from .utils import is_rule, is_term
from .modifier import Modifier
from .token import Renderable, Token
from .definitions import DirectiveDef, RuleDef, TemplateDef, TerminalDef
from .combinators import Option
from .atoms import Rule, Terminal

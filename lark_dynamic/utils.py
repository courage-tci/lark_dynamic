from __future__ import annotations
from typing import Iterable, Sequence


def wrap(parens: Sequence[str], content: Iterable[str]) -> Iterable[str]:
    yield parens[0]
    yield from content
    yield parens[1]


def separated(parts: Iterable[Iterable[str]], sep: str) -> Iterable[str]:
    is_first = True
    for part in parts:
        if not is_first:
            yield sep
        else:
            is_first = False
        yield from part


def spaced(parts: Iterable[Iterable[str]]) -> Iterable[str]:
    yield from separated(parts, " ")


def comma_separated(parts: Iterable[Iterable[str]]) -> Iterable[str]:
    yield from separated(parts, ", ")


def render_all(
    renderables: Sequence[Renderable], context: ContextType
) -> Iterable[Iterable[str]]:
    for renderable in renderables:
        # it is intentionally not `yield from`
        yield Token.render_str(renderable, context)


def add_tab(text: str) -> str:
    return ("\n" + text).replace("\n", "\n    ") + "\n" if text else ""


def is_rule(s: str) -> bool:
    return s.islower() and s.isidentifier()


def is_term(s: str) -> bool:
    return s.isupper() and s.isidentifier()


from .token import Renderable, Token
from .constants import ContextType

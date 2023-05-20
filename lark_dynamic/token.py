from __future__ import annotations
from typing import Iterable, Union
from codecs import getencoder

from .constants import ContextType
from .utils import add_tab


Renderable = Union[str, "list[Renderable]", "tuple[Renderable, ...]", "Token"]
str_encoder = getencoder("unicode_escape")


class Token:
    def get_name(self) -> str:
        return self.__class__.__name__

    def repr_children(self) -> str:
        return ""

    def __repr__(self) -> str:
        return f"{self.get_name()}({add_tab(self.repr_children())})"

    def render(self, context: ContextType) -> Iterable[str]:
        return NotImplemented

    @staticmethod
    def render_str(token: Renderable, context: ContextType) -> Iterable[str]:
        if isinstance(token, tuple):
            yield from Group(*token).render(context)
        elif isinstance(token, list):
            yield from Optional(*token).render(context)
        elif isinstance(token, str):
            str_escaped = str_encoder(token)[0].decode("utf-8")

            yield '"'
            yield str_escaped
            yield '"'
        else:
            yield from token.render(context)

    def __or__(self, other: Renderable) -> Option:
        return Option(self, other)

    def __ror__(self, other: Renderable) -> Option:
        return Option(other, self)


from .combinators import Group, Option, Optional

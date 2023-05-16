from __future__ import annotations


class Modifier:
    INLINE: Modifier
    INLINE_SINGLE: Modifier
    KEEP_TERMINALS: Modifier
    ANONYMOUS: Modifier

    def __init__(self, type_: str, *tokens: Renderable):
        self.type = type_
        self.tokens = tokens

    def __call__(self, *tokens: Renderable) -> Modifier:
        return Modifier(self.type, *tokens)


# for rules
Modifier.INLINE = Modifier("_")
Modifier.INLINE_SINGLE = Modifier("?")
Modifier.KEEP_TERMINALS = Modifier("!")
# for terminals
Modifier.ANONYMOUS = Modifier("_")


from .token import Renderable

from typing import Iterable


def comma_separated(parts: Iterable[Iterable[str]]) -> Iterable[str]:
    is_first = True
    for part in parts:
        if not is_first:
            yield ", "
        else:
            is_first = False
        yield from part


def add_tab(text: str) -> str:
    return ("\n" + text).replace("\n", "\n    ") + "\n" if text else ""


def is_rule(s: str) -> bool:
    return s.islower() and s.isidentifier()


def is_term(s: str) -> bool:
    return s.isupper() and s.isidentifier()

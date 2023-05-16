from lark_dynamic.constants import ContextType
from lark_dynamic.grammar import Grammar
from lark_dynamic.token import Renderable, Token


def render_token(token: Renderable, context: ContextType | None = None) -> str:
    return "".join(Token.render_str(token, context or {}))


dummy_grammar = Grammar()

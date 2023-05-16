from lark_dynamic.constants import ContextType
from lark_dynamic.token import Renderable
from lark_dynamic.variable import BoolVariable, Variable, makeBoolVariable

from token_utils import render_token


class TestClass:
    def test_variable(self):
        def callback(context: ContextType) -> Renderable:
            return context["a"]

        variable = Variable(callback)

        assert render_token(variable, {"a": "b"}) == '"b"'
        assert render_token(variable, {"a": "c"}) == '"c"'

        # don't need to test actually, this is not used at the moment and is not a public API
        str(variable)

    def test_bool_variable(self):
        def callback(bool_key: bool) -> Renderable:
            if bool_key is True:
                return "yes"
            return "no"

        bool_variable = BoolVariable(callback, "what")

        assert render_token(bool_variable) == '"no"'
        assert render_token(bool_variable, {"what": True}) == '"yes"'
        assert render_token(bool_variable, {"what": False}) == '"no"'

        simple_bool_variable = makeBoolVariable("what", "yes", "no")

        assert render_token(simple_bool_variable) == '"no"'
        assert render_token(simple_bool_variable, {"what": True}) == '"yes"'
        assert render_token(simple_bool_variable, {"what": False}) == '"no"'

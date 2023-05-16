from __future__ import annotations

from lark_dynamic import Literal, RegExp
from lark_dynamic.atoms import Prerendered, Rule, Terminal
from lark_dynamic.constants import ContextType
from lark_dynamic.definitions import TemplateDef
from lark_dynamic.token import Token
from token_utils import render_token, dummy_grammar

import pytest


class TestClass:
    def test_literal(self):
        assert render_token(Literal("abcd")) == '"abcd"'
        assert render_token(Literal("abcd").i) == '"abcd"i'
        assert render_token(Literal("abcd", "i")) == '"abcd"i'

        str(Literal("abcd"))

    def test_regexp(self):
        assert render_token(RegExp("abcd")) == "/abcd/"
        assert render_token(RegExp("abcd").i) == "/abcd/i"
        assert render_token(RegExp("abcd", "i")) == "/abcd/i"

        str(RegExp("abcd"))

    def test_prerendered(self):
        assert render_token(Prerendered("abcd")) == "abcd"

    def test_rule(self):
        rule = Rule("test_rule", dummy_grammar)

        assert render_token(rule) == "test_rule"

        rule[10] = "123"

        ruledef = dummy_grammar.use_wrapper().get_def("test_rule")

        assert ruledef
        assert ruledef.priority == 10

        rule2 = Rule("test_rule2", dummy_grammar)

        rule2["a"] = "123"

        templatedef = dummy_grammar.use_wrapper().get_def("test_rule2")

        assert templatedef
        assert isinstance(templatedef, TemplateDef)

        assert templatedef.args == "a"

        template = rule["a"]
        template2 = rule["a", "b"]

        assert render_token(template) == 'test_rule{"a"}'
        assert render_token(template2) == 'test_rule{"a", "b"}'

        str(rule)
        str(template)

    def test_terminal(self):
        term = Terminal("TEST_TERMINAL", dummy_grammar)

        assert render_token(term) == "TEST_TERMINAL"

        term[10] = "123"

        ruledef = dummy_grammar.use_wrapper().get_def("TEST_TERMINAL")

        assert ruledef
        assert ruledef.priority == 10

        term2 = Terminal("TEST_TERMINAL2", dummy_grammar)

        with pytest.raises(TypeError):
            term2["a"] = "123"

        assert not dummy_grammar.use_wrapper().get_def("TEST_TERMINAL2")

    def test_token(self):
        token = Token()
        context: ContextType = {}

        assert token.render(context) == NotImplemented

        str(token)

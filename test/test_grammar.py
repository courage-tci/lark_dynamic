from __future__ import annotations

from lark_dynamic import Literal, RegExp
from lark_dynamic.atoms import Prerendered, Rule, Terminal
from lark_dynamic.definitions import RuleDef, TemplateDef
from lark_dynamic.grammar import Grammar
from lark_dynamic.modifier import Modifier
from token_utils import render_token, dummy_grammar

import pytest

#


class TestClass:
    def test_make_rule(self):
        ruledef = dummy_grammar.make_rule("make_rule_stuff", "a")

        assert ruledef.tokens == ("a",)
        assert ruledef.name == "make_rule_stuff"

        with pytest.raises(ValueError):
            dummy_grammar.make_rule("WHAT", "a")

        with pytest.raises(NameError):
            dummy_grammar.make_rule("make_rule_stuff", "a")

    def test_make_terminal(self):
        ruledef = dummy_grammar.make_terminal("MAKE_TERMINAL_STUFF", "a")

        assert ruledef.tokens == ("a",)
        assert ruledef.name == "MAKE_TERMINAL_STUFF"

        with pytest.raises(ValueError):
            dummy_grammar.make_terminal("what", "a")

        with pytest.raises(NameError):
            dummy_grammar.make_terminal("MAKE_TERMINAL_STUFF", "a")

        assert render_token(dummy_grammar.MAKE_TERMINAL_STUFF) == "MAKE_TERMINAL_STUFF"

        with pytest.raises(AttributeError):
            dummy_grammar.WhAtS_wRoNg

    def test_make_template(self):
        templatedef = dummy_grammar.make_template("MAKE_TEMPLATE_STUFF", "a", "b")

        assert templatedef.args == "a"
        assert templatedef.tokens == ("b",)
        assert templatedef.name == "MAKE_TEMPLATE_STUFF"
        assert templatedef.modifier == ""

        templatedef_modified = dummy_grammar.make_template(
            "MAKE_TEMPLATE_STUFF_MOD", "a", Modifier.INLINE_SINGLE("b")
        )

        assert templatedef_modified.args == "a"
        assert templatedef_modified.tokens == ("b",)
        assert templatedef_modified.name == "MAKE_TEMPLATE_STUFF_MOD"
        assert templatedef_modified.modifier == "?"

    def test_build(self):
        g = Grammar()
        g.rule1 = "a"
        g.TERM1 = "b"
        g.template1[g.c] = "d"
        g.modified = Modifier.INLINE_SINGLE("e")
        g.MODIFIED = Modifier.INLINE_SINGLE("j")
        g.make_directive("f", "g")
        g.make_directive("h", Literal("i"))
        assert list(filter(None, g.generate().split("\n"))) == [
            'TERM1: "b"',
            '?MODIFIED: "j"',
            'rule1: "a"',
            '?modified: "e"',
            "%f g",
            '%h "i"',
            'template1{c}: "d"',
        ]

    def test_wrapper(self):
        wrapper = dummy_grammar.use_wrapper()

        dummy_grammar.wrapper_test = "b"

        definition = wrapper.get_def("wrapper_test")

        assert isinstance(definition, RuleDef)

        assert definition.name == "wrapper_test"
        assert definition.modifier == ""
        assert definition.priority == 1
        assert definition.tokens == ("b",)

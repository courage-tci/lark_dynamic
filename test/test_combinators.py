from __future__ import annotations

from lark_dynamic import Literal
from lark_dynamic.combinators import (
    Group,
    Many,
    ManySeparated,
    Maybe,
    Option,
    OptionG,
    Optional,
    Range,
    Repeat,
    Some,
    SomeSeparated,
)
from lark_dynamic.token import Renderable
from token_utils import render_token

import pytest


class TestClass:
    def test_option(self):
        option_explicit = Option("a", "b")
        option_operator_reversed = "a" | Literal("b")
        option_operator = Literal("a") | "b"
        option_grouped = OptionG("a", "b")

        assert (
            render_token(option_explicit)
            == render_token(option_operator)
            == render_token(option_operator_reversed)
            == '"a" | "b"'
        )

        assert render_token(option_grouped) == '("a" | "b")'

    def test_generic_combinators(self):
        some = Some("a")
        many = Many("b")
        maybe = Maybe("c")

        assert render_token(some) == '("a")*'
        assert render_token(many) == '("b")+'
        assert render_token(maybe) == '("c")?'

        str(some)
        str(many)
        str(maybe)

    def test_separated_combinators(self):
        some = SomeSeparated(",", "a")
        many = ManySeparated(",", "b")

        assert render_token(some) == '("a" ("," "a")*)'
        assert render_token(many) == '("b" ("," "b")+)'

        str(some)
        str(many)

    def test_optional(self):
        optional_explicit = Optional("a", "b")
        optional_literal: list[Renderable] = ["a", "b"]

        assert (
            render_token(optional_explicit)
            == render_token(optional_literal)
            == '["a" "b"]'
        )

    def test_repeat(self):
        range_ = Range(1, 4)

        assert render_token(range_) == "1..4"
        assert render_token(Repeat("a", range_)) == '("a") ~ 1..4'
        assert render_token(Repeat("a", (1, 4))) == '("a") ~ 1..4'
        assert render_token(Repeat("a", [1, 4])) == '("a") ~ 1..4'
        assert render_token(Repeat("a", 4)) == '("a") ~ 4'
        assert render_token(Repeat("a", [4])) == '("a") ~ 4'

        with pytest.raises(ValueError):
            render_token(Repeat("a", 0))

        str(range_)
        str(Repeat("a", range_))

    def test_group(self):
        group_explicit = Group("a", "b")
        group_literal = "a", "b"

        assert (
            render_token(group_explicit) == render_token(group_literal) == '("a" "b")'
        )

from emojify_cli.emoji import emojify, expand_macros, Token

BASE_CFG = {
    "compact": False,
    "normalize": True,
    "case": False,
    "mappings": {
        "letters": {
            "a": ":regional_indicator_a:",
            "b": ":regional_indicator_b:",
            "A": ":a:",
            "B": ":b:"
        },
        "numbers": {
            "1": ":one:"
        },
        "symbols": {
            "!": ":exclamation:"
        },
        "macro": {
            "000": "#",
            "001": ":fire:"
        }
    }
}


def test_letters():
    assert emojify("ab", BASE_CFG) == (
        ":regional_indicator_a: :regional_indicator_b:"
    )


def test_letters_case():
    cfg = dict(BASE_CFG)
    cfg["case"] = True
    assert emojify("aA", cfg) == (
        ":regional_indicator_a: :a:"
    )


def test_letters_icase():
    cfg = dict(BASE_CFG)
    cfg["case"] = False
    assert emojify("aA", cfg) == (
        ":regional_indicator_a: :regional_indicator_a:"
    )


def test_numbers():
    assert emojify("a1", BASE_CFG) == (
        ":regional_indicator_a: :one:"
    )


def test_symbols():
    assert emojify("a!", BASE_CFG) == (
        ":regional_indicator_a: :exclamation:"
    )


def test_macro_expansion():
    assert emojify("hi #001", BASE_CFG) == (
        "h i   :fire:"
    )


def test_macro_escape():
    assert emojify("#000", BASE_CFG) == "#"


def test_compact_mode():
    cfg = dict(BASE_CFG)
    cfg["compact"] = True
    assert emojify("a1!", cfg) == (
        ":regional_indicator_a::one::exclamation:"
    )


def test_expand_macros_basic():
    macros = {"001": ":fire:"}
    tokens = list(expand_macros("a#001b", macros))

    assert tokens == [
        Token("a", False),
        Token(":fire:", True),
        Token("b", False),
    ]


def test_expand_macros_failed():
    macros = {"001": ":fire:"}
    tokens = list(expand_macros("#001#999#abc", macros))

    assert tokens == [
        Token(":fire:", True),
        Token("#", False),
        Token("9", False),
        Token("9", False),
        Token("9", False),
        Token("#", False),
        Token("a", False),
        Token("b", False),
        Token("c", False)
    ]


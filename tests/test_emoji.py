from emojify_cli.emoji import emojify

BASE_CFG = {
    "compact": False,
    "normalize": True,
    "mappings": {
        "letters": {
            "a": ":regional_indicator_a:",
            "b": ":regional_indicator_b:"
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


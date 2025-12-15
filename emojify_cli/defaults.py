# emojify_cli/defaults.py

LETTER_EMOJI = {ch: f":regional_indicator_{ch}:" for ch in "abcdefghijklmnopqrstuvwxyz"}

NUMBER_EMOJI = {
    "0": ":zero:",
    "1": ":one:",
    "2": ":two:",
    "3": ":three:",
    "4": ":four:",
    "5": ":five:",
    "6": ":six:",
    "7": ":seven:",
    "8": ":eight:",
    "9": ":nine:",
}

SYMBOL_EMOJI = {
    "!": ":exclamation:",
    "?": ":question:",
    "*": ":asterisk:",
    "+": ":heavy_plus_sign:",
    "-": ":heavy_minus_sign:",
    "/": ":heavy_division_sign:"
}

DEFAULT_CONFIG = {
    "compact": False,
    "normalize": True,
    "case": 'off',
    "mappings": {
        "letters": LETTER_EMOJI,
        "numbers": NUMBER_EMOJI,
        "symbols": SYMBOL_EMOJI,
        "macro": {
            "000": "#"
        }
    }
}


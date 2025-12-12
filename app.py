#!/usr/bin/env python3
import unicodedata

LETTER_EMOJI = {
    ch: f":regional_indicator_{ch}:" for ch in "abcdefghijklmnopqrstuvwxyz"
}

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
    "/": ":heavy_division_sign:",
}

def normalize_ascii(s: str) -> str:
    """Remove accents while keeping ASCII letters."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )

def emojify(msg: str, compact: bool = False) -> str:
    msg = normalize_ascii(msg)
    out = []

    for ch in msg.lower():
        if ch in LETTER_EMOJI:
            out.append(LETTER_EMOJI[ch])
        elif ch in NUMBER_EMOJI:
            out.append(NUMBER_EMOJI[ch])
        elif ch in SYMBOL_EMOJI:
            out.append(SYMBOL_EMOJI[ch])
        else:
            out.append(ch)

    if compact:
        return "".join(out)  # no spaces

    return " ".join(out)

if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    compact = False

    # detect --compact or -c
    if "--compact" in args:
        compact = True
        args.remove("--compact")
    if "-c" in args:
        compact = True
        args.remove("-c")

    if args:
        message = " ".join(args)
    else:
        message = input("Message: ")

    print(emojify(message, compact=compact))


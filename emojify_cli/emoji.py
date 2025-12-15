# emojify_cli/emoji.py

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Mapping
import unicodedata

@dataclass(slots=True)
class Token:
    value: str
    is_macro: bool

def normalize_ascii(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )

def expand_macros(msg: str, macros: Mapping[str, str]) -> Iterator[Token]:
    i = 0
    n = len(msg)

    while i < n:
        if msg[i] == "#" and i + 3 < n and msg[i+1:i+4].isdigit():
            code = msg[i+1:i+4]
            if code in macros:
                yield Token(macros[code], True)
                i += 4
                continue
        yield Token(msg[i], False)
        i += 1


def emojify(msg: str, cfg: dict) -> str:
    if cfg.get("normalize", True):
        msg = normalize_ascii(msg)

    m = cfg.get("mappings", {})
    case_mode = cfg.get("case", "off")

    letters = m.get("letters", {})
    numbers = m.get("numbers", {})
    symbols = m.get("symbols", {})

    out = []
    for token in expand_macros(msg, m.get("macro", {})):
        ch = token.value
        macro = token.is_macro

        if macro:
            out.append(ch)
            continue
        if ch.isalpha():
            key = ch

            if case_mode == "off":
                key = ch.lower()
                out.append(letters.get(key, key))

            elif case_mode == "on":
                out.append(letters.get(ch, ch))

            elif case_mode == "auto":
                if ch in letters:
                    out.append(letters[ch])
                else:
                    out.append(letters.get(ch.lower(), ch))

        elif ch in numbers:
            out.append(numbers[ch])
        elif ch in symbols:
            out.append(symbols[ch])
        else:
            out.append(ch)

    return "".join(out) if cfg.get("compact") else " ".join(out)


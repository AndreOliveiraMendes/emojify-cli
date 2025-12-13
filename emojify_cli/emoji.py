# emojify_cli/emoji.py

import unicodedata

def normalize_ascii(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def expand_macros(msg: str, macros: dict) -> list:
    out = []
    i = 0
    n = len(msg)

    while i < n:
        if msg[i] == "#" and i + 3 < n and msg[i+1:i+4].isdigit():
            code = msg[i+1:i+4]
            if code in macros:
                out.append({"item":macros[code], "macro":True})
                i += 4
                continue
        out.append({"item":msg[i], "macro":False})
        i += 1

    return out


def emojify(msg: str, cfg: dict) -> str:
    if cfg.get("normalize", True):
        msg = normalize_ascii(msg)

    m = cfg.get("mappings", {})
    msg = expand_macros(msg, m.get("macro", {}))

    letters = m.get("letters", {})
    numbers = m.get("numbers", {})
    symbols = m.get("symbols", {})

    out = []

    for packet in msg:
        ch = packet['item']
        macro = packet['macro']
        if macro:
            out.append(ch)
            continue
        key = ch.lower()
        if key in letters:
            out.append(letters[key])
        elif ch in numbers:
            out.append(numbers[ch])
        elif ch in symbols:
            out.append(symbols[ch])
        else:
            out.append(ch)

    return "".join(out) if cfg.get("compact") else " ".join(out)


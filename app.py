#!/usr/bin/env python3
import unicodedata

def normalize_ascii(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )

def to_regional_indicator(msg: str) -> str:
    msg = normalize_ascii(msg)
    res = []
    for ch in msg:
        if ch.isalpha() and 'a' <= ch.lower() <= 'z':
            res.append(f":regional_indicator_{ch.lower()}:")
        elif ch:
            res.append(ch)
        else:
            res.append('')
    return " ".join(res)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = input("Message: ")

    print(to_regional_indicator(message))

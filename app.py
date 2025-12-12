#!/usr/bin/env python3
import argparse
import json
import os
import unicodedata
import sys

# -----------------------
# Default mappings
# -----------------------

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
    "mappings": {
        "letters": LETTER_EMOJI,
        "numbers": NUMBER_EMOJI,
        "symbols": SYMBOL_EMOJI
    }
}


# -----------------------
# Config loading
# -----------------------

def load_config(path=None):
    if not path:
        path = os.path.expanduser("~/.emojify.json")

    if not os.path.exists(path):
        return {}

    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def merge_config(base, overrides):
    """Merge mapping configs recursively."""
    result = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and key in result:
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    return result


# -----------------------
# Emoji conversion
# -----------------------

def normalize_ascii(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def emojify(msg: str, cfg):
    if cfg.get("normalize", True):
        msg = normalize_ascii(msg)

    m = cfg.get("mappings", {})
    letters = m.get("letters", {})
    numbers = m.get("numbers", {})
    symbols = m.get("symbols", {})

    out = []

    for ch in msg.lower():
        if ch in letters:
            out.append(letters[ch])
        elif ch in numbers:
            out.append(numbers[ch])
        elif ch in symbols:
            out.append(symbols[ch])
        else:
            out.append(ch)

    if cfg.get("compact"):
        return "".join(out)

    return " ".join(out)


# -----------------------
# Main
# -----------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert text to Discord emoji codes.",
        add_help=False
    )

    parser.add_argument("text", nargs="*", help="Text to convert")

    parser.add_argument("-c", "--compact", action="store_true")
    parser.add_argument("--no-compact", action="store_true")
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--no-normalize", action="store_true")
    parser.add_argument("--config", help="Custom config file")
    parser.add_argument("--dump-config", action="store_true")
    parser.add_argument("-h", "--help", action="help")

    args = parser.parse_args()

    # Load config
    user_cfg = load_config(args.config)
    cfg = merge_config(DEFAULT_CONFIG, user_cfg)

    # Apply CLI overrides
    if args.compact:
        cfg["compact"] = True
    if args.no_compact:
        cfg["compact"] = False

    if args.normalize:
        cfg["normalize"] = True
    if args.no_normalize:
        cfg["normalize"] = False

    if args.dump_config:
        print(json.dumps(cfg, indent=4))
        sys.exit(0)

    # Get message
    if args.text:
        message = " ".join(args.text)
    else:
        message = input("Message: ")

    print(emojify(message, cfg))


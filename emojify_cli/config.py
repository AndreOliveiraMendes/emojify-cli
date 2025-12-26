# emojify_cli/config.py

import json
import os
import sys
from emojify_cli.util import open_editor

def load_config(path=None):
    if not path:
        path = os.path.expanduser("~/.emojify.json")

    if not os.path.exists(path):
        return {}

    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Invalid JSON config: {e}", file=sys.stderr)
        return {}


def merge_config(base, overrides):
    result = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    return result

def init_config(base):
    path = os.path.expanduser("~/.emojify.json")

    if os.path.exists(path):
        return 1, "config file already exists"

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(base, f, indent=4)
        return 0, "config file created successfully"
    except Exception as e:
        return 2, f"unable to create config file: {e}"

def edit_config():
    path = os.path.expanduser("~/.emojify.json")

    open_editor(path)

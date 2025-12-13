# emojify_cli/config.py

import json
import os
import sys

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


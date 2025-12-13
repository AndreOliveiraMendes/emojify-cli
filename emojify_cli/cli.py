# emojify_cli/cli.py

import argparse
import json
import sys

from emojify_cli import __version__
from emojify_cli.config import load_config, merge_config
from emojify_cli.defaults import DEFAULT_CONFIG
from emojify_cli.emoji import emojify


def main():
    parser = argparse.ArgumentParser(
        description="Convert text to Discord emoji codes."
    )

    parser.add_argument("text", nargs="*", help="Text to convert")

    parser.add_argument("-c", "--compact", action="store_true")
    parser.add_argument("--no-compact", action="store_true")
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--no-normalize", action="store_true")
    parser.add_argument("--config", help="Custom config file")
    parser.add_argument("--dump-config", action="store_true")

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    user_cfg = load_config(args.config)
    cfg = merge_config(DEFAULT_CONFIG, user_cfg)

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

    message = " ".join(args.text) if args.text else input("Message: ")
    print(emojify(message, cfg))


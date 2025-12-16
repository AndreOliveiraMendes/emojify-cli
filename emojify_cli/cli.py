# emojify_cli/cli.py
import argparse
import json
import sys

from emojify_cli import __version__
from emojify_cli.config import load_config, merge_config
from emojify_cli.defaults import DEFAULT_CONFIG
from emojify_cli.emoji import emojify
from enum import Enum


class CaseMode(str, Enum):
    off = "off"
    on = "on"
    auto = "auto"

def main():
    parser = argparse.ArgumentParser(
        description="Convert text to Discord emoji codes."
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    sub = parser.add_subparsers(dest="command")

    # sub comand run
    run = sub.add_parser("run", help="Convert text to emojis")

    run.add_argument("text", nargs="*", help="Text to convert")

    run.add_argument("-c", "--compact", action="store_true")
    run.add_argument("--no-compact", action="store_true")
    run.add_argument("--normalize", action="store_true")
    run.add_argument("--no-normalize", action="store_true")
    run.add_argument(
        "--case",
        choices=CaseMode,
        default=CaseMode.off,
    )

    # sub comand config
    config = sub.add_parser("config", help="Manage configuration")

    config.add_argument("--config", help="Custom config file")
    config.add_argument("--dump", action="store_true")

    args = parser.parse_args()

    # Default: behave like "run"
    if args.command is None:
        args.command = "run"

    if args.command == "run":
        user_cfg = load_config(None)
        cfg = merge_config(DEFAULT_CONFIG, user_cfg)

        if args.compact:
            cfg["compact"] = True
        if args.no_compact:
            cfg["compact"] = False

        if args.normalize:
            cfg["normalize"] = True
        if args.no_normalize:
            cfg["normalize"] = False

        cfg["case"] = args.case

        message = " ".join(args.text) if args.text else input("Message: ")
        print(emojify(message, cfg))

    elif args.command == "config":
        cfg = load_config(args.config)
        cfg = merge_config(DEFAULT_CONFIG, cfg)

        if args.dump:
            print(json.dumps(cfg, indent=4))
            sys.exit(0)


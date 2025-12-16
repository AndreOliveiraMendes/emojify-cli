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

    run.add_argument(
        "--case",
        choices=[c.value for c in CaseMode],
        default=CaseMode.off.value,
        help="control case conversion"
    )
    run.add_argument("--config", help="Custom config file (temporary)")

    # compact group
    compact_group = run.add_mutually_exclusive_group()
    compact_group.add_argument("-c", "--compact", action="store_true", help="output emojis without spaces")
    compact_group.add_argument("--no-compact", action="store_true", help="output emojis with spaces")

    # normal group
    normal_group = run.add_mutually_exclusive_group()
    normal_group.add_argument("--normalize", action="store_true", help="normalize accented characters (e.g. á → a, ç → c)")
    normal_group.add_argument("--no-normalize", action="store_true", help="disable character normalization")

    # sub comand config
    config = sub.add_parser("config", help="Manage configuration")

    config.add_argument("--config", help="Custom config file")
    config.add_argument("--dump", action="store_true", help="show current config being used")

    args = parser.parse_args()

    # Default: behave like "run"
    if args.command is None:
        args.command = "run"

    cfg = merge_config(
        DEFAULT_CONFIG,
        load_config(args.config),
    )

    if args.command == "run":

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
        if args.dump:
            print(json.dumps(cfg, indent=4))
            sys.exit(0)
        else:
            print("nothing else yet, try --dump for now")


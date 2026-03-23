#!/usr/bin/env python3
"""
todo - A simple command-line todo list manager.
"""

import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple command-line todo list manager.",
    )
    parser.add_argument("--version", action="version", version="todo 0.1.0")

    # Subcommands will be added in future branches
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = False

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()


if __name__ == "__main__":
    main()

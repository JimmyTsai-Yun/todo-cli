#!/usr/bin/env python3
"""
todo - A simple command-line todo list manager.
"""

import argparse
import json
import os
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.todo.json")


def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)


def cmd_add(args):
    todos = load_todos()
    new_id = max((t["id"] for t in todos), default=0) + 1
    todo = {
        "id": new_id,
        "task": args.task,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    todos.append(todo)
    save_todos(todos)
    print(f"Added #{new_id}: {args.task}")


def main():
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple command-line todo list manager.",
    )
    parser.add_argument("--version", action="version", version="todo 0.1.0")

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = False

    # add
    p_add = subparsers.add_parser("add", help="Add a new task")
    p_add.add_argument("task", help="Task description")
    p_add.set_defaults(func=cmd_add)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()

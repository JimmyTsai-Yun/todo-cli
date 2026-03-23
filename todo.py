#!/usr/bin/env python3
"""
todo - A simple command-line todo list manager.
"""

import argparse
import json
import os
import sys
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.todo.json")


def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(
            f"Error: {DATA_FILE} is corrupted and could not be read.\n"
            f"  Detail: {e}\n"
            f"  To recover, inspect or delete {DATA_FILE} and re-add your tasks.",
            file=sys.stderr,
        )
        sys.exit(1)
    except OSError as e:
        print(
            f"Error: Could not read {DATA_FILE}: {e.strerror}.",
            file=sys.stderr,
        )
        sys.exit(1)


def save_todos(todos):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(todos, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(
            f"Error: Could not write to {DATA_FILE}: {e.strerror}.",
            file=sys.stderr,
        )
        sys.exit(1)


def cmd_list(args):
    todos = load_todos()
    if not todos:
        print("No tasks yet. Use `todo add` to create one.")
        return
    for i, t in enumerate(todos):
        missing = [f for f in ("id", "task", "done") if f not in t]
        if missing:
            print(
                f"Warning: Entry {i} in {DATA_FILE} is missing fields {missing}, skipped.",
                file=sys.stderr,
            )
            continue
        status = "✓" if t["done"] else "○"
        print(f"  {status} #{t['id']}  {t['task']}")


def cmd_done(args):
    todos = load_todos()
    for i, t in enumerate(todos):
        missing = [f for f in ("id", "task", "done") if f not in t]
        if missing:
            print(
                f"Warning: Entry {i} in {DATA_FILE} is missing fields {missing}, skipped.",
                file=sys.stderr,
            )
            continue
        if not isinstance(t["id"], int):
            print(
                f"Warning: Entry {i} in {DATA_FILE} has non-integer id {t['id']!r}, skipped.",
                file=sys.stderr,
            )
            continue
        if t["id"] == args.id:
            if t["done"]:
                print(f"#{args.id} is already done.", file=sys.stderr)
                sys.exit(2)
            t["done"] = True
            save_todos(todos)
            print(f"Done #{args.id}: {t['task']}")
            return
    print(f"Error: task #{args.id} not found.", file=sys.stderr)
    sys.exit(1)


def cmd_delete(args):
    todos = load_todos()
    target_was_corrupt = False
    for i, t in enumerate(todos):
        missing = [f for f in ("id", "task", "done") if f not in t]
        if missing:
            print(
                f"Warning: Entry {i} in {DATA_FILE} is missing fields {missing}, skipped.",
                file=sys.stderr,
            )
            if "id" not in missing and t.get("id") == args.id:
                target_was_corrupt = True
            continue
        if not isinstance(t["id"], int):
            print(
                f"Warning: Entry {i} in {DATA_FILE} has non-integer id {t['id']!r}, skipped.",
                file=sys.stderr,
            )
            continue
        if t["id"] == args.id:
            todos.pop(i)
            save_todos(todos)
            print(f"Deleted #{args.id}: {t['task']}")
            return
    if target_was_corrupt:
        print(
            f"Error: task #{args.id} exists in {DATA_FILE} but its entry is corrupt. "
            f"Inspect or manually edit {DATA_FILE} to remove it.",
            file=sys.stderr,
        )
    else:
        print(f"Error: task #{args.id} not found.", file=sys.stderr)
    sys.exit(1)


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

    # list
    subparsers.add_parser("list", help="List all tasks").set_defaults(func=cmd_list)

    # done
    p_done = subparsers.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int, help="Task id")
    p_done.set_defaults(func=cmd_done)

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int, help="Task id")
    p_delete.set_defaults(func=cmd_delete)

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

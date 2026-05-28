#!/usr/bin/env python3
import argparse
import os
import sys
import json
import datetime
import uuid
import tempfile
import shutil
import subprocess

TODOS_DIRNAME = ".todos"

# ---------- utils ----------


def now():
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def die(msg):
    print(f"todo: {msg}", file=sys.stderr)
    sys.exit(1)


def ensure_repo():
    base, _, _ = todos_paths()
    if not os.path.isdir(base):
        die("not initialized (run `todo init`)")


def git(*args):
    return subprocess.run(
        ["git", *args],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def git_output(*args):
    return subprocess.run(
        ["git", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )


def repo_root():
    res = git_output("rev-parse", "--show-toplevel")
    if res.returncode != 0:
        return None
    root = res.stdout.strip()
    return root if root else None


def todos_paths():
    root = repo_root()
    base = os.path.join(root, TODOS_DIRNAME) if root else TODOS_DIRNAME
    return base, os.path.join(base, "todos.jsonl"), os.path.join(base, "closed.jsonl")


def load_todos(path=None):
    if path is None:
        _, path, _ = todos_paths()
    todos = {}
    if not os.path.exists(path):
        return todos
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            todos[obj["id"]] = obj
    return todos


def resolve_id(todos, needle):
    if needle in todos:
        return needle
    matches = [t_id for t_id in todos if t_id.startswith(needle)]
    if not matches:
        die("unknown id")
    if len(matches) > 1:
        die("ambiguous id: " + ", ".join(sorted(matches)))
    return matches[0]


def write_todos(todos, path=None):
    if path is None:
        _, path, _ = todos_paths()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
    with os.fdopen(fd, "w") as f:
        for _id in sorted(todos):
            f.write(json.dumps(todos[_id], separators=(",", ":")) + "\n")
    shutil.move(tmp, path)


# ---------- commands ----------


def cmd_init(_):
    base, todos_file, closed_file = todos_paths()
    os.makedirs(base, exist_ok=True)

    if not os.path.exists(todos_file):
        write_todos({}, todos_file)
    if not os.path.exists(closed_file):
        write_todos({}, closed_file)

    root = repo_root()
    if root:
        entries = [
            ".todos/todos.jsonl merge=todo\n",
            ".todos/closed.jsonl merge=todo\n",
        ]
        ga = os.path.join(root, ".gitattributes")

        if os.path.exists(ga):
            with open(ga) as f:
                existing = f.read()
            to_add = [e for e in entries if e not in existing]
            if to_add:
                with open(ga, "a") as af:
                    af.writelines(to_add)
        else:
            with open(ga, "w") as f:
                f.writelines(entries)

        git("config", "merge.todo.driver", "python todo.py merge %O %A %B")

    print("initialized todo")


def cmd_new(args):
    ensure_repo()
    _, todos_file, _ = todos_paths()
    todos = load_todos(todos_file)
    _id = "td-" + uuid.uuid4().hex[:8]
    todos[_id] = {
        "id": _id,
        "title": args.title,
        "summary": "",
        "status": "open",
        "deps": [],
        "updated_at": now(),
    }
    write_todos(todos, todos_file)
    print(_id)


def cmd_close(args):
    ensure_repo()
    _, todos_file, closed_file = todos_paths()
    todos = load_todos(todos_file)
    _id = resolve_id(todos, args.id)
    closed = load_todos(closed_file)
    todos[_id]["status"] = "closed"
    todos[_id]["updated_at"] = now()
    closed[_id] = todos[_id]
    del todos[_id]
    write_todos(todos, todos_file)
    write_todos(closed, closed_file)


def cmd_dep(args):
    ensure_repo()
    _, todos_file, _ = todos_paths()
    todos = load_todos(todos_file)
    child_id = resolve_id(todos, args.child)
    parent_id = resolve_id(todos, args.parent)
    if parent_id not in todos[child_id]["deps"]:
        todos[child_id]["deps"].append(parent_id)
        todos[child_id]["deps"].sort()
        todos[child_id]["updated_at"] = now()
    write_todos(todos, todos_file)


def cmd_summary(args):
    ensure_repo()
    _, todos_file, _ = todos_paths()
    todos = load_todos(todos_file)
    _id = resolve_id(todos, args.id)
    todos[_id]["summary"] = args.text
    todos[_id]["updated_at"] = now()
    write_todos(todos, todos_file)


def cmd_list(args):
    ensure_repo()
    _, todos_file, closed_file = todos_paths()
    path = closed_file if args.closed else todos_file
    todos = load_todos(path)
    items = sorted(todos.values(), key=lambda x: x["id"])
    if args.json:
        for t in items:
            print(json.dumps(t, separators=(",", ":")))
        return
    for t in items:
        deps = ",".join(t["deps"])
        summary = f": {t['summary']}" if t.get("summary") else ""
        print(
            f"{t['id']} [{t['status']}] {t['title']}{summary}"
            + (f" <- {deps}" if deps else "")
        )


def cmd_ready(args):
    ensure_repo()
    _, todos_file, _ = todos_paths()
    todos = load_todos(todos_file)
    ready = []
    for t in todos.values():
        if t["status"] != "open":
            continue
        if all(d in todos and todos[d]["status"] == "closed" for d in t["deps"]):
            ready.append(t)
    ready = sorted(ready, key=lambda x: x["id"])
    if args.json:
        for t in ready:
            print(json.dumps(t, separators=(",", ":")))
        return
    for t in ready:
        print(f"{t['id']} {t['title']}")


# ---------- merge driver ----------


def cmd_merge(args):
    base = load_todos(args.base)
    ours = load_todos(args.ours)
    theirs = load_todos(args.theirs)

    merged = {}
    for _id in set(base) | set(ours) | set(theirs):
        a = ours.get(_id)
        b = theirs.get(_id)
        if not a and not b:
            continue
        if not b or (a and a["updated_at"] >= b["updated_at"]):
            merged[_id] = a
        else:
            merged[_id] = b

    write_todos(merged, args.ours)


# ---------- argparse ----------


def main():
    p = argparse.ArgumentParser(prog="todo")
    sp = p.add_subparsers(dest="cmd", required=True)

    def _add(cmd, *argspec):
        sub = sp.add_parser(cmd)
        for flags, kw in argspec:
            sub.add_argument(*flags, **kw)
        return sub

    _add("init")

    _add("new", (("title",), {}))
    _add("close", (("id",), {}))
    _add("dep", (("child",), {}), (("parent",), {}))
    _add("summary", (("id",), {}), (("text",), {}))
    _add(
        "list",
        (("--closed",), {"action": "store_true"}),
        (("--json",), {"action": "store_true"}),
    )
    _add("ready", (("--json",), {"action": "store_true"}))

    _add(
        "merge",
        (("base",), {}),
        (("ours",), {}),
        (("theirs",), {}),
    )

    args = p.parse_args()

    {
        "init": cmd_init,
        "new": cmd_new,
        "close": cmd_close,
        "dep": cmd_dep,
        "summary": cmd_summary,
        "list": cmd_list,
        "ready": cmd_ready,
        "merge": cmd_merge,
    }[args.cmd](args)


if __name__ == "__main__":
    main()

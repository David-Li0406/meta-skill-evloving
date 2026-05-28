"""Simple, fast and fun task runner, not unlike gulp / grunt (but zero dep)"""

import os
import shutil
import subprocess
import sys
import textwrap


# === TASKS (add your do_ functions here) ===


def do_check(args) -> None:
    """Run linting and type checking"""
    c("ruff check")


def do_format(args) -> None:
    """Format code with ruff"""
    c("ruff format .")


def do_test(args) -> None:
    """Run tests"""
    c("pytest")


def default() -> None:
    show_help()


# === LIBRARY FUNCTIONS ===

emit = print


def c(cmd):
    """Run command, raise on failure"""
    emit(">", cmd)
    subprocess.check_call(cmd, shell=True)


def c_ignore(cmd):
    """Run command, ignore failures"""
    emit(">", cmd)
    subprocess.call(cmd, shell=True)


def c_dir(cmd, dir):
    """Run command in specific directory"""
    emit("%s > %s" % (dir, cmd))
    subprocess.check_call(cmd, cwd=dir, shell=True)


def c_spawn(cmd, cwd=None):
    """Spawn command in background"""
    emit(">", cmd)
    subprocess.Popen(cmd, cwd=cwd, shell=True)


def copy_files(sources, destinations):
    """Copy each source to each destination"""
    for src in sources:
        for dest in destinations:
            src = os.path.abspath(src)
            dest = os.path.abspath(dest)
            emit("cp %s -> %s" % (src, dest))
            if not os.path.isdir(dest):
                emit("Directory not found", dest)
                continue
            shutil.copy(src, dest)


# === LAUNCHER (do not edit below) ===


def show_help() -> None:
    g = globals()
    emit(
        "Command not found, try",
        sys.argv[0],
        " | ".join([n[3:] for n in g if n.startswith("do_")]),
        "| <command> -h",
    )


def main() -> None:
    if len(sys.argv) < 2:
        default()
        return
    func = sys.argv[1]
    f = globals().get("do_" + func)
    if sys.argv[-1] == "-h":
        emit(
            textwrap.dedent(f.__doc__).strip()
            if f.__doc__
            else "No documentation for this command",
        )
        return
    if not f:
        show_help()
        return
    f(sys.argv[2:])


if __name__ == "__main__":
    main()

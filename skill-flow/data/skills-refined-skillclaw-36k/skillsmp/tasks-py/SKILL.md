---
name: tasks-py
description: Create and maintain tasks.py task runner files. Use when user wants to add project automation, create a tasks.py file, add tasks, or mentions "tasks.py".
---

# tasks.py Task Runner

A zero-dependency Python task runner using `do_` prefixed functions.

## Creating a New tasks.py

**Minimal** (zero dependencies, self-contained): Copy [tasks.py](tasks.py) to the project root.

**Maximal** (argparse integration, task modules, task-by-index): Use [scaffer-templates tasks.py](https://github.com/vivainio/scaffer-templates/blob/master/templates/tasks/tasks.py)

Use minimal for standard tasks (check, format, test). Use maximal for project-specific tasks or if you need argparse arguments.

## Adding Tasks

Add new tasks by creating `do_<name>` functions:

```python
def do_build(args) -> None:
    """Build the project"""
    c("python -m build")
```

## Common Task Patterns

### Publishing to PyPI
```python
def do_publish(args) -> None:
    """Publish package to PyPI"""
    shutil.rmtree("dist", ignore_errors=True)
    c("python -m build")
    c("twine upload dist/*")
```

### Running in subdirectory
```python
def do_test(args) -> None:
    """Run tests in test directory"""
    os.chdir("test")
    c("pytest")
```

### Using c_dir for directory-scoped commands
```python
def do_frontend(args) -> None:
    """Build frontend"""
    c_dir("npm run build", "frontend")
```

### Task with arguments
```python
def do_greet(args) -> None:
    """Greet someone: greet <name>"""
    name = args[0] if args else "World"
    print(f"Hello, {name}!")
```

## Usage

```bash
python tasks.py              # Show available tasks
python tasks.py check        # Run the check task
python tasks.py test -h      # Show help for test task
```

## Library Functions Reference

| Function | Purpose |
|----------|---------|
| `c(cmd)` | Run command, fail on error |
| `c_ignore(cmd)` | Run command, ignore errors |
| `c_dir(cmd, dir)` | Run command in directory |
| `c_spawn(cmd, cwd)` | Run command in background |
| `copy_files(src, dest)` | Copy files to destinations |

## Guidelines

- Keep tasks.py at project root
- Only use standard library imports
- Document tasks with docstrings
- Use `c()` for commands that must succeed
- Use `c_ignore()` for optional/cleanup commands

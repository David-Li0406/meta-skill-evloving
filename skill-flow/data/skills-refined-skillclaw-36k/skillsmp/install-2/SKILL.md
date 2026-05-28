---
name: install
description: Use this skill when you want to install something (npm / uv / brew / `x.sh | bash` / ...), or when the user asks to install
---

# Install skill

## Option 1: Installing something in npm / uv / and so on

Use the command line (e.g `npm install`), don't change the package file directly (e.g `package.json`)

## Option 2: Installing new software on the computer

Check what are the recent installation instructions for this software, e.g `https://docs.astral.sh/uv/getting-started/installation/` to check how to install `uv`, from the OFFICIAL website not a blog post or so.

Don't default to `brew` or to installation instructions you memorized, but rather check what is the latest recommended way to install.

## Option 3: Installing python versions specifically

Use `uv python install`. [Here](https://docs.astral.sh/uv/guides/install-python/) are the official docs.

```bash
# Install a Python version
uv python install 3.12

# Install multiple versions
uv python install 3.10 3.11 3.12

# List installed versions
uv python list --only-installed

# Pin a version for the current project
uv python pin 3.12
```

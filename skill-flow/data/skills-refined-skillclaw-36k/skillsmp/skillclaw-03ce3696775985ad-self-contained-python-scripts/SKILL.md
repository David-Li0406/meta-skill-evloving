---
name: self-contained-python-scripts
description: Use this skill when you want to write self-installing, autocontained Python scripts that manage their own dependencies.
---

# Skill body

Use this to write Python tools, scripts, or CLIs as single files.

Using PEP 723 inline metadata, you can create self-contained Python scripts that declare their own dependencies. This allows you to run your scripts in isolated environments without needing to manually set up virtual environments or install dependencies.

To do that, embed the invocation of the `uv` command right in the shebang line.

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "httpx",
# ]
# ///
import httpx
# Your script logic here
```
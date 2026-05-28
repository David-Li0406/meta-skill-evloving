---
name: self-contained-python-scripts
description: Use this skill to write self-installing autocontained Python scripts that declare their own dependencies.
---

# Body of the merged SKILL.md

This skill allows you to create Python tools, scripts, or CLIs as single files. By using PEP 723 inline metadata, you can declare dependencies within the script, enabling execution in isolated environments without manual setup of virtual environments.

To implement this, embed the invocation of the `uv` command directly in the shebang line:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "httpx",
# ]
# ///
import httpx
.
.
.
```
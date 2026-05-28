---
name: ignored-files
description: Read when accessing gitignored files
---

You are trying to read a file that is in `.cursorignore`.
You can only with `grep`, `head`, etc.
You cannot modify them, they are auto-generated.
If you are trying to read a type/function, use `read-symbol` skill instead.
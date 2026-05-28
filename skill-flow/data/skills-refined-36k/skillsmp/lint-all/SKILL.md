---
name: lint-all
description: Lint the entire project. Use whenever you finish editing to ensure your code is clean and follows best practices.
---

# Linting

Note: this guide assumes you are in the root of the project.

To lint this project, you should use the Dagger function `lint`:

```bash
dagger call lint --source=.
```

## Per-component linting

You can also lint the Cloudflare Worker on its own:

```bash
dagger call cf-worker-lint --source=.
```

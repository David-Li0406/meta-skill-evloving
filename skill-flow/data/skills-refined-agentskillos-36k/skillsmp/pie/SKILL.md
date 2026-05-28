---
name: pie
description: How to run, test and debug Pie
---

# Preparing Pie

Please make sure everything is up to date.
If you are first time using Pie, the setup the environment:

```bash
uv sync --extra cu128
```

If you have modified the Rust runtime, then you'll need to rebuild it.
```bash
touch pyproject.toml && uv sync --extra cu128
```
* Python edits should be okay because uv installs edited dependencies.


# Runnig the one-shot inferlet.

uv run pie run text-completion -- --prompt "Hello world"

# Running long running Pie server

to run the Pie server, use:

```
uv run pie serve
```

You can configure the server using the `pie config` command, or by directly editing the config file.
```
cat ~/.pie/config.toml
```


# Running the workload


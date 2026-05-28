---
name: setup
description: Check and install the Vocal Bridge CLI. Run this automatically before using other Vocal Bridge commands if the CLI is not installed.
allowed-tools: Bash
---

Check if the Vocal Bridge CLI is installed and install it if needed.

## Step 1: Check if vb CLI exists

Try these in order:
1. `which vb` - Check if in PATH
2. `python -m vocal_bridge.cli --version` - Check if installed as module
3. `pip show vocal-bridge` - Check if package is installed

## Step 2: If not installed, install it

If the CLI is not found, install using pip:

```bash
pip install --upgrade vocal-bridge
```

Or if using uv:

```bash
uv pip install --upgrade vocal-bridge
```

## Step 3: Verify installation

Run: `vb --version` or `python -m vocal_bridge.cli --version`

If installation succeeds, inform the user they can now use Vocal Bridge commands like `/vocal-bridge:login`.

If pip install fails, suggest using the standalone script:

```bash
mkdir -p ~/.local/bin
curl -fsSL https://vocalbridgeai.com/cli/vb.py -o ~/.local/bin/vb && chmod +x ~/.local/bin/vb
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
```

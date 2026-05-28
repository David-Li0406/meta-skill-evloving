---
name: sandbox-agent
description: "Run agent CLIs (codex/copilot/opencode) inside a Podman container with full internet access but filesystem exposure limited to the repo root + explicit bind mounts."
---

# sandbox-agent

Use this when you want:
- Full egress/network for agent CLIs (web search, fetching, etc.)
- Tight filesystem boundaries via container bind mounts (repo root + explicit allowlist)

This repo contains a wrapper script intended to be installed as `sandbox-agent`.

## Workflow

1. **Build the image**

   From the repo root (this repository):

   ```bash
  podman build -t localhost/sandbox-agent:latest -f Containerfile .
   ```

2. **Install the wrapper**

   ```bash
  install -m 0755 sandbox-agent ~/.local/bin/sandbox-agent
   ```

3. **(Optional) Configure extra mounts**

  Create `~/.config/sandbox-agent/config.sh`:

   ```bash
  CODEX_CONTAINER_SANDBOX_IMAGE="localhost/sandbox-agent:latest"

   # Extra read-only mounts (mapped under /home/codex/... if under $HOME)
   CODEX_CONTAINER_SANDBOX_RO_MOUNTS=(
     "$HOME/.local/bin"
   )

   # Extra read-write mounts
   CODEX_CONTAINER_SANDBOX_RW_MOUNTS=(
     "$HOME/.cache/uv"
     "$HOME/tmp"
   )
   ```

4. **Login once inside the container**

   ```bash
  sandbox-agent --shell
  codex login
   ```

5. **Run the self-test (recommended)**

   ```bash
   ./selftest.sh
   ```

  If this repo is vendored as a git submodule at `./sandbox-agent/` (for example in a dotfiles repo), either:
  - `cd sandbox-agent && ./selftest.sh`, or
  - run `./sandbox-agent/selftest.sh` from the parent repo root.

6. **Run an agent CLI**

  ```bash
  sandbox-agent codex exec "Summarize this repo"
  ```

## Safety notes

- This wrapper runs with full networking. Anything mounted into the container can be exfiltrated.
- Keep mounts minimal; do not mount secrets, password stores, SSH keys, or large chunks of `$HOME` unless you intend to expose them.

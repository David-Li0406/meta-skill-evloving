# Linux

## Prereqs

- Ensure `git` is installed via your package manager.

## Script setup

```bash
chmod +x ralph-loop/ralph.sh
```

If the script has CRLF line endings:
```bash
sed -i 's/\r$//' ralph-loop/ralph.sh
```

## Example run

```bash
./ralph-loop/ralph.sh "codex exec --full-auto" 20
```

## Long-running runs

- Prefer `tmux` or `screen` if installed.
- Or detach with `nohup`:
```bash
nohup ./ralph-loop/ralph.sh "<AGENT_CMD>" 20 > ralph.log 2>&1 &
```

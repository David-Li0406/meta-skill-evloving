# Windows (WSL2)

## Install or repair WSL

- Install Ubuntu if missing:
  - `wsl --install -d Ubuntu-24.04`
  - `wsl --set-default Ubuntu-24.04`
- Verify:
  - `wsl -l -v`

If a distro fails to start due to missing `ext4.vhdx`, reinstall the distro.

## Run ralph-loop from WSL

Use `/mnt/c` paths to reach Windows files:
```bash
wsl -d Ubuntu-24.04 --exec bash -lc "cd /mnt/c/Users/<user>/path && git clone https://github.com/syuya2036/ralph-loop.git ralph-loop"
```

## Fix line endings

If `ralph.sh` fails with `cannot execute: required file not found`, fix CRLF line endings:
```bash
sed -i 's/\r$//' ralph-loop/ralph.sh
```

## Example run

```bash
wsl -d Ubuntu-24.04 --exec bash -lc "cd /mnt/c/Users/<user>/path && chmod +x ralph-loop/ralph.sh && ./ralph-loop/ralph.sh \"codex exec --full-auto\" 20"
```

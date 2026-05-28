# CLI Validation Checklist

Detailed validation steps for each CLI in the ecosystem.

## Core CLIs

### outline

| check | command | expected |
|-------|---------|----------|
| PATH | `which outline` | path to binary |
| help | `outline --help` | usage info |
| basic | `outline src/` | YAML output |
| recursive | `outline src/ -r` | recursive parse |

### layer

| check | command | expected |
|-------|---------|----------|
| PATH | `which layer` | path to binary |
| help | `layer --help` | usage info |
| basic | `layer .` | dependency tree |
| json | `layer . --format=json` | JSON output |

### verify

| check | command | expected |
|-------|---------|----------|
| PATH | `which verify` | path to binary |
| help | `verify --help` | usage info |
| summary | `verify --format=summary` | test summary |

### agents

| check | command | expected |
|-------|---------|----------|
| PATH | `which agents` | path to binary |
| help | `agents --help` | usage info |
| session list | `agents session list` | session list |
| report | `agents report --help` | report subcommands |

### trails

| check | command | expected |
|-------|---------|----------|
| PATH | `which trails` | path to binary |
| help | `trails --help` | usage info |
| replay | `trails trail replay --last 1` | recent events |

### mem

| check | command | expected |
|-------|---------|----------|
| PATH | `which mem` | path to binary |
| help | `mem --help` | usage info |
| audit | `mem audit --json` | memory audit |

### slack

| check | command | expected |
|-------|---------|----------|
| PATH | `which slack` | path to binary |
| help | `slack --help` | usage info |
| workspace | `slack workspace list` | workspace list |

### linear

| check | command | expected |
|-------|---------|----------|
| PATH | `which linear` | path to binary |
| help | `linear --help` | usage info |
| workspace | `linear workspace list` | workspace list |

### format

| check | command | expected |
|-------|---------|----------|
| PATH | `which format` | path to binary |
| help | `format --help` | usage info |
| slack | `echo "**test**" \| format slack` | `*test*` |

### prompts

| check | command | expected |
|-------|---------|----------|
| PATH | `which prompts` | path to binary |
| help | `prompts --help` | usage info |
| list | `prompts commands list --json -q` | JSON array |
| export | `prompts commands export /prime` | expanded content |

### roles

| check | command | expected |
|-------|---------|----------|
| PATH | `which roles` | path to binary |
| help | `roles --help` | usage info |
| list | `roles list --json -q` | JSON array |
| export | `roles export jony` | role content |

### epub

| check | command | expected |
|-------|---------|----------|
| PATH | `which epub` | path to binary |
| help | `epub --help` | usage info |

## Agent CLIs

### claude

| check | command | expected |
|-------|---------|----------|
| PATH | `which claude` | path to binary |
| version | `claude --version` | version string |

### codex

| check | command | expected |
|-------|---------|----------|
| PATH | `which codex` | path to binary |
| version | `codex --version` | version string |

### copilot

| check | command | expected |
|-------|---------|----------|
| PATH | `which copilot` | path to binary |
| version | `copilot --version` | version string |

## Common Fixes

| issue | fix |
|-------|-----|
| CLI not found | check `~/.local/bin` in PATH |
| symlink broken | `ln -sf source ~/.local/bin/name` |
| help not showing commands | regenerate oclif manifest |
| permission denied | `chmod +x binary` |

## xmind2md Skill

Use this skill to read and process XMind (`.xmind`) files by converting them to markdown. The output is printed to stdout and preserves the mind map hierarchy.

## Requirements

- Python 3

If Python 3 is not available, install it before using this skill.

## Usage

Basic conversion:

```bash
python ~/.claude/skills/xmind2md/references/xmind2md /path/to/file.xmind
```

## Options

- `--numbers`: Prefix bullets with hierarchical numbers (e.g., 1.2.3)
- `--max-depth N`: Limit depth (1 = root only)
- `--sheet-sep TEXT`: Separator between sheets (default: blank line)

## Examples

Limit depth to two levels:

```bash
python ~/.claude/skills/xmind2md/references/xmind2md --max-depth 2 /path/to/file.xmind
```

Add hierarchical numbering:

```bash
python ~/.claude/skills/xmind2md/references/xmind2md --numbers /path/to/file.xmind
```

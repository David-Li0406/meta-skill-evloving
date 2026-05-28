# Claude Code Status Line Configuration

Complete reference for custom status line configurations.

## Overview

The status line appears at the bottom of Claude Code and can display contextual information about your session. Configure via `statusLine` in `~/.claude/settings.json`.

## Configuration Structure

```json
{
  "statusLine": {
    "type": "command",
    "command": "your-command-here"
  }
}
```

The command receives JSON input via stdin with session context and should output formatted text to stdout.

## Available Data (JSON Input)

```json
{
  "workspace": {
    "current_dir": "/path/to/project"
  },
  "model": {
    "display_name": "Opus 4.5"
  },
  "context_window": {
    "used_percentage": 42.5
  },
  "cost": {
    "total_cost_usd": 1.23
  },
  "transcript_path": "/path/to/transcript.json"
}
```

## Style Presets

### Minimal
Clean, unobtrusive - just the essentials.

```
~/project  main  45%
```

**Elements**: Directory, git branch, context percentage

**Command**:
```bash
input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir' | sed "s|$HOME|~|g")
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
cd "$(echo "$input" | jq -r '.workspace.current_dir')" 2>/dev/null
branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')
printf "%s" "$cwd"
[ -n "$branch" ] && printf "  %s" "$branch"
[ -n "$used" ] && printf "  %d%%" "${used%.*}"
echo
```

### Powerline
Arrow separators with colored segments. Modern terminal aesthetic.

```
 ~/project   main*   ▓▓░░░ 42%   Opus 4.5   $1.23
```

**Elements**: Directory, git (branch + status + ahead/behind), context bar, model, cost

**Features**:
- Powerline arrow separators ()
- Alternating background colors
- Color-coded context bar (green < 50%, yellow 50-80%, red > 80%)
- Git dirty indicator (*) and ahead/behind arrows

### Classic
Simple text with subtle colors. Traditional terminal style.

```
koen:~/project (main*) | Opus 4.5 | 42% | 14:30 | $1.23
```

**Elements**: User, directory, git, model, context %, time, cost

**Features**:
- Pipe separators
- Minimal color usage
- User@host style prefix

### Data-rich
Everything visible for power users who want maximum information.

```
koen:~/project  main*↑1↓2  ▓▓░░░ 42%  Opus 4.5  14:30  todos:3  $1.23
```

**Elements**: User, directory, git (full), context bar, model, time, todo count, cost

## Color Schemes

> **Note**: These color values are shown for reference. When using this plugin, use the palette system instead of hardcoding hex values. See [PALETTE-SYSTEM.md](../../../docs/PALETTE-SYSTEM.md) for token usage.

### Gruvbox (Warm)
**Palette ID**: `gruvbox-dark`
```bash
BG0='#282828'; BG1='#3c3836'
FG='#ebdbb2'
AQUA='#8ec07c'; GREEN='#b8bb26'
YELLOW='#fabd2f'; ORANGE='#fe8019'
RED='#fb4934'; GRAY='#928374'
```

### Catppuccin Mocha (Soft)
**Palette ID**: `catppuccin-mocha`
```bash
BG0='#1e1e2e'; BG1='#313244'
FG='#cdd6f4'
TEAL='#94e2d5'; GREEN='#a6e3a1'
YELLOW='#f9e2af'; PEACH='#fab387'
RED='#f38ba8'; OVERLAY='#6c7086'
```

### Dracula (Vibrant)
**Palette ID**: `dracula`
```bash
BG0='#282a36'; BG1='#44475a'
FG='#f8f8f2'
CYAN='#8be9fd'; GREEN='#50fa7b'
YELLOW='#f1fa8c'; ORANGE='#ffb86c'
RED='#ff5555'; PURPLE='#bd93f9'
```

### Nord (Cool)
**Palette ID**: `nord`
```bash
BG0='#2e3440'; BG1='#3b4252'
FG='#eceff4'
CYAN='#88c0d0'; GREEN='#a3be8c'
YELLOW='#ebcb8b'; ORANGE='#d08770'
RED='#bf616a'; FROST='#81a1c1'
```

### Tokyo Night
**Palette ID**: `tokyo-night`
```bash
BG0='#1a1b26'; BG1='#24283b'
FG='#c0caf5'
CYAN='#7dcfff'; GREEN='#9ece6a'
YELLOW='#e0af68'; ORANGE='#ff9e64'
RED='#f7768e'; PURPLE='#bb9af7'
```

## Elements Reference

### Directory
```bash
cwd=$(echo "$input" | jq -r '.workspace.current_dir' | sed "s|$HOME|~|g")
```

### Git Branch
```bash
cd "$(echo "$input" | jq -r '.workspace.current_dir')" 2>/dev/null
branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')
```

### Git Status (Dirty)
```bash
[ -n "$(git status --porcelain 2>/dev/null)" ] && status='*'
```

### Git Ahead/Behind
```bash
ab=$(git rev-list --left-right --count @{u}...HEAD 2>/dev/null || echo '')
if [ -n "$ab" ]; then
  behind=$(echo "$ab" | cut -f1)
  ahead=$(echo "$ab" | cut -f2)
  [ "$ahead" -gt 0 ] && ahead_behind="↑${ahead}"
  [ "$behind" -gt 0 ] && ahead_behind="${ahead_behind}↓${behind}"
fi
```

### Context Usage (Percentage)
```bash
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
used_int=${used%.*}
```

### Context Bar (Visual)
```bash
filled=$((used_int / 20))
[ "$filled" -gt 5 ] && filled=5
empty=$((5 - filled))
bar=$(printf '▓%.0s' $(seq 1 $filled 2>/dev/null))
bar="${bar}$(printf '░%.0s' $(seq 1 $empty 2>/dev/null))"
```

### Model Name
```bash
model=$(echo "$input" | jq -r '.model.display_name')
```

### Time
```bash
time=$(date +%H:%M)
```

### Cost
```bash
cost=$(echo "$input" | jq -r '.cost.total_cost_usd // empty')
[ -n "$cost" ] && [ "$cost" != "null" ] && cost_fmt=$(printf "%.2f" "$cost")
```

### Todo Count
```bash
transcript=$(echo "$input" | jq -r '.transcript_path')
todo_count=$([ -f "$transcript" ] && grep -c '"type":"todo"' "$transcript" 2>/dev/null || echo 0)
```

### User
```bash
user=$(whoami)
```

## ANSI Color Codes

### 256 Color
```bash
# Foreground
\033[38;5;COLORm

# Background
\033[48;5;COLORm
```

### True Color (RGB)
```bash
# Foreground
\033[38;2;R;G;Bm

# Background
\033[48;2;R;G;Bm
```

### Reset
```bash
\033[0m
```

## Complete Example: Powerline Gruvbox

```bash
input=$(cat)
user=$(whoami)
cwd=$(echo "$input" | jq -r '.workspace.current_dir' | sed "s|$HOME|~|g")
model=$(echo "$input" | jq -r '.model.display_name')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
cost=$(echo "$input" | jq -r '.cost.total_cost_usd // empty')

cd "$(echo "$input" | jq -r '.workspace.current_dir')" 2>/dev/null
branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')
status=''
ahead_behind=''
if [ -n "$branch" ]; then
  [ -n "$(git status --porcelain 2>/dev/null)" ] && status='*'
  ab=$(git rev-list --left-right --count @{u}...HEAD 2>/dev/null || echo '')
  if [ -n "$ab" ]; then
    behind=$(echo "$ab" | cut -f1); ahead=$(echo "$ab" | cut -f2)
    [ "$ahead" -gt 0 ] && ahead_behind="↑${ahead}"
    [ "$behind" -gt 0 ] && ahead_behind="${ahead_behind}↓${behind}"
  fi
fi

# Gruvbox colors
BG0='\033[48;2;40;40;40m'; BG1='\033[48;2;60;56;54m'
AQUA='\033[38;2;142;192;124m'; GREEN='\033[38;2;184;187;38m'
YELLOW='\033[38;2;250;189;47m'; GRAY='\033[38;2;146;131;116m'
RED='\033[38;2;251;73;52m'; R='\033[0m'

# Context bar
if [ -n "$used" ]; then
  used_int=${used%.*}
  filled=$((used_int / 20)); [ "$filled" -gt 5 ] && filled=5
  empty=$((5 - filled))
  bar=$(printf '▓%.0s' $(seq 1 $filled 2>/dev/null))
  bar="${bar}$(printf '░%.0s' $(seq 1 $empty 2>/dev/null))"
  if [ "$used_int" -gt 80 ]; then UC=$RED
  elif [ "$used_int" -gt 50 ]; then UC=$YELLOW
  else UC=$GREEN; fi
fi

# Output
printf "${BG0}${AQUA} ${cwd} ${R}"
[ -n "$branch" ] && printf "${BG1}${GREEN}  ${branch}${YELLOW}${status}${ahead_behind} ${R}"
[ -n "$used" ] && printf "${BG0}${UC} ${bar} ${used_int}%% ${R}"
printf "${BG1}${GRAY} ${model} ${R}"
if [ -n "$cost" ] && [ "$cost" != "null" ]; then
  cost_fmt=$(printf "%.2f" "$cost")
  printf "${BG0}${YELLOW} \$${cost_fmt} ${R}"
fi
echo
```

## Customization Tips

1. **Test commands directly**: `echo '{"workspace":{"current_dir":"'"$PWD"'"}}' | your-command`
2. **Use jq carefully**: Always provide fallback with `// empty` or `// "default"`
3. **Quote properly**: Use single quotes around heredocs to prevent variable expansion issues
4. **Keep it fast**: Status line runs frequently; avoid slow operations
5. **Handle missing data**: Not all fields are always present

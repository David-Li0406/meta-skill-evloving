# Global Prompts Sync

Synchronizes prompt files to both GitHub Copilot and OpenCode global configuration directories.

## Features

- ✅ Syncs agents, rules, and commands to GitHub Copilot
- ✅ Syncs agents, rules, and commands to OpenCode
- ✅ Automatic file naming conversion for each editor
- ✅ Merges multiple rule files into single AGENTS.md for OpenCode
- ✅ Removes YAML front matter for OpenCode
- ✅ WSL environment detection and path handling

## Quick Start

1. Add your prompt files to the appropriate directories:
   - `prompts/agents/` - Agent definitions
   - `prompts/rules/` - Instruction/rules files
   - `prompts/commands/` - Command prompts

2. Run the sync script:
   ```bash
   python3 scripts/sync_prompts.py
   ```

## Usage

### Sync to all targets (default)
```bash
python3 scripts/sync_prompts.py
```

### Sync to GitHub Copilot only
```bash
python3 scripts/sync_prompts.py --target copilot
```

### Sync to OpenCode only
```bash
python3 scripts/sync_prompts.py --target opencode
```

## File Naming Conventions

### GitHub Copilot
- Agents: `filename.agent.md`
- Rules: `filename.instructions.md`
- Commands: `filename.prompt.md`

### OpenCode
- Agents: `filename.md` (copied as-is)
- Rules: Merged into single `AGENTS.md` (front matter removed)
- Commands: `filename.md` (copied as-is)

## Target Directories

### GitHub Copilot
All files synced to:
```
/mnt/c/Users/<USERNAME>/AppData/Roaming/Code/User/prompts/
```

### OpenCode
Files synced to separate directories:
```
~/.config/opencode/agent/          # or /mnt/c/Users/<USERNAME>/.config/opencode/agent/
~/.config/opencode/AGENTS.md       # or /mnt/c/Users/<USERNAME>/.config/opencode/AGENTS.md
~/.config/opencode/command/        # or /mnt/c/Users/<USERNAME>/.config/opencode/command/
```

## Examples

### Adding a New Agent

1. Create `prompts/agents/my-agent.md`:
   ```markdown
   ---
   name: my-agent
   description: My custom agent
   ---
   
   # My Agent
   
   Agent instructions here...
   ```

2. Run sync:
   ```bash
   python3 scripts/sync_prompts.py
   ```

3. Results:
   - GitHub Copilot: `my-agent.agent.md`
   - OpenCode: `agent/my-agent.md`

### Adding Multiple Rules

1. Create multiple rule files:
   - `prompts/rules/rule-1.md`
   - `prompts/rules/rule-2.md`

2. Run sync - OpenCode will have:
   - Single `AGENTS.md` with merged content (front matter removed)
   
3. GitHub Copilot will have:
   - `rule-1.instructions.md`
   - `rule-2.instructions.md`

## Requirements

- Python 3.6+
- WSL (for Windows users)
- Access to Windows file system (for GitHub Copilot sync)

## See Also

- [SKILL.md](SKILL.md) - Full skill documentation

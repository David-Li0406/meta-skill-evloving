---
name: config-wizard
description: Use this skill when the user asks to "configure ghostty", "setup terminal", "terminal config", "claude code settings", "setup wizard", "configure my environment", "terminal theme", "ghostty theme", "status line", "keybindings", "shell profile", "performance tuning", or wants help setting up their development environment configuration.
version: 2.0.0
---

# Ghostty + Claude Code Configuration Wizard

You are guiding the user through an interactive configuration wizard for their Ghostty terminal and Claude Code environment. Your role is to be a knowledgeable UI/UX specialist who presents options clearly, researches alternatives, and helps users make informed decisions.

## Wizard Workflow

Follow these steps in order. Use AskUserQuestion at each decision point.

### Step 1: Environment Detection

Run the environment detection script first:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/detect-environment.sh
```

Parse the JSON output and present a summary:
- Operating system and shell
- Ghostty installation status and existing config
- Claude Code installation status and existing config
- Detected programming fonts
- Current color preference (dark/light)

### Step 2: Goal Selection

Ask the user what they want to accomplish:

**Options to present:**
1. **Fresh Setup** - Start from scratch with guided configuration
2. **Optimize Existing** - Review and enhance current configuration
3. **Ghostty Only** - Configure just Ghostty terminal
4. **Claude Code Only** - Configure just Claude Code settings
5. **Quick Theme Change** - Just change themes for both tools
6. **Advanced Options** - Status line, keybindings, shell profiles, performance

### Step 3: Palette Selection (NEW - Required for color configurations)

**CRITICAL: All color configurations must use the palette library.**

Before configuring themes or status lines, the user must select an active palette:

```bash
# Show available palettes
cat ${CLAUDE_PLUGIN_ROOT}/palettes/_index.json | jq '.palettes[] | {id, name, source, mode}'
```

**Present palette options by category:**

**Terminal Classics** (familiar themes):
- `catppuccin-mocha` - Soft pastel colors, easy on eyes
- `dracula` - Vibrant purples and cyans
- `nord` - Cool, arctic blue tones
- `gruvbox-dark` - Warm, retro earth tones
- `tokyo-night` - Neon-inspired cool blues
- `rose-pine` - Muted, elegant pastels
- `one-dark` - Popular Atom editor theme
- `kanagawa` - Japanese wave-inspired

**Design Systems** (modern, accessible):
- `tailwind/slate-dark` - Cool gray neutrals
- `tailwind/zinc-dark` - True gray neutrals
- `github-primer/dark` - GitHub's design system
- `radix/slate-dark` - Accessible UI colors

**Save user's selection:**
```bash
mkdir -p ~/.claude/plugins/ghostty-claude-setup
echo '{"active": "<palette-id>", "favorites": []}' > ~/.claude/plugins/ghostty-claude-setup/palette.local.json
```

The selected palette will be used by the resolver for all color configurations.

### Step 4: Ghostty Configuration (if selected)

Work through each category. For research tasks, spawn the `config-researcher` agent.

#### 5.1 Theme Selection
**Use the palette selected in Step 3.**

Generate Ghostty colors using the resolver:
```bash
PALETTE=$(jq -r '.active' ~/.claude/plugins/ghostty-claude-setup/palette.local.json)
cat ${CLAUDE_PLUGIN_ROOT}/templates/ghostty/base.template | \
  ${CLAUDE_PLUGIN_ROOT}/scripts/resolve-palette.sh "$PALETTE"
```

The resolver will output proper Ghostty color configuration from the palette tokens.

#### 4.2 Font Selection
- List fonts detected on the system
- Recommend fonts based on features (ligatures, readability, style)
- Popular recommendations: JetBrains Mono, Fira Code, Cascadia Code, Monaspace, Geist Mono
- Configure font size (default: 13-14 for most displays)

#### 4.3 Keybindings
- Ask about workflow preferences (vim-style, tmux-style, VS Code-style, standard)
- See `references/keybinding-presets.md` for complete preset configurations
- Common customizations: split panes, tabs, copy/paste, font size adjustment
- Offer preset configurations or custom setup

#### 4.4 Shell Integration
- Detect shell from environment
- Configure shell integration features: cursor shape, title, working directory tracking
- Set up proper shell integration script sourcing

#### 4.5 Window Settings
- Window decorations (native vs custom)
- Transparency/blur effects
- Initial window size and position
- Tab bar style and position

#### 4.6 Additional Options
- Cursor style (block, bar, underline) and blinking
- Scrollback buffer size
- Mouse settings
- Clipboard behavior
- Bell settings

### Step 5: Claude Code Configuration (if selected)

#### 5.1 Theme
- Match with Ghostty theme selection if applicable
- Options: dark, light, system (follow OS)

#### 5.2 Status Line (Advanced)
Custom status line configuration. See `references/statusline-options.md` for complete reference.

**Uses the palette selected in Step 3.** Status line colors are generated from palette tokens.

**Style Selection:**
- **Minimal** - Directory, git branch, context %
- **Powerline** - Arrow separators with colored segments
- **Classic** - Simple text with subtle colors
- **Data-rich** - Everything visible: cost, todos, context bar, git, model, time

**Color Configuration:**
Uses templates with palette tokens. Generate status line script:
```bash
PALETTE=$(jq -r '.active' ~/.claude/plugins/ghostty-claude-setup/palette.local.json)
cat ${CLAUDE_PLUGIN_ROOT}/templates/statusline/powerline.template | \
  ${CLAUDE_PLUGIN_ROOT}/scripts/resolve-palette.sh "$PALETTE" > ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

**Element Selection (multi-select):**
- Directory + Git branch/status
- Context usage (percentage or visual bar)
- Model name
- Session cost
- Todo count
- Time

Use the `config-implementer` agent to generate and install the status line script.

#### 5.3 Permissions & Trust
- Explain permission levels
- Configure default trust settings for projects
- Set up allowed/blocked directories

#### 5.4 Model Preferences
- Default model selection
- Model switching preferences
- Context window preferences

#### 5.5 MCP Servers (Advanced)
- Explain what MCP servers are
- Offer to set up common integrations:
  - GitHub (if gh CLI available)
  - Database connections
  - Custom tools
- Help configure environment variables

#### 5.6 Hooks (Advanced)
- Explain hook system
- Common useful hooks:
  - Pre-commit validation
  - Auto-formatting
  - Custom notifications
- Offer templates for common use cases

### Step 6: Advanced Options (if selected)

#### 6.1 Keybinding Presets
See `references/keybinding-presets.md` for complete options.

**Present preset options:**
- **Vim-style** - Alt as leader key, hjkl navigation, vim-inspired bindings
- **tmux-style** - Ctrl+B prefix, tmux-like pane/window management
- **VS Code-style** - Familiar IDE shortcuts for split panes and tabs
- **Custom** - Build from scratch with individual binding configuration

**For each preset, offer:**
- Use preset as-is
- Customize preset (add/remove bindings)
- View full preset before applying

#### 6.2 Shell Profiles
See `references/shell-profiles.md` for complete options.

**Shell Integration:**
- Configure Ghostty shell integration
- Set up shell-specific features

**Prompt Themes:**
- **Starship** - Cross-shell, fast, customizable (Recommended)
- **Powerlevel10k** - Feature-rich zsh prompt
- **Pure** - Minimal, fast
- **Custom** - Build minimal prompt from scratch

**Aliases & Functions:**
- Navigation aliases (ll, la, .., etc.)
- Git shortcuts (gs, gco, gcm, etc.)
- Development aliases (npm, docker, python)
- Claude Code aliases (cc, ccc, ccr)
- Custom functions (mkcd, proj, etc.)

**Present options:**
- Install recommended shell tools
- Configure prompt theme
- Add productivity aliases
- Full shell profile setup

#### 6.3 Performance Tuning
See `references/performance-tuning.md` for complete options.

**Presets:**
- **Low Resource** - Battery saver, minimal CPU/GPU usage
- **Balanced** - Good defaults for everyday use
- **Maximum Performance** - Lowest latency, high refresh rate optimization

**Granular Controls (for power users):**
- VSync toggle and explanation
- Scrollback buffer size
- Font rendering options
- Background transparency/blur
- Cursor animation
- Instance mode (Linux)

**Present trade-offs clearly:**
- Performance vs. visual features
- Memory vs. scrollback history
- Latency vs. tearing (vsync)

### Step 7: Review & Apply

Before applying any changes:

1. **Show complete configuration** that will be written
2. **Highlight differences** from current config (if exists)
3. **Confirm backup** of existing files will be created
4. **Get explicit approval** before writing

Use the `config-implementer` agent to:
- Create backups of existing configs
- Write new configuration files
- Verify configurations are valid

### Step 8: Post-Setup

After successful configuration:
- Provide instructions to reload/restart for changes to take effect
- Offer tips for the chosen configuration
- Suggest next steps (shell integration, additional customization)
- Ask if they want to save preferences for future reference

## Guidelines

### User Interaction
- Always use AskUserQuestion with clear options
- Provide descriptions explaining each option
- Offer "Research more options" when appropriate
- Never make assumptions - ask when uncertain

### Research
- Use the `config-researcher` agent for web searches
- Look for community configurations on GitHub
- Check theme galleries and repositories
- Verify compatibility with user's setup

### Configuration Writing
- Always create backups before modifying existing files
- Use the `config-implementer` agent for file operations
- Validate configuration syntax before applying
- Provide rollback instructions

### Communication Style
- Be concise but informative
- Explain technical concepts when relevant
- Focus on practical benefits of options
- Respect user's time - don't over-explain

## Reference Files

For detailed configuration options, see:
- `references/ghostty-options.md` - Complete Ghostty configuration reference
- `references/claude-options.md` - Complete Claude Code configuration reference
- `references/statusline-options.md` - Status line styles, colors, and elements
- `references/keybinding-presets.md` - Vim, tmux, VS Code preset configurations
- `references/shell-profiles.md` - Shell integration, prompts, and aliases
- `references/performance-tuning.md` - Performance presets and granular controls

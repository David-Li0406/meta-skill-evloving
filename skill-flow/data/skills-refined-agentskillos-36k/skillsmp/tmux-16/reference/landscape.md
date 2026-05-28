# tmux Ecosystem Landscape

Guide for evaluating and extending tmux setup based on user context.

## Evaluating User Context

Before recommending plugins, understand the user's situation:

**Project type:**
| Context | Likely Needs |
|---------|--------------|
| Full-stack app (server, db, builds) | Session persistence, process restoration, multi-pane layouts |
| Monorepo with worktrees | Fast session switching, session-per-worktree patterns |
| Static files / journaling | Minimal - basics likely sufficient |
| Multiple active projects | Session management, fuzzy switching |

**Questions to clarify:**
- How many projects do you actively switch between?
- Do you use git worktrees?
- Do you run dev servers / databases locally?
- Do you reboot often? Care about restoring state?
- How terminal-centric is your workflow?

## Plugin Manager

| Tool | Status | Recommendation |
|------|--------|----------------|
| [tpm](https://github.com/tmux-plugins/tpm) | Abandoned (last merge Feb 2023) | Avoid |
| [tpm-redux](https://github.com/RyanMacG/tpm-redux) | Maintained fork | **Use this** |
| Manual management | Works | Fine for few plugins |

## Session Persistence

| Plugin | What | When to Use |
|--------|------|-------------|
| [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect) | Save/restore sessions manually | Want to survive reboots |
| [tmux-continuum](https://github.com/tmux-plugins/tmux-continuum) | Auto-save + auto-restore | Pairs with resurrect, "just works" persistence |

**How continuum works:**
1. Every 15 min (configurable), saves tmux state to `~/.config/tmux/resurrect/`
2. On tmux server start, automatically restores last saved state
3. Sessions, windows, panes, working directories restored
4. Processes NOT restored by default - configure resurrect for that

**Process restoration (optional):**
```bash
# In .tmux.conf - resurrect will restart these on restore
set -g @resurrect-processes 'vim nvim "npm run dev" postgres'
```

## Session Management

| Plugin | What | When to Use |
|--------|------|-------------|
| [tmux-sessionx](https://github.com/omerxx/tmux-sessionx) | Fuzzy session picker (fzf + zoxide) | Multiple projects, worktrees |
| [tmux-fzf-session-switch](https://github.com/thuanOwa/tmux-fzf-session-switch) | Simpler fzf switcher | Lighter alternative |

**sessionx features:**
- Fuzzy search across sessions
- zoxide integration (frecency-based)
- Preview pane layout before switching
- Create new sessions from picker

## Clipboard

| Plugin | What | When to Use |
|--------|------|-------------|
| [tmux-yank](https://github.com/tmux-plugins/tmux-yank) | Copy to system clipboard | Cross-platform, reliable clipboard |

**macOS note:** Modern tmux + macOS may handle clipboard natively. Test first:
1. Enter copy mode (`prefix + [`)
2. Select text, yank (`y`)
3. Paste outside tmux (`cmd + v`)

If it works, yank may be unnecessary. If not, install yank.

## Recommended Setups by Context

### Minimal (new to tmux, simple projects)
- No plugins needed
- Learn basics first, add when pain emerges

### Terminal-centric dev (full-stack, multiple services)
- tpm-redux (manager)
- tmux-resurrect + tmux-continuum (persistence)
- tmux-sessionx (switching)

### Worktree-heavy workflow
- tpm-redux (manager)
- tmux-sessionx (fast switching between worktree sessions)
- Consider: resurrect + continuum if reboots are frequent

## Sources

- [tmux-plugins/list](https://github.com/tmux-plugins/list) - Full plugin list
- [tpm-redux](https://github.com/RyanMacG/tpm-redux) - Maintained plugin manager

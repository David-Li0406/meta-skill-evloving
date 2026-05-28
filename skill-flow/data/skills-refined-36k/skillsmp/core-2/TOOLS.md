# PAI Tool Preferences

**PAI-specific tool choices. Claude knows how to use these tools intrinsically.**

---

## Tool Preference Matrix

| Task | Use This | NOT This | Speed Gain |
|------|----------|----------|------------|
| File search | `fd` | `find` | 13-23x |
| Text search | `rg` | `grep -r` | 10-50x |
| Text replacement | `sd` | `sed -i` | Cross-platform |
| File viewer | `bat` | `cat` | Syntax highlighting |
| Directory listing | `eza` | `ls` | Git-aware, icons |
| Git diffs | `delta` | `diff` | Syntax highlighting |
| JS/TS runtime | `bun` | `node` | 15x startup |
| JS packages | `bun` | `npm/yarn/pnpm` | 15x install |
| Python packages | `uv` | `pip` | 10-100x |
| Benchmarking | `hyperfine` | `time` | Statistical |
| Semantic code | `ast-grep` | `grep` | AST-aware |
| Fuzzy finder | `fzf` | - | Interactive |

---

## Installation Commands

```bash
# Core (Rust-based modern CLI)
cargo install fd-find ripgrep sd bat eza git-delta hyperfine ast-grep

# Interactive
brew install fzf

# JavaScript/TypeScript
curl -fsSL https://bun.sh/install | bash

# Python
curl -LsSf https://astral.sh/uv/install.sh | sh

# Rust toolchain (if needed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

---

## PAI Tool Categories

**Core Infrastructure:**
- Git, Bun, Cargo/Rust

**Modern CLI (prefer over POSIX):**
- fd, rg, sd, bat, eza, delta, fzf, hyperfine

**Development:**
- gh (GitHub CLI), ast-grep, markdownlint-cli2

**AI Agents:**
- Claude Code (primary), Gemini CLI, Grok CLI, Ollama (local)

---

## Quick Verification

```bash
fd --version && rg --version && sd --version && bat --version && eza --version && delta --version && hyperfine --version
```

---

**For detailed tool usage:** Claude knows fd, rg, bat, git, bun APIs intrinsically. Just ask.

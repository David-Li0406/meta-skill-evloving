# The Agentic Shift

Ship features faster with AI-assisted development.

## Install

### Option 1: Claude Plugin (Official)

```bash
/plugin marketplace add vishwastam/the-agentic-shift
/plugin install agentic-shift
```

### Option 2: npm (GitHub-independent)

```bash
npx agentic-shift
```

### Option 3: Manual

```bash
git clone https://github.com/vishwastam/the-agentic-shift.git
cp -r the-agentic-shift/agentic-shift-skill ~/.claude/skills/agentic-shift
```

## Use

```bash
claude /agentic-shift
```

The setup is interactive. It will:
1. Ask about your project and context
2. Create a minimal CLAUDE.md
3. Walk you through your first AI-assisted feature

Takes about 5 minutes.

## What It Does

```
You write spec → Claude asks questions → Claude generates code → You approve
```

That's the core workflow. Optional add-ons (GitHub integration, Figma, security hooks) are offered based on your needs.

## Requirements

- [Claude Code CLI](https://docs.anthropic.com/claude-code) installed
- Authenticated (`claude login`)

## Documentation

The skill is self-contained and interactive—you don't need to read docs to get started.

For reference:
- [LIMITATIONS.md](LIMITATIONS.md) — When AI-assisted dev isn't the right fit
- [ENTERPRISE.md](ENTERPRISE.md) — Compliance, security, large organizations

## Publishing to npm

If you want to publish your own version:

```bash
cd npm-package
npm publish
```

Users can then install with `npx your-package-name`.

## License

MIT

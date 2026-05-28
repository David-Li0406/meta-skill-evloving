# VS Code / Copilot Guidance (Optional)

## Scope
- Agent Skills (open standard): foldered skills with `SKILL.md`.
- VS Code agent/prompt files: user prompts under `~/Library/Application Support/Code/User/prompts`.
- GitHub repo custom instructions: `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md`.
- Prompt files: `*.prompt.md` (public preview).
- Agent instructions: `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` (repo-level).

## Frontmatter checklist (current naming)
- Agent file: `description`, `model`, `tools` (when supported)
- Instructions: `applyTo` (glob string)
- Prompt: `mode` ("agent" or "ask"); optional `tools`

## Agent Skills
- GitHub Copilot supports project skills in `.github/skills` or `.claude/skills`.
- Personal skills live in `~/.copilot/skills` or `~/.claude/skills`.
- GitHub Copilot CLI is public preview; VS Code stable support is rolling out (Insiders first).
- `SKILL.md` requires `name` and `description`; optional `license`.

## Custom instructions (precedence)
- Personal instructions > repository instructions > organization instructions.
- Repository instructions include:
  - Path-specific: `.github/instructions/**/*.instructions.md`
  - Repo-wide: `.github/copilot-instructions.md`
  - Agent instructions: `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`

## Authoring best practices
- Keep prompts tool-specific and concise.
- Prefer editor context and built-in metadata over shell.
- Avoid conflicting guidance across chatmodes and instructions.

## References
- Response customization: [Response customization](https://docs.github.com/en/copilot/concepts/prompting/response-customization?tool=vscode)

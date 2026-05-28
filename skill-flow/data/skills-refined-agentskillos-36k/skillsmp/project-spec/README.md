# Project Spec

Create a project spec for AI agents to work from autonomously. Works with [Claude Code](https://github.com/anthropics/claude-code) (Anthropic), [Codex](https://github.com/openai/codex) (OpenAI), and [Gemini CLI](https://github.com/google-gemini/gemini-cli) (Google).

## Features

- **5-step process** — Explore → Ask → Approaches → Derive → Write
- **7-section structure** — Instructions, Mission, Architecture, Components, Constraints, Build Order, Done When
- **State management** — PLAN.md for the spec, PROGRESS.md for tracking across sessions
- **Anti-filler guidance** — Concrete examples of vague writing to avoid

## Installation

### Claude Code

```bash
mkdir -p ~/.claude/skills/project-spec && curl -o ~/.claude/skills/project-spec/SKILL.md https://raw.githubusercontent.com/ilm-alan/project-spec/main/SKILL.md
```

### Codex

```bash
mkdir -p ~/.codex/skills/project-spec && curl -o ~/.codex/skills/project-spec/SKILL.md https://raw.githubusercontent.com/ilm-alan/project-spec/main/SKILL.md
```

### Gemini CLI

First, enable the experimental skills feature in `~/.gemini/settings.json`:

```json
{
  "experimental": {
    "skills": true
  }
}
```

Then install the skill:

```bash
mkdir -p ~/.gemini/skills/project-spec && curl -o ~/.gemini/skills/project-spec/SKILL.md https://raw.githubusercontent.com/ilm-alan/project-spec/main/SKILL.md
```

Run `/skills list` to verify the skill was loaded.

## Usage

Invoke the skill when starting a new project:

```
/project-spec
```

Or reference it contextually:

```
Using the project spec skill, create a spec for a CLI tool that manages AWS credentials
```

## Structure

Every generated spec contains:

| Section | Purpose |
|---------|---------|
| **Instructions** | How the agent operates autonomously—build without asking, make decisions from code |
| **Mission** | What, who, why in 1-3 lines |
| **Architecture** | Technical decisions stated, not debated |
| **Components** | What to build—one line each |
| **Constraints** | Non-negotiables only |
| **Build Order** | Sequenced phases by name |
| **Done When** | Concrete, testable acceptance criteria |

## Output Files

- `PLAN.md` — The project spec (under 100 lines)
- `PROGRESS.md` — State tracking updated by the executing agent

## Example

**Prompt:**
```
/project-spec
```

**Conversation:**
```
What are you building?
> A CLI tool for rotating AWS access keys

Who is this for?
> DevOps engineers managing multiple AWS accounts

What does "done" look like?
> Keys rotate without downtime, old keys are revoked after confirmation
```

**Output (PLAN.md):**
```markdown
## Instructions
Read PROGRESS.md to know what's done. Check git log for context. Build the next incomplete phase—do not ask what to work on. Make decisions from existing code patterns. Update PROGRESS.md when done and continue to next phase. No clarifying questions—inspect code, make reasonable choices, ship working features.

## Mission
Your job is to build a CLI tool for rotating AWS access keys. For DevOps engineers managing multiple AWS accounts. Eliminates manual key rotation and reduces security risk from stale credentials.

## Architecture
Go binary. AWS SDK for credential operations. Viper for config. No database—uses AWS IAM as source of truth.

## Components
- Key rotator: creates new key, updates configs, revokes old key
- Config manager: reads/writes credential locations from ~/.aws and environment
- Account switcher: handles multiple AWS profiles

## Constraints
- Zero downtime during rotation
- Old key revoked only after new key confirmed working
- Must support assumed roles

## Build Order
1. Config manager
2. Key rotator
3. Account switcher

## Done When
- `rotate` command creates new key, updates all configured locations, revokes old key
- `status` command shows key age across all profiles
- Works with 10+ AWS profiles without performance degradation
```

## License

MIT. See [LICENSE.txt](LICENSE.txt).

## Guidance

Perfection is a continual process.

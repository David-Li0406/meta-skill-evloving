# Common Patterns & Data Reference

Standard conventions and decision guides for adding providers.

## Support Levels

Use these consistently across all 11 primitives:

### `full` - Native, First-Class Support

The provider has built-in, well-documented support for this primitive.

**Examples:**
- Agent Mode in Cursor Editor (native multi-step execution)
- Persistent Instructions in .cursor/instructions.md (first-class config file)
- Tool Integrations in Claude Code (MCP support built-in)

**When to use**: The feature is natively available, documented, and part of the provider's core offering.

### `partial` - Works with Limitations or Workarounds

The provider supports the primitive but with limitations, workarounds, or indirect approaches.

**Examples:**
- Skills in Cursor (via .cursor/rules but not as full as GitHub Copilot)
- Tool Integrations in Cursor (via Extensions API, not full MCP)
- Slash Commands in Cursor (via UI shortcuts, not full custom commands)

**When to use**: The primitive works but requires workarounds, isn't as feature-complete, or needs custom configuration.

### `diy` - DIY (Do It Yourself) Workaround

Not natively available, but users can implement custom configuration to achieve similar functionality.

**Examples:**
- Lifecycle Hooks in Copilot (not available natively, but user can script them)
- Lifecycle Hooks in Cursor (not available, but could be scripted)

**When to use**: The feature isn't built-in but is achievable through custom setup.

### `none` - Not Available

The provider cannot support this primitive in any form.

**Examples:**
- (Rare - most primitives can be emulated somehow)

**When to use**: The primitive is fundamentally incompatible with the provider's architecture.

---

## File Location Conventions

Follow provider-specific patterns for consistency:

### GitHub Copilot

Uses `.github/` directory with standardized naming:

```
.github/
├── copilot-instructions.md          # Repository-level instructions
├── agents/
│   ├── reviewer.agent.md            # Custom agent
│   └── planner.agent.md
├── skills/
│   └── debug-ci/
│       └── SKILL.md                 # Reusable skill
├── prompts/
│   ├── write-tests.prompt.md        # Slash command / prompt
│   └── review-pr.prompt.md
└── instructions/
    ├── frontend.instructions.md     # Path-scoped rules
    └── backend.instructions.md
```

**Global** (user-level):
```
~/.copilot/                           # Copilot global config
~/.github/skills/                     # Global skills
```

### Claude Code

Uses `.claude/` directory with JSON + markdown:

```
.claude/
├── CLAUDE.md                        # Project memory/instructions
├── settings.json                    # Configuration
├── agents/
│   ├── code-reviewer.md             # Custom agent
│   └── planner.md
├── commands/
│   └── commit.md                    # Slash command
├── rules/
│   ├── api-guidelines.md            # Path-scoped rules
│   └── frontend.md
├── skills/
│   └── refactor/
│       └── SKILL.md                 # Reusable skill
└── hooks/
    └── hooks.json                   # Lifecycle hooks
```

**Global** (user-level):
```
~/.claude/                            # Claude global config
~/.claude/CLAUDE.md                   # Global memory
~/.claude/settings.json               # Global settings
~/.claude/agents/                     # Global agents
~/.claude/commands/                   # Global commands
```

### Cursor (New Pattern)

Follows Claude's `.claude/` pattern with `.cursor/` directory:

```
.cursor/
├── instructions.md                  # Project instructions
├── settings.json                    # Configuration
├── agents/
│   └── specialized-agent.md         # Custom agents
├── rules/
│   ├── api-guidelines.md            # Path-scoped rules
│   └── frontend.md
└── extensions/                      # Tool integrations
    └── custom-tools/
```

**Global** (user-level):
```
~/.cursor/                            # Cursor global config
~/.cursor/settings.json               # Global settings
```

---

## Naming Conventions

### File and Directory Names

- **Lowercase with hyphens** for most files: `copilot-instructions.md`, `code-reviewer.md`
- **Folders match content type**: `agents/`, `rules/`, `commands/`, `skills/`
- **SKILL.md** (uppercase) for reusable skill definitions (agentskills convention)
- **CLAUDE.md**, **.cursor/instructions.md** for memory/context files

### Primitive IDs

Used in `primitives.ts` and `comparison.ts` - must be consistent:

```typescript
// Use kebab-case, lowercase
id: 'agent-mode'          // ✓ correct
id: 'agentMode'           // ✗ inconsistent
id: 'Agent Mode'          // ✗ not lowercase
```

### Provider Names in Display Labels

Used in `PrimitiveCard.tsx` and UI:

```typescript
const providerLabels: Record<Provider, string> = {
  copilot: 'GitHub Copilot',        // Full official name
  claude: 'Claude Code',            // Official product name
  cursor: 'Cursor',                 // Simple product name
}
```

---

## Implementation Details: What to Document

For each of the 11 primitives × each provider, document:

### `implementation` (string)

**What**: Concise description of how the provider implements this feature.

**Examples:**
- "Agent mode in Copilot Chat"
- "Agentic workflows in Claude Code"
- "Custom instructions and workflows via .cursor/rules"

**Length**: 1-2 sentences, descriptive but brief

### `location` (string)

**What**: File path or feature name where this is configured/used.

**Examples:**
- "VS Code Copilot Chat" (feature name for UI-based features)
- ".github/copilot-instructions.md" (file path for config)
- "Cursor Editor with Agent capabilities" (feature description)
- ".claude/settings.json" (settings file)
- ".cursor/rules/*.md" (file pattern)

**Pattern**: Follow provider's actual file/folder structure

### `support` (full | partial | diy)

**Decision tree:**

```
Does provider natively support this?
├─ Yes, well-documented, core feature
│  └─ support: 'full'
├─ Yes, but limited or with workarounds
│  └─ support: 'partial'
├─ No, but achievable with custom setup
│  └─ support: 'diy'
└─ No, impossible
   └─ support: 'none'  (rare)
```

---

## Comparison Matrix: Full vs Partial vs None

Quick reference for common feature mappings:

| Primitive | Copilot | Claude | Cursor | Notes |
|-----------|---------|--------|--------|-------|
| **Agent Mode** | `full` | `full` | `full` | All support multi-step execution |
| **Skills** | `full` | `full` | `partial` | Cursor has rules but not full skill system |
| **Tool Integrations** | `full` | `full` | `partial` | Cursor has Extensions API, not full MCP |
| **Persistent Instructions** | `full` | `full` | `full` | All have project-level instructions |
| **Global Instructions** | `full` | `full` | `full` | All support user-level preferences |
| **Path-Scoped Rules** | `full` | `full` | `full` | All support directory-specific rules |
| **Slash Commands** | `full` | `full` | `partial` | Cursor has UI shortcuts, not full custom commands |
| **Custom Agents** | `full` | `full` | `partial` | Cursor has agents but less flexible |
| **Permissions & Guardrails** | `full` | `full` | `partial` | Cursor has safety features, not as comprehensive |
| **Lifecycle Hooks** | `diy` | `full` | `none` | Only Claude has built-in hooks |
| **Verification / Evals** | `full` | `full` | `full` | All support terminal execution for tests |

---

## Emoji Reference

### Comparison Table Column Headers

Used in column headers for visual distinction:

```
GitHub Copilot → 🤖  (robot emoji for automation)
Claude Code    → 🧠  (brain emoji for AI)
Cursor         → ✨  (sparkles emoji for magic)
```

Alternative emojis (if preferred):
- Copilot: 🔧, 💻, 🛠️
- Claude: 🤖, 💡, 🎯
- Cursor: ⚡, 🎨, 🚀

### Interactive File Tree Provider Tabs

Used in `FileTree.tsx` component for provider selection:

```
GitHub Copilot → 🤖  (robot - consistent with comparison table)
Claude Code    → 🧠  (brain - consistent with comparison table)
Cursor         → ➤   (arrow - direction/flow, alternative to ✨)
```

Alternative emojis for File Tree tabs:
- Arrow variants: ➤, ▶, →, ⇒
- Direction: 🎯, ⚡, 🚀
- Editor: 💻, ⚙️, 🔧

**Note:** File Tree icons can differ from comparison table icons if desired. Choose based on visual balance and readability in the UI.

---

## TypeScript Patterns

### Provider Type

```typescript
export type Provider = 'copilot' | 'claude' | 'cursor'
```

Add new providers as literal union types, not enum (more flexible).

### Provider Implementations

```typescript
interface ProviderImplementation {
  provider: Provider              // Must match the type
  implementation: string          // How it works
  location: string               // Where it's configured
  support: 'full' | 'partial' | 'diy'
}
```

### Comparison Row

```typescript
interface ComparisonRow {
  primitiveId: string
  primitiveName: string
  [provider: Provider]: ProviderSupport
  // Type-safe way to add providers:
  // copilot: ProviderSupport
  // claude: ProviderSupport
  // cursor: ProviderSupport
}
```

---

## Common Research Questions

When adding a provider, research these questions:

### Agent Mode
- Does the provider have multi-step execution?
- Where is it accessed? (UI, CLI, config)
- What is it called in the provider's documentation?

### Skills/Workflows
- Can users create reusable procedures?
- What format? (markdown, JSON, YAML)
- Where are they stored?
- Are there examples?

### Tool Integrations
- Does it support MCP (Model Context Protocol)?
- What other tool/API integration methods exist?
- How are integrations configured?
- Are there limitations?

### Instructions
- Can users set project-level instructions? (persistent)
- Can users set personal/global instructions?
- Format? (markdown, JSON, plain text)
- Where are they stored?

### Path-Scoped Rules
- Can instructions apply to specific directories?
- How are patterns specified? (glob, regex)
- Format of scoping syntax?

### Slash Commands
- Can users create custom commands?
- Are there built-in commands?
- How are they invoked?
- Format? (markdown with frontmatter, YAML)

### Custom Agents
- Can users define agent personas/roles?
- Can agents have different capabilities?
- Format? (markdown, JSON)
- Examples?

### Permissions & Guardrails
- Can users restrict what the AI can do?
- Allow/deny lists? Approval workflows?
- Scope of restrictions?
- Documentation?

### Lifecycle Hooks
- Can custom code run before/after operations?
- What events trigger hooks?
- Supported languages? (bash, JavaScript, etc.)
- Documentation?

### Verification/Evals
- How does the provider verify outputs?
- Can users run tests/linting?
- Integration with CI/CD?
- What tools does it support?

---

## Checklist: Naming & Consistency

Before committing provider data:

- [ ] Provider name appears consistently in all 3 files:
  - [ ] `primitives.ts` (Provider type + implementations)
  - [ ] `fileTree.ts` (Provider type)
  - [ ] `comparison.ts` (ComparisonRow interface)
- [ ] All 11 primitives have provider entries
- [ ] All 11 comparison rows have provider field
- [ ] Support levels are consistent (primitives.ts ↔ comparison.ts)
- [ ] File locations follow provider's naming conventions
- [ ] Provider display name is added to PrimitiveCard labels
- [ ] combineWith references only valid primitives
- [ ] No typos in ids, implementations, locations
- [ ] TypeScript compiles without errors

---

## Updating Existing Providers

If you need to update an existing provider (e.g., Cursor gains new features):

1. Update `primitives.ts` - change support level and implementation details
2. Update `comparison.ts` - change level and implementation details
3. Update `fileTree.ts` if new file locations were added
4. Update E2E tests if support badge counts changed
5. Regenerate llms-full.txt
6. Create semantic commit message with scope: `feat(data): update cursor support for Tool Integrations`

All files must stay in sync - if you miss any, TypeScript will catch it.

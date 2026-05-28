# Code Examples: Copy-Paste Templates

Ready-to-use code snippets for each stream. Customize as needed.

## Stream 1: Type System Updates

### Add to Provider Union Type

**File**: `site/src/data/primitives.ts`

```typescript
export type Provider = 'copilot' | 'claude' | 'cursor'
```

**File**: `site/src/data/fileTree.ts`

```typescript
export type Provider = 'copilot' | 'claude' | 'cursor'
```

### Update Comparison Interface

**File**: `site/src/data/comparison.ts`

```typescript
export interface ComparisonRow {
  /** Primitive ID (matches primitives.ts) */
  primitiveId: string
  /** Primitive display name */
  primitiveName: string
  /** GitHub Copilot implementation */
  copilot: ProviderSupport
  /** Claude Code implementation */
  claude: ProviderSupport
  /** Cursor implementation */
  cursor: ProviderSupport
}
```

### Update Provider Labels

**File**: `site/src/components/PrimitiveCards/PrimitiveCard.tsx`

```typescript
const providerLabels: Record<Provider, string> = {
  copilot: 'GitHub Copilot',
  claude: 'Claude Code',
  cursor: 'Cursor',
}
```

---

## Stream 2: Data Layer Updates

### Add Provider Implementation (Repeat for All 11 Primitives)

**File**: `site/src/data/primitives.ts`

```typescript
{
  id: 'agent-mode',
  name: 'Agent Mode',
  description: 'Multi-step execution with planning and tool use.',
  whatItIs: 'A mode where the AI can plan and execute over multiple steps...',
  useWhen: [
    'The task spans multiple files',
    'You need iterative debugging',
    'You want the system to keep working until done',
  ],
  prevents: '"One-shot" incomplete solutions that require manual follow-up',
  combineWith: ['Skills', 'Tools', 'Verification'],
  implementations: [
    {
      provider: 'copilot',
      implementation: 'Agent mode in Copilot Chat',
      location: 'VS Code Copilot Chat',
      support: 'full',
    },
    {
      provider: 'claude',
      implementation: 'Agentic workflows in Claude Code',
      location: 'Claude Code CLI',
      support: 'full',
    },
    {
      provider: 'cursor',
      implementation: 'Cursor Agent mode for multi-step execution',
      location: 'Cursor Editor with Agent capabilities',
      support: 'full',
    },
  ],
  category: 'execution',
}
```

### Add Provider Row (Repeat for All 11 Primitives)

**File**: `site/src/data/comparison.ts`

```typescript
{
  primitiveId: 'agent-mode',
  primitiveName: 'Agent Mode',
  copilot: {
    level: 'full',
    implementation: 'Agent mode in Copilot Chat',
    location: 'VS Code Copilot Chat',
  },
  claude: {
    level: 'full',
    implementation: 'Agentic workflows in Claude Code',
    location: 'Claude Code CLI',
  },
  cursor: {
    level: 'full',
    implementation: 'Cursor Agent mode for multi-step execution',
    location: 'Cursor Editor with Agent capabilities',
  },
}
```

### Add File Tree Structure

**File**: `site/src/data/fileTree.ts`

```typescript
export const cursorTree: FileNode = {
  id: 'cursor-root',
  name: 'my-project',
  type: 'folder',
  children: [
    {
      id: 'cursor-dotcursor',
      name: '.cursor',
      type: 'folder',
      children: [
        {
          id: 'cursor-instructions',
          name: 'instructions.md',
          type: 'file',
          details: {
            label: 'Project Instructions',
            description: 'Cursor project-level instructions for AI behavior.',
            whatGoesHere: [
              'Project overview and tech stack',
              'Coding conventions',
              'How to build and test',
            ],
            whenLoaded: 'Always loaded first. Forms the baseline for Cursor interactions.',
            loadOrder: 1,
            example: `# Cursor Instructions

## Project Setup
- Node.js 18+
- npm install

## Conventions
- TypeScript strict mode
- Functional components`,
          },
        },
        {
          id: 'cursor-rules',
          name: 'rules',
          type: 'folder',
          children: [
            {
              id: 'cursor-rule-frontend',
              name: 'frontend.md',
              type: 'file',
              details: {
                label: 'Path-Specific Rule',
                description: 'Rules applying to specific directories.',
                whatGoesHere: [
                  'Directory-specific conventions',
                  'Framework guidance',
                ],
                whenLoaded: 'Loaded when working on matching paths.',
                loadOrder: 2,
                example: `# Frontend Rules

- Use React hooks
- Test with React Testing Library`,
              },
            },
          ],
        },
      ],
    },
  ],
}

export const cursorGlobalTree: FileNode = {
  id: 'cursor-global-root',
  name: '~',
  type: 'folder',
  children: [
    {
      id: 'cursor-global-dotcursor',
      name: '.cursor',
      type: 'folder',
      children: [
        {
          id: 'cursor-global-settings',
          name: 'settings.json',
          type: 'file',
          details: {
            label: 'Global Settings',
            description: 'Personal Cursor settings across all projects.',
            whatGoesHere: [
              'Default preferences',
              'Model selection',
              'Theme settings',
            ],
            whenLoaded: 'Always loaded. Applies globally.',
            loadOrder: 1,
            example: `{
  "theme": "dark",
  "fontSize": 14
}`,
          },
        },
      ],
    },
  ],
}

// Update the mapping objects:
export const trees: Record<Provider, FileNode> = {
  copilot: copilotTree,
  claude: claudeTree,
  cursor: cursorTree,
}

export const globalTrees: Record<Provider, FileNode> = {
  copilot: copilotGlobalTree,
  claude: claudeGlobalTree,
  cursor: cursorGlobalTree,
}
```

---

## Stream 3: UI Component Updates

### Add Column Header

**File**: `site/src/components/ProviderComparison/ComparisonTable.tsx`

```typescript
<thead>
  <tr className="bg-secondary/50">
    <th className="px-4 py-3 text-left text-sm font-semibold text-foreground">
      Primitive
    </th>
    <th className="px-4 py-3 text-center text-sm font-semibold text-foreground">
      <span className="inline-flex items-center gap-2">
        <span aria-hidden="true">🤖</span>
        GitHub Copilot
      </span>
    </th>
    <th className="px-4 py-3 text-center text-sm font-semibold text-foreground">
      <span className="inline-flex items-center gap-2">
        <span aria-hidden="true">🧠</span>
        Claude Code
      </span>
    </th>
    <th className="px-4 py-3 text-center text-sm font-semibold text-foreground">
      <span className="inline-flex items-center gap-2">
        <span aria-hidden="true">✨</span>
        Cursor
      </span>
    </th>
  </tr>
</thead>
```

### Add Table Cell

```typescript
<tbody className="divide-y divide-border">
  {comparisonData.map((row) => (
    <>
      <tr className={...}>
        <td className="px-4 py-3">
          {/* Primitive name */}
        </td>
        <td className="px-4 py-3 text-center">
          <SupportBadge level={row.copilot.level} />
        </td>
        <td className="px-4 py-3 text-center">
          <SupportBadge level={row.claude.level} />
        </td>
        <td className="px-4 py-3 text-center">
          <SupportBadge level={row.cursor.level} />
        </td>
      </tr>
    </>
  ))}
</tbody>
```

### Update Expanded Row

```typescript
function ExpandedRow({ row }: ExpandedRowProps): VNode {
  const [copiedLocation, setCopiedLocation] = useState<'copilot' | 'claude' | 'cursor' | null>(null)

  const handleCopy = async (provider: 'copilot' | 'claude' | 'cursor', location: string) => {
    try {
      await navigator.clipboard.writeText(location)
      setCopiedLocation(provider)
      setTimeout(() => { setCopiedLocation(null) }, 2000)
    } catch {
      // Clipboard not available
    }
  }

  return (
    <tr className="bg-secondary/30">
      <td colSpan={4} className="px-4 py-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Copilot details */}
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-foreground">GitHub Copilot</h4>
            <p className="text-sm text-muted-foreground">{row.copilot.implementation}</p>
            <div className="flex items-center gap-2">
              <code className="flex-1 text-xs bg-background px-2 py-1.5 rounded font-mono...">
                {row.copilot.location}
              </code>
              <button onClick={() => { void handleCopy('copilot', row.copilot.location) }}>
                {/* icon */}
              </button>
            </div>
          </div>

          {/* Claude details */}
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-foreground">Claude Code</h4>
            <p className="text-sm text-muted-foreground">{row.claude.implementation}</p>
            <div className="flex items-center gap-2">
              <code className="flex-1 text-xs bg-background px-2 py-1.5 rounded font-mono...">
                {row.claude.location}
              </code>
              <button onClick={() => { void handleCopy('claude', row.claude.location) }}>
                {/* icon */}
              </button>
            </div>
          </div>

          {/* Cursor details */}
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-foreground">Cursor</h4>
            <p className="text-sm text-muted-foreground">{row.cursor.implementation}</p>
            <div className="flex items-center gap-2">
              <code className="flex-1 text-xs bg-background px-2 py-1.5 rounded font-mono...">
                {row.cursor.location}
              </code>
              <button onClick={() => { void handleCopy('cursor', row.cursor.location) }}>
                {/* icon */}
              </button>
            </div>
          </div>
        </div>
      </td>
    </tr>
  )
}
```

---

## Stream 4: Testing

### Header Test

**File**: `site/tests/e2e/comparison.spec.ts`

```typescript
test('should display table headers', async ({ page }) => {
  await expect(page.getByRole('columnheader', { name: /Primitive/i })).toBeVisible()
  await expect(page.getByRole('columnheader', { name: /GitHub Copilot/i })).toBeVisible()
  await expect(page.getByRole('columnheader', { name: /Claude Code/i })).toBeVisible()
  await expect(page.getByRole('columnheader', { name: /Cursor/i })).toBeVisible()
})
```

### Support Badge Test

```typescript
test('should display support level badges', async ({ page }) => {
  const table = page.getByRole('table')
  await expect(table.getByText('Full Support').first()).toBeVisible()

  const fullSupportBadges = table.getByText('Full Support')
  await expect(fullSupportBadges).toHaveCount(18)  // Adjust based on provider

  const partialBadges = table.getByText('Partial')
  await expect(partialBadges).toHaveCount(5)  // Adjust based on provider
})
```

### Expansion Tests

```typescript
test('should expand row on click to show details', async ({ page }) => {
  const table = page.getByRole('table')
  const row = table.getByRole('row').filter({ hasText: 'Persistent Instructions' }).first()
  await row.click()

  await expect(page.getByText('Repo instructions file')).toBeVisible()
  await expect(page.getByText('Project memory file with @imports')).toBeVisible()
  await expect(page.getByText('Project instructions file')).toBeVisible()
})

test('should show file locations when expanded', async ({ page }) => {
  const table = page.getByRole('table')
  const row = table.getByRole('row').filter({ hasText: 'Persistent Instructions' }).first()
  await row.click()

  await expect(page.getByText('.github/copilot-instructions.md')).toBeVisible()
  await expect(page.getByText('CLAUDE.md').first()).toBeVisible()
  await expect(page.getByText('.cursor/instructions.md')).toBeVisible()
})

test('should have copy buttons in expanded row', async ({ page }) => {
  const table = page.getByRole('table')
  const row = table.getByRole('row').filter({ hasText: 'Persistent Instructions' }).first()
  await row.click()

  const copyButtons = page.getByRole('button', { name: /Copy location/i })
  await expect(copyButtons.nth(0)).toBeVisible()
  await expect(copyButtons.nth(1)).toBeVisible()
  await expect(copyButtons.nth(2)).toBeVisible()
})
```

---

## Stream 5: App Integration

### Update App.tsx

**File**: `site/src/App.tsx`

```typescript
<Section
  id="comparison"
  title="Provider Comparison"
  description="Compare how primitives are implemented across GitHub Copilot, Claude Code, and Cursor."
>
  <ProviderComparisonSection />
</Section>
```

### Update Hero.tsx

**File**: `site/src/components/Hero/Hero.tsx`

```typescript
<p className="text-xl text-muted-foreground max-w-2xl mb-6">
  Configure GitHub Copilot, Claude Code, and Cursor for any role or workflow.
  Explore the primitives that unlock their full potential, then learn how to{' '}
  <a href="https://thisistheway.to/ai" className="underline hover:text-foreground transition-colors">
    improve AI agents through systematic failure analysis
  </a>.
</p>
```

### Update README.md

**File**: `README.md`

```markdown
## What's Here

- **AI Primitives** — The 11 core configuration primitives (instructions, skills, agents, commands, etc.) that power AI coding assistants
- **Interactive File Tree** — Visual guide to where config files live, for both global (user home) and project-level configuration
- **Provider Comparison** — Side-by-side comparison of GitHub Copilot, Claude Code, and Cursor support for each primitive

## Key Paths

### GitHub Copilot

| Type | Path |
|------|------|
| Global skills | `~/.copilot/skills/` or `~/.github/skills/` |
| Project instructions | `.github/copilot-instructions.md` |
| Project skills | `.github/skills/<skill-name>/SKILL.md` |
| Project agents | `.github/agents/<name>.agent.md` |

### Claude Code

| Type | Path |
|------|------|
| Global config | `~/.claude/` |
| Global memory | `~/.claude/CLAUDE.md` |
| Global commands | `~/.claude/commands/<name>.md` |
| Project memory | `./CLAUDE.md` or `.claude/CLAUDE.md` |
| Project settings | `.claude/settings.json` |

### Cursor

| Type | Path |
|------|------|
| Global settings | `~/.cursor/settings.json` |
| Project instructions | `.cursor/instructions.md` |
| Project rules | `.cursor/rules/<name>.md` |
```

---

## Stream 6: LLMs Generation

### Update Generation Script (if needed)

**File**: `.github/skills/generate-llms/scripts/generate-llms-full.ts`

```typescript
// Look for the provider name mapping around line 583
${p.implementations.map((impl: any) => {
  const providerName =
    impl.provider === 'copilot' ? 'GitHub Copilot' :
    impl.provider === 'claude' ? 'Claude Code' :
    impl.provider === 'cursor' ? 'Cursor' :
    impl.provider;
  return `| ${providerName} | ${impl.implementation} | ${impl.location} | ${impl.support} |`
}).join('\n')}
```

---

## Reference: All 11 Primitives

Use this checklist when adding implementation data. All 11 must be included:

1. **Agent Mode** (Execution)
2. **Skills / Workflows** (Execution)
3. **Tool Integrations (MCP)** (Execution)
4. **Persistent Instructions** (Customization)
5. **Global Instructions** (Customization)
6. **Path-Scoped Rules** (Customization)
7. **Slash Commands** (Customization)
8. **Custom Agents** (Control)
9. **Permissions & Guardrails** (Control)
10. **Lifecycle Hooks** (Control)
11. **Verification / Evals** (Control)

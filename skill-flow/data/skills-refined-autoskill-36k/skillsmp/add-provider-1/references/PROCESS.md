# Detailed Process: Adding a Provider

Complete step-by-step instructions for all 6 work streams.

## Stream 1: Type System Updates (2-4 hours)

**No dependencies, can start immediately**

### 1.1 Add to Provider Union Type

Edit `site/src/data/primitives.ts`:

```typescript
// Change from:
export type Provider = 'copilot' | 'claude'

// To:
export type Provider = 'copilot' | 'claude' | 'cursor'
```

Edit `site/src/data/fileTree.ts`:

```typescript
// Change from:
export type Provider = 'copilot' | 'claude'

// To:
export type Provider = 'copilot' | 'claude' | 'cursor'
```

### 1.2 Update Comparison Interface

Edit `site/src/data/comparison.ts`:

```typescript
export interface ComparisonRow {
  primitiveId: string
  primitiveName: string
  copilot: ProviderSupport
  claude: ProviderSupport
  cursor: ProviderSupport  // Add this
}
```

### 1.3 Update UI Provider Labels

Edit `site/src/components/PrimitiveCards/PrimitiveCard.tsx`:

```typescript
const providerLabels: Record<Provider, string> = {
  copilot: 'GitHub Copilot',
  claude: 'Claude Code',
  cursor: 'Cursor',  // Add this
}
```

### 1.4 Verify TypeScript

```bash
npm run typecheck
```

You'll see errors about missing provider data - this is expected. Continue to Stream 2.

---

## Stream 2: Data Layer Updates (4-6 hours)

**Depends on Stream 1 - must have types in place**

### 2.0 Research Phase: Verify Provider Capabilities

⚠️ **CRITICAL**: Before adding implementation data, verify against the provider's official documentation.

**Steps:**

1. **Visit official provider documentation**
   - Example: cursor.com/docs, claude.ai, github.com/features/copilot

2. **For each of the 11 primitives, research and document:**
   - Does the provider support this feature natively?
   - What are the official file locations? (e.g., `.cursor/instructions.md`, not guesses)
   - Are there any limitations or workarounds?
   - What version/channel is it available in? (e.g., nightly vs stable)
   - What does the provider call this feature in their docs?

3. **Document findings before coding**
   - Create a research summary with answers to the above
   - This prevents adding outdated or incorrect support levels
   - Reference official docs in your research notes

**Example research record:**
```
Agent Mode: ✓ Full support
  - Called "Agent mode" in Cursor Editor
  - Docs: cursor.com/docs/agent/modes
  - Available in: Stable release
  - Config: Enabled in editor settings
  - Limitations: None observed

Tool Integrations (MCP): ✓ Full support
  - Uses .cursor/mcp.json (project) or ~/.cursor/mcp.json (global)
  - Docs: cursor.com/docs/context/mcp
  - Supports: stdio, SSE, HTTP transports
  - Note: Requires manual configuration
```

### 2.1 Add Provider Implementations to All 11 Primitives

Edit `site/src/data/primitives.ts`:

For each of the 11 primitives, add a new entry to the `implementations` array:

```typescript
implementations: [
  {
    provider: 'copilot',
    implementation: '...',
    location: '...',
    support: 'full',
  },
  {
    provider: 'claude',
    implementation: '...',
    location: '...',
    support: 'full',
  },
  {
    provider: 'cursor',  // Add new entry
    implementation: 'Cursor Agent mode for multi-step execution',
    location: 'Cursor Editor with Agent capabilities',
    support: 'full',  // 'full' | 'partial' | 'diy'
  },
]
```

**Research guide for each primitive:**
1. How does the provider implement this primitive?
2. Where are the config files? (.cursor/instructions.md, etc.)
3. Is support native (full), limited (partial), or via custom setup (diy)?

**Support level decision tree** (see [PATTERNS.md](PATTERNS.md#support-levels) for detailed explanations):

```
Does provider natively support this?
├─ Yes, well-documented, core feature
│  └─ support: 'full'
├─ Yes, but limited or with workarounds
│  └─ support: 'partial'
├─ No, but achievable with custom setup
│  └─ support: 'diy'
└─ No, impossible
   └─ support: 'none' (rare)
```

All 11 primitives:
- Agent Mode
- Skills / Workflows
- Tool Integrations (MCP)
- Persistent Instructions
- Global Instructions
- Path-Scoped Rules
- Slash Commands
- Custom Agents
- Permissions & Guardrails
- Lifecycle Hooks
- Verification / Evals

### 2.2 Add Provider Data to Comparison Matrix

Edit `site/src/data/comparison.ts`:

For each of the 11 `ComparisonRow` entries, add cursor field:

```typescript
{
  primitiveId: 'agent-mode',
  primitiveName: 'Agent Mode',
  copilot: { level: 'full', implementation: '...', location: '...' },
  claude: { level: 'full', implementation: '...', location: '...' },
  cursor: {  // Add this
    level: 'full',  // 'full' | 'partial' | 'none'
    implementation: 'Cursor Agent mode for multi-step execution',
    location: 'Cursor Editor with Agent capabilities',
  },
}
```

### 2.3 Add File Tree Structure

Edit `site/src/data/fileTree.ts`:

Create global and project-level file trees for the provider:

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
            description: 'Cursor project-level instructions.',
            whatGoesHere: ['Project overview', 'Coding standards', 'Build commands'],
            whenLoaded: 'Always loaded first.',
            loadOrder: 1,
            example: '# Cursor Instructions\n\n## Setup\n...',
          },
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
    // Global config structure
  ],
}

// Update the mappings:
export const trees: Record<Provider, FileNode> = {
  copilot: copilotTree,
  claude: claudeTree,
  cursor: cursorTree,  // Add
}

export const globalTrees: Record<Provider, FileNode> = {
  copilot: copilotGlobalTree,
  claude: claudeGlobalTree,
  cursor: cursorGlobalTree,  // Add
}
```

#### File Tree Completeness Guidelines

⚠️ **CRITICAL**: The file tree is educational/reference material that demonstrates provider capabilities to users. Sparse file trees make providers look incomplete even if they have full support.

**How to build comprehensive file trees:**

1. **Demonstrate ALL supported primitives with concrete examples**
   - If the provider has full support for Skills, show 2-3 skill examples
   - If the provider has full support for Custom Agents, show 2-3 agent examples
   - If the provider has full support for Slash Commands, show 2-3 command examples
   - Include examples for: hooks, MCP config, path-scoped rules, etc.

2. **Include both project-level AND global-level examples**
   - Project tree: `.cursor/agents/`, `.cursor/skills/`, etc.
   - Global tree: `~/.cursor/agents/`, `~/.cursor/skills/`, etc.
   - Global examples show workflows users can reuse across all projects

3. **Add nested directory examples**
   - Show `frontend/.cursor/instructions.md` and `backend/.cursor/instructions.md`
   - Demonstrates path-scoped configuration
   - Makes file tree feel realistic and practical

4. **Use exact syntax from official documentation**
   - Check each primitive's official docs page for:
     - File naming conventions (e.g., `SKILL.md` vs `skill.md`)
     - Frontmatter fields (e.g., Cursor agents support `model`, `readonly`, `is_background`)
     - Configuration format (e.g., `.cursor/hooks.json` vs `.cursor/hooks/hooks.json`)
   - Don't guess or copy from other providers—syntax varies

5. **Provide realistic, helpful examples**
   - Examples should be practical (e.g., "debug-ci" skill, "code-reviewer" agent)
   - Include complete example content with proper formatting
   - Show what goes in `whatGoesHere`, `whenLoaded`, and `example` fields

6. **Verify parity with other providers**
   - Compare line counts: `wc -l site/src/data/fileTree.ts`
   - Compare demonstrated primitives: count how many types each provider shows
   - If one provider has 300+ lines and yours has 60 lines, investigate why
   - Example: Cursor tree was initially 64 lines (2 primitives) vs Copilot 386 lines (7 primitives)—this made Cursor look incomplete despite having 11/11 full support

**Research sources for file tree examples:**
- Provider's official "Configuration" or "Setup" docs
- Provider's docs for each primitive (skills, agents, commands, hooks, MCP)
- Example repositories or templates from the provider
- Community examples (verify against official docs)

**Common file tree documentation pages:**
- Commands: `{provider}.com/docs/context/commands`
- Skills: `{provider}.com/docs/context/skills`
- Agents: `{provider}.com/docs/context/agents` or `/context/subagents`
- MCP: `{provider}.com/docs/context/mcp` or `/mcp`
- Hooks: `{provider}.com/docs/agent/hooks` or `/lifecycle`

### 2.4 Verify TypeScript

```bash
npm run typecheck
```

Should have no errors now.

---

## Stream 3: UI Component Updates (4-8 hours)

**Depends on Streams 1 & 2**

### 3.1 Update Comparison Table

Edit `site/src/components/ProviderComparison/ComparisonTable.tsx`:

Add provider column header:

```typescript
<th className="px-4 py-3 text-center text-sm font-semibold text-foreground">
  <span className="inline-flex items-center gap-2">
    <span aria-hidden="true">✨</span>
    Cursor
  </span>
</th>
```

Add provider cell to table rows:

```typescript
<td className="px-4 py-3 text-center">
  <SupportBadge level={row.cursor.level} />
</td>
```

Update `ExpandedRow` state typing:

```typescript
const [copiedLocation, setCopiedLocation] = useState<'copilot' | 'claude' | 'cursor' | null>(null)

const handleCopy = async (provider: 'copilot' | 'claude' | 'cursor', location: string) => {
  // ... existing logic
}
```

Update `ExpandedRow` to show provider details:

```typescript
<tr className="bg-secondary/30">
  <td colSpan={4} className="px-4 py-4">  {/* Change from colSpan={3} */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">  {/* Change from md:grid-cols-2 */}
      {/* Copilot details */}
      {/* Claude details */}
      {/* Add Cursor details */}
      <div className="space-y-2">
        <h4 className="text-sm font-semibold text-foreground">Cursor</h4>
        <p className="text-sm text-muted-foreground">{row.cursor.implementation}</p>
        <div className="flex items-center gap-2">
          <code className="flex-1 text-xs bg-background px-2 py-1.5 rounded font-mono...">
            {row.cursor.location}
          </code>
          <button onClick={() => { void handleCopy('cursor', row.cursor.location) }}>
            {/* copy button JSX */}
          </button>
        </div>
      </div>
    </div>
  </td>
</tr>
```

### 3.2 Add Provider Tab to Interactive File Tree

Edit `site/src/components/FileTree/FileTree.tsx`:

Add provider to the providers array at the top of the component:

```typescript
const providers: { id: Provider; label: string; icon: string }[] = [
  { id: 'copilot', label: 'GitHub Copilot', icon: '🤖' },
  { id: 'claude', label: 'Claude Code', icon: '🧠' },
  { id: 'cursor', label: 'Cursor', icon: '➤' },  // Add this line
]
```

This allows users to switch between providers in the Interactive File Tree visualization on the homepage. The icon helps distinguish the provider visually.

**Icon suggestions** (if different from above):
- Arrow: ➤, ▶, →
- Editor: ✨, 💻, ⚙️
- Action: ⚡, 🎯, 🚀

---

## Stream 4: Testing (3-4 hours)

**Depends on Stream 3**

### 4.1 Update E2E Tests

Edit `site/tests/e2e/comparison.spec.ts`:

Add provider to header test:

```typescript
test('should display table headers', async ({ page }) => {
  await expect(page.getByRole('columnheader', { name: /Cursor/i })).toBeVisible()
})
```

Update support badge count test (adjust numbers based on provider support):

```typescript
test('should display support level badges', async ({ page }) => {
  const fullSupportBadges = table.getByText('Full Support')
  await expect(fullSupportBadges).toHaveCount(18)  // Adjust

  const partialBadges = table.getByText('Partial')
  await expect(partialBadges).toHaveCount(5)  // Adjust
})
```

Add provider to expansion test:

```typescript
test('should expand row on click to show details', async ({ page }) => {
  // ...
  await expect(page.getByText('Project instructions file')).toBeVisible()  // Cursor
})

test('should show file locations when expanded', async ({ page }) => {
  // ...
  await expect(page.getByText('.cursor/instructions.md')).toBeVisible()
})

test('should have copy buttons in expanded row', async ({ page }) => {
  const copyButtons = page.getByRole('button', { name: /Copy location/i })
  await expect(copyButtons.nth(0)).toBeVisible()  // Copilot
  await expect(copyButtons.nth(1)).toBeVisible()  // Claude
  await expect(copyButtons.nth(2)).toBeVisible()  // Cursor
})
```

### 4.2 Run Tests

```bash
npm run test
```

All tests should pass.

---

## Stream 5: App Integration (1-2 hours)

**No hard dependency, can run in parallel with Streams 3-4**

### 5.1 Update Site Copy

Edit `site/src/App.tsx`:

```typescript
<Section
  id="comparison"
  title="Provider Comparison"
  description="Compare how primitives are implemented across GitHub Copilot, Claude Code, and Cursor."
>
```

Edit `site/src/components/Hero/Hero.tsx`:

```typescript
Configure GitHub Copilot, Claude Code, and Cursor for any role or workflow.
```

### 5.2 Update Documentation

Edit `README.md`:

Update primitive count:
```markdown
- **AI Primitives** — The 11 core configuration primitives...
```

Update provider comparison description:
```markdown
- **Provider Comparison** — Side-by-side comparison of GitHub Copilot, Claude Code, and Cursor...
```

Add provider section:
```markdown
### Cursor

| Type | Path |
|------|------|
| Global settings | `~/.cursor/settings.json` |
| Project instructions | `.cursor/instructions.md` |
| Project rules | `.cursor/rules/*.md` |
```

---

## Stream 6: LLMs Generation (1-2 hours)

**Depends on all previous streams**

### 6.1 Update Generation Script (if needed)

Check `.github/skills/generate-llms/scripts/generate-llms-full.ts` for provider name mapping:

```typescript
// If using a ternary that only handles copilot/claude:
const providerName =
  impl.provider === 'copilot' ? 'GitHub Copilot' :
  impl.provider === 'claude' ? 'Claude Code' :
  impl.provider === 'cursor' ? 'Cursor' :
  impl.provider;
```

### 6.2 Regenerate Machine-Readable Files (CRITICAL - Final Step)

⚠️ **This must be the final step after all other streams complete.**

Run the generation script to sync all provider data:

```bash
bun .github/skills/generate-llms/scripts/generate-llms-full.ts
```

**Why this is critical:**
- Pulls data from updated `primitives.ts`, `comparison.ts`, and `fileTree.ts`
- Generates machine-readable files for AI agents to consume
- Keeps llms.txt/llms-full.txt in sync with UI data
- Missing this step = outdated documentation for AI tool consumption

**What gets regenerated:**
- `site/public/llms-full.txt` - Complete content for all primitives
- `site/public/llms.txt` - Table of contents
- `site/public/skills.md`, `site/public/agents.md`, `site/public/mcp.md` - Page-specific markdown

### 6.3 Verify Output

```bash
grep -A 3 "Agent Mode" site/public/llms-full.txt
```

Should show your provider correctly:
```
| Cursor | Cursor Agent mode... | Cursor Editor... | full |
```

### 6.4 Build and Test

```bash
npm run typecheck
npm run test
npm run build
```

All should succeed.

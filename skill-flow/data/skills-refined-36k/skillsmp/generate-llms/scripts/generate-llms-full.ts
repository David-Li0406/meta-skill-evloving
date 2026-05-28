#!/usr/bin/env bun
/**
 * Generate llms.txt and llms-full.txt files from site data
 * 
 * Usage: bun .claude/skills/generate-llms/scripts/generate-llms-full.ts
 * 
 * Reads from the page registry (site/src/data/pages.ts) and generates:
 * - site/public/llms.txt (table of contents)
 * - site/public/llms-full.txt (complete content)
 * - site/public/*.md (page-specific markdown files)
 */

import { writeFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

// Get the project root (assuming script is in .claude/skills/generate-llms/scripts/)
const __dirname = dirname(fileURLToPath(import.meta.url))
const projectRoot = join(__dirname, '../../../..')
const dataDir = join(projectRoot, 'site/src/data')
const publicDir = join(projectRoot, 'site/public')

// Types
interface PageMeta {
  slug: string
  title: string
  description: string
  features?: string
  dataFile?: string
  mdFile?: string
  partNumber?: number
}

// Dynamic imports for TypeScript data files
async function loadData() {
  const primitives = await import(join(dataDir, 'primitives.ts'))
  const comparison = await import(join(dataDir, 'comparison.ts'))
  const skillsTutorial = await import(join(dataDir, 'skillsTutorial.ts'))
  const skillExamples = await import(join(dataDir, 'skillExamples.ts'))
  const agentsTutorial = await import(join(dataDir, 'agentsTutorial.ts'))
  const mcpTutorial = await import(join(dataDir, 'mcpTutorial.ts'))
  const pagesRegistry = await import(join(dataDir, 'pages.ts'))
  
  return {
    // Page registry
    pages: pagesRegistry.pages as readonly PageMeta[],
    // Primitives & comparison (homepage)
    primitives: primitives.primitives,
    categories: primitives.categories,
    comparisonData: comparison.comparisonData,
    // Skills tutorial
    tutorialSections: skillsTutorial.tutorialSections,
    skillExamples: skillExamples.skillExamples,
    // Agents tutorial
    agentsTocItems: agentsTutorial.tocItems,
    agentsCodeSamples: agentsTutorial.codeSamples,
    agentsFurtherReadingLinks: agentsTutorial.furtherReadingLinks,
    // MCP tutorial
    mcpTocItems: mcpTutorial.tocItems,
    mcpCodeSamples: mcpTutorial.codeSamples,
    mcpFurtherReadingLinks: mcpTutorial.furtherReadingLinks,
  }
}

function generateLlmsTxt(pages: readonly PageMeta[]): string {
  // Generate pages list
  const pagesList = [
    '- [Homepage](https://agentconfig.org/): AI primitives reference, interactive file tree, provider comparison matrix',
    ...pages.map(p => `- [${p.title}](https://agentconfig.org/${p.slug}): ${p.description}`)
  ].join('\n')

  // Generate docs list
  const docsList = [
    '- [Full site content](/llms-full.txt): Complete content for deep context (recommended for agents)',
    ...pages.filter(p => p.mdFile).map(p => `- [${p.title} content](/${p.mdFile}): ${p.features || p.description}`)
  ].join('\n')

  return `# agentconfig.org

> A reference site for configuring AI coding assistants like GitHub Copilot and Claude Code.
> Covers 10 AI primitives, provider comparison, config file locations, and tutorials for
> skills, agent definitions, and MCP tool integrations.

This file provides a table of contents. For complete content, see /llms-full.txt.

## Pages

${pagesList}

## Docs

${docsList}

## Optional

- [agentskills.io specification](https://agentskills.io/specification): The skills format specification
- [AGENTS.md specification](https://agents.md): Open format for guiding coding agents
- [MCP specification](https://modelcontextprotocol.io/specification/latest): Model Context Protocol specification
- [Claude Code Memory docs](https://docs.anthropic.com/en/docs/claude-code/memory): Official CLAUDE.md documentation
- [Copilot customization docs](https://docs.github.com/en/copilot/customizing-copilot): GitHub Copilot instructions documentation
`
}

function generateSkillsMd(data: Awaited<ReturnType<typeof loadData>>): string {
  const { tutorialSections, skillExamples } = data
  
  let content = `# Skills Tutorial

Tutorial for creating agent skills following the agentskills.io specification.
Covers progressive disclosure, composability, and includes 5 example skills
from minimal to sophisticated.

## Tutorial Sections

`

  for (const section of tutorialSections) {
    content += `### ${section.title}

${section.description}

${section.content}

---

`
  }

  content += `## Example Skills

Five example skills demonstrating different complexity levels and patterns:

`

  for (const example of skillExamples) {
    content += `### ${example.displayName}

**Complexity:** ${example.complexity}
**Demonstrates:** ${example.demonstrates}

${example.description}

`
    
    for (const file of example.files) {
      content += `**${file.path}:**
\`\`\`${file.language || 'markdown'}
${file.content}
\`\`\`

`
    }

    content += `**Key Takeaways:**
${example.keyTakeaways.map(t => `- ${t}`).join('\n')}

---

`
  }

  return content
}

function generateAgentsMd(data: Awaited<ReturnType<typeof loadData>>): string {
  const { agentsTocItems: tocItems, agentsCodeSamples: codeSamples, agentsFurtherReadingLinks: furtherReadingLinks } = data
  
  let content = `# Agent Definitions Tutorial

Tutorial for creating agent definition files (AGENTS.md, CLAUDE.md, copilot-instructions.md).
Covers provider-specific formats, path-scoped rules, agent personas, file hierarchy,
and monorepo strategies.

## Tutorial Sections

${tocItems.map(item => `- ${item.label}${item.level ? ` (${item.level})` : ''}`).join('\n')}

## Section Details

### 1. What Are Agent Definitions?

Agent definitions are markdown files that teach AI coding assistants about your project.
They provide context about how to build, what conventions to follow, and where things live.

**Why Markdown?**
- Human readable: Team members can review and update easily
- Version controlled: Instructions evolve with your codebase
- Tool agnostic: Many AI tools read the same formats
- No runtime cost: Instructions load at session start

### 2. Your First Agent Definition

Minimal example that works with any AI coding assistant:

\`\`\`markdown
${codeSamples.minimalAgent}
\`\`\`

### 3. The Six Sections That Matter

Analysis of 2,500+ repositories shows effective agent definitions cover:

1. **Commands**: Build, test, lint with full flags
2. **Testing**: Framework, locations, how to run
3. **Project Structure**: Key directories mapped
4. **Code Style**: Actual code examples, not descriptions
5. **Git Workflow**: Branch naming, commit format, PR process
6. **Boundaries**: What the AI should NOT do

\`\`\`markdown
${codeSamples.sixSections}
\`\`\`

### 4. Provider-Specific Formats

**AGENTS.md** (Open standard, 60k+ projects):
\`\`\`markdown
${codeSamples.agentsMdFormat}
\`\`\`

**CLAUDE.md** (Claude Code):
\`\`\`markdown
${codeSamples.claudeMdFormat}
\`\`\`

**copilot-instructions.md** (GitHub Copilot):
\`\`\`markdown
${codeSamples.copilotInstructions}
\`\`\`

| Feature | AGENTS.md | CLAUDE.md | copilot-instructions |
|---------|-----------|-----------|---------------------|
| Location | Project root | Root or .claude/ | .github/ |
| Path rules | ✗ | ✓ .claude/rules/ | ✓ .instructions.md |
| File imports | ✗ | ✓ @file syntax | ✗ |
| Agent personas | ✗ | ✗ | ✓ .agent.md |
| Cross-tool support | Wide | Claude only | Copilot only |

### 5. Path-Scoped Rules

Claude (.claude/rules/api.md):
\`\`\`markdown
${codeSamples.claudeRules}
\`\`\`

Copilot (.github/instructions/api.instructions.md):
\`\`\`markdown
${codeSamples.copilotPathRules}
\`\`\`

### 6. Agent Personas (Copilot)

\`\`\`markdown
${codeSamples.agentPersona}
\`\`\`

### 7. File Hierarchy & Precedence

**Claude Code:**
\`\`\`
${codeSamples.claudeHierarchy}
\`\`\`

**GitHub Copilot:**
\`\`\`
${codeSamples.copilotHierarchy}
\`\`\`

### 8. Monorepo Strategies

\`\`\`
${codeSamples.monorepoStructure}
\`\`\`

Root AGENTS.md:
\`\`\`markdown
${codeSamples.monorepoRoot}
\`\`\`

Package-specific:
\`\`\`markdown
${codeSamples.monorepoPackage}
\`\`\`

## Further Reading

${furtherReadingLinks.map(link => `- [${link.title}](${link.url}): ${link.description}`).join('\n')}
`

  return content
}

function generateMcpMd(data: Awaited<ReturnType<typeof loadData>>): string {
  const { mcpTocItems, mcpCodeSamples, mcpFurtherReadingLinks } = data
  
  let content = `# MCP Tool Integrations Tutorial

Tutorial for connecting AI coding assistants to external tools using the Model Context Protocol (MCP).
Covers core primitives, server installation, configuration scopes, and provider comparison.

## Tutorial Sections

${mcpTocItems.map((item: any) => `- ${item.label}${item.level ? ` (${item.level})` : ''}`).join('\n')}

## Section Details

### 1. What is MCP?

The Model Context Protocol (MCP) is an open standard that connects AI applications
to external tools, databases, and APIs. Think of it like a USB-C port for AI—one
standardized interface that works across different tools.

\`\`\`
${mcpCodeSamples.mcpConcept}
\`\`\`

MCP follows a client-server architecture:

\`\`\`
${mcpCodeSamples.mcpArchitecture}
\`\`\`

### 2. Why MCP Matters

With MCP servers connected, AI assistants can:
- Query databases naturally
- Manage GitHub issues and PRs
- Analyze monitoring data from Sentry
- Access files outside the current workspace

### 3. Core Primitives

MCP servers expose three types of capabilities:

**Tools** - Executable functions the AI can invoke:
\`\`\`json
${mcpCodeSamples.toolPrimitive}
\`\`\`

**Resources** - Contextual data the AI can read:
\`\`\`json
${mcpCodeSamples.resourcePrimitive}
\`\`\`

**Prompts** - Reusable templates for interactions:
\`\`\`json
${mcpCodeSamples.promptPrimitive}
\`\`\`

### 4. Installing MCP Servers

**Claude Code (HTTP):**
\`\`\`bash
${mcpCodeSamples.claudeHttpServer}
\`\`\`

**Claude Code (stdio):**
\`\`\`bash
${mcpCodeSamples.claudeStdioServer}
\`\`\`

**VS Code + Copilot:**
\`\`\`json
${mcpCodeSamples.vscodeMcpJson}
\`\`\`

### 5. Configuration Scopes

Both providers support multiple configuration scopes:

| Scope | Claude Code | VS Code |
|-------|-------------|---------|
| Local/Workspace | ~/.claude.json | .vscode/mcp.json |
| Project | .mcp.json | .vscode/mcp.json |
| User | ~/.claude.json | User profile |
| Enterprise | managed-mcp.json | Settings + MDM |

### 6. Provider Comparison

| Feature | Claude Code | VS Code/Copilot |
|---------|-------------|-----------------|
| Transports | stdio, http, sse | stdio, http, sse |
| Tools | ✓ | ✓ |
| Resources | ✓ | ✓ |
| Prompts | ✓ (/mcp) | ✓ (/mcp.*) |
| Configuration | CLI + JSON | JSON + UI |
| Server Discovery | Manual | Gallery + Auto |
| Tool Search | ✓ (auto 10%+) | Via tool picker |
| Enterprise Control | managed-mcp.json | Settings + MDM |

### 7. Security Considerations

\`\`\`
${mcpCodeSamples.securityTrust}
\`\`\`

Enterprise management with allowlists:
\`\`\`json
${mcpCodeSamples.allowDenyLists}
\`\`\`

### 8. Practical Examples

**GitHub Integration:**
\`\`\`bash
${mcpCodeSamples.exampleGitHub}
\`\`\`

**Database Queries:**
\`\`\`bash
${mcpCodeSamples.exampleDatabase}
\`\`\`

**Error Monitoring (Sentry):**
\`\`\`bash
${mcpCodeSamples.exampleSentry}
\`\`\`

## Further Reading

${mcpFurtherReadingLinks.map((link: any) => `- [${link.title}](${link.url}): ${link.description}`).join('\n')}
`

  return content
}

function generateLlmsFullTxt(data: Awaited<ReturnType<typeof loadData>>): string {
  const { primitives, comparisonData, pages } = data
  
  // Build list of topics from registry
  const topicsList = pages.map(p => `- ${p.title}`).join('\n')
  
  let content = `# agentconfig.org - Complete Site Content

> This file contains the complete content of agentconfig.org for AI agents.
> It includes all AI primitives, provider comparisons, config file locations,
> and tutorials for skills, agent definitions, and MCP tool integrations.

## Site Overview

agentconfig.org is a reference site for configuring AI coding assistants like GitHub Copilot
and Claude Code. The site helps developers understand and implement AI configuration primitives
to get consistent, high-quality assistance from AI tools.

**Key Topics:**
- 10 AI primitives for configuring agent behavior
- Provider comparison (GitHub Copilot vs Claude Code)
- Config file locations and hierarchy
${topicsList}

---

# Part 1: AI Primitives

The site documents 10 AI primitives organized into 3 categories:
- **Capability (Execution)**: What the AI can do
- **Customization (Instructions)**: How to shape AI behavior
- **Control (Safety)**: How to constrain AI actions

`

  // Group primitives by category
  const byCategory = {
    execution: primitives.filter(p => p.category === 'execution'),
    instructions: primitives.filter(p => p.category === 'instructions'),
    safety: primitives.filter(p => p.category === 'safety'),
  }

  content += `## Capability Primitives (Execution)

These primitives define what the AI can do.

`

  for (const p of byCategory.execution) {
    content += formatPrimitive(p)
  }

  content += `## Customization Primitives (Instructions)

These primitives shape how the AI behaves.

`

  for (const p of byCategory.instructions) {
    content += formatPrimitive(p)
  }

  content += `## Control Primitives (Safety)

These primitives constrain what the AI is allowed to do.

`

  for (const p of byCategory.safety) {
    content += formatPrimitive(p)
  }

  content += `---

# Part 2: Provider Comparison

Support matrix comparing GitHub Copilot and Claude Code:

| Primitive | Copilot | Claude |
|-----------|---------|--------|
`

  for (const row of comparisonData) {
    const copilotIcon = row.copilot.level === 'full' ? '✓' : row.copilot.level === 'partial' ? '◐' : '—'
    const claudeIcon = row.claude.level === 'full' ? '✓' : row.claude.level === 'partial' ? '◐' : '—'
    content += `| ${row.primitiveName} | ${copilotIcon} ${row.copilot.implementation} | ${claudeIcon} ${row.claude.implementation} |\n`
  }

  content += `
### Config File Locations

**GitHub Copilot:**
- Persistent Instructions: \`.github/copilot-instructions.md\`
- Path-Scoped Rules: \`.github/instructions/*.instructions.md\`
- Slash Commands: \`.github/prompts/*.prompt.md\`
- Custom Agents: \`.github/agents/*.agent.md\`
- Skills: \`.github/skills/*/SKILL.md\`

**Claude Code:**
- Persistent Instructions: \`CLAUDE.md\` (root) or \`.claude/CLAUDE.md\`
- Global Instructions: \`~/.claude/CLAUDE.md\`
- Path-Scoped Rules: \`.claude/rules/*.md\`
- Slash Commands: \`.claude/commands/*.md\`
- Custom Agents: \`.claude/agents/*.md\`
- Skills: \`.claude/skills/*/SKILL.md\`
- Lifecycle Hooks: \`.claude/hooks/hooks.json\`
- MCP Settings: \`.claude/settings.json\`

---

# Part 3: Skills Tutorial

`

  content += generateSkillsMd(data).replace(/^# Skills Tutorial\n\n[^\n]+\n[^\n]+\n[^\n]+\n\n/, '')

  content += `
---

# Part 4: Agent Definitions Tutorial

`

  content += generateAgentsMd(data).replace(/^# Agent Definitions Tutorial\n\n[^\n]+\n[^\n]+\n[^\n]+\n\n/, '')

  content += `
---

# Part 5: MCP Tool Integrations Tutorial

`

  content += generateMcpMd(data).replace(/^# MCP Tool Integrations Tutorial\n\n[^\n]+\n[^\n]+\n[^\n]+\n\n/, '')

  return content
}

function formatPrimitive(p: any): string {
  return `### ${p.name}

${p.description}

**What it is:** ${p.whatItIs}

**Use when:**
${p.useWhen.map((u: string) => `- ${u}`).join('\n')}

**Prevents:** ${p.prevents}

**Combine with:** ${p.combineWith.join(', ')}

**Provider Implementations:**

| Provider | Implementation | Location | Support |
|----------|---------------|----------|---------|
${p.implementations.map((impl: any) => {
  const providerName =
    impl.provider === 'copilot' ? 'GitHub Copilot' :
    impl.provider === 'claude' ? 'Claude Code' :
    impl.provider === 'cursor' ? 'Cursor' :
    impl.provider;
  return `| ${providerName} | ${impl.implementation} | ${impl.location} | ${impl.support} |`
}).join('\n')}

---

`
}

async function main() {
  console.log('Loading data files...')
  const data = await loadData()
  
  console.log('Generating llms.txt...')
  const llmsTxt = generateLlmsTxt(data.pages)
  writeFileSync(join(publicDir, 'llms.txt'), llmsTxt)
  
  console.log('Generating skills.md...')
  const skillsMd = generateSkillsMd(data)
  writeFileSync(join(publicDir, 'skills.md'), skillsMd)
  
  console.log('Generating agents.md...')
  const agentsMd = generateAgentsMd(data)
  writeFileSync(join(publicDir, 'agents.md'), agentsMd)
  
  console.log('Generating mcp.md...')
  const mcpMd = generateMcpMd(data)
  writeFileSync(join(publicDir, 'mcp.md'), mcpMd)
  
  console.log('Generating llms-full.txt...')
  const llmsFullTxt = generateLlmsFullTxt(data)
  writeFileSync(join(publicDir, 'llms-full.txt'), llmsFullTxt)
  
  console.log('Done! Generated:')
  console.log('  - site/public/llms.txt')
  console.log('  - site/public/llms-full.txt')
  for (const page of data.pages) {
    if (page.mdFile) {
      console.log(`  - site/public/${page.mdFile}`)
    }
  }
}

main().catch(console.error)

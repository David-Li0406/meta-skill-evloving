---
name: write-research
description: Create a blog post from a research document. Use when the user says "/write-research..." to convert research material into a polished article at the specified post type and category.
---

# Write Research Skill

Converts research documents from `content/in-research/` into polished blog posts.

## Invocation

- `/write-research <posttype> <category> <path-to-research>`
- `/write-research posts web content/in-research/2024-01-15-websockets/`

### Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `posttype` | Target collection | `posts`, `in-research` |
| `category` | Category within collection | `web`, `tools`, `design-problems` |
| `path` | Path to research folder | `content/in-research/2024-01-15-websockets/` |

If called without arguments, ask user for:
1. Path to research document
2. Target post type and category

## Workflow

```mermaid
flowchart TD
    A[User Request] --> B[Load Research]
    B --> C[Validate Research]
    C --> D[Plan Article]
    D --> E[Write Content]
    E --> F[Quality Check]
    F --> G[Save Article]
    G --> H[Update Research Status]
```

## Phase 1: Load Research

Read all files from the research folder:

```plain
content/in-research/[slug]/
├── index.md          # Main research
├── _sources.md       # Annotated sources
├── _outline.md       # Proposed outline
└── _notes.md         # Raw notes
```

### Extract Key Information

- Research summary and key findings
- Annotated sources with quality ratings
- Proposed article outline
- Identified gaps and open questions

## Phase 2: Validate Research

Check research is ready to write:

### Research Readiness Checklist

- [ ] Key findings documented
- [ ] Major themes identified
- [ ] Authoritative sources found
- [ ] Outline is specific and actionable
- [ ] Critical gaps addressed or noted

### If Research is Incomplete

Ask user:
1. Proceed with available research?
2. Return to `/research-post` to fill gaps?
3. Specify which gaps to ignore?

## Phase 3: Plan Article

### Map Research to Article

Based on the research outline, create article plan:

```markdown
## Article Plan

**Title**: [From outline or refined]
**Target**: posts/[category]/YYYY-MM-DD-[slug]/

### Sections

1. **Abstract**
   - Sources: [list]
   - Key points to cover: [list]

2. **TLDR**
   - Themes from research: [map]

3. **[Section Name]**
   - Research findings to use: [list]
   - Sources for citations: [list]
   - Diagrams needed: [list]

### Code Examples
- [Example 1]: [Source reference]

### Diagrams
- [Diagram 1]: [Description]
```

### Identify Additional Research Needed

If outline reveals gaps:
- Do quick targeted research
- Note in article if something is unverified
- Flag for future update

## Phase 4: Write Content

Use the `/write-post` skill's content standards, but leverage existing research.

### Writing From Research

#### Abstract
- Use research summary as foundation
- Refine for article context
- Add overview diagram

#### TLDR
- Map research themes to TLDR subsections
- Ensure comprehensive coverage
- Add trade-offs identified in research

#### Main Content

For each section:
1. Review relevant research findings
2. Pull key insights and examples
3. Add inline citations from `_sources.md`
4. Create diagrams from research descriptions
5. Write code examples with collapse

### Citation Integration

Transform source annotations into inline references:

```markdown
// From _sources.md
## Node.js Event Loop Documentation
**URL**: https://nodejs.org/...
**Type**: Official Docs
**Key Points**: Event loop has 6 phases...

// In article
The event loop processes callbacks in six distinct phases ([Node.js Event Loop Documentation](https://nodejs.org/...)).
```

### Code Examples

**Always collapse any lines not essential to the key concept.** Use multiple ranges:

**Collapse Syntax:** `collapse={1-5, 12-18, 25-30}` — any line ranges, including middle sections.

````markdown
```typescript title="data-fetcher.ts" collapse={1-6, 14-21, 29-35}
// Lines 1-6: Imports (collapsed)
import { fetch } from 'node-fetch'
import { Cache } from './cache'
import type { FetchOptions, FetchResult } from './types'

const cache = new Cache()
const BASE_URL = 'https://api.example.com'

// Lines 7-13: VISIBLE - Key fetching pattern
export async function fetchWithCache<T>(path: string, ttl: number): Promise<T> {
  const cached = cache.get<T>(path)
  if (cached) return cached
  const data = await fetch(`${BASE_URL}${path}`).then(r => r.json())
  cache.set(path, data, ttl)
  return data
}

// Lines 14-21: Retry logic (collapsed)
async function fetchWithRetry(url: string, retries = 3): Promise<Response> {
  for (let i = 0; i < retries; i++) {
    const res = await fetch(url)
    if (res.ok) return res
    await sleep(Math.pow(2, i) * 100)
  }
  throw new Error('Max retries exceeded')
}

// Lines 22-28: VISIBLE - Key batch operation
export async function fetchBatch<T>(paths: string[]): Promise<T[]> {
  return Promise.all(paths.map(p => fetchWithCache<T>(p, 300)))
}

// Lines 29-35: Utilities (collapsed)
function sleep(ms: number): Promise<void> { return new Promise(r => setTimeout(r, ms)) }
function buildUrl(path: string, params: Record<string, string>): string { /* ... */ }
```
````

**Collapse rules:**
- Imports and setup: Always collapsed
- **Middle sections**: Helpers between key functions collapsed
- Only the key patterns readers need should be visible

## Phase 5: Quality Check

### Technical Accuracy (HIGHEST PRIORITY)
- [ ] Every claim verified against research sources
- [ ] Inline references for all significant claims
- [ ] Code examples syntactically correct and idiomatic
- [ ] Code would pass PR review from senior engineer
- [ ] Performance claims backed by evidence
- [ ] Diagrams accurately represent described behavior
- [ ] No speculation presented as fact
- [ ] Terminology correct and current

### Authoritative Tone
- [ ] Assertive statements where evidence supports
- [ ] No excessive hedging or unnecessary qualifiers
- [ ] Confident presentation of verified facts
- [ ] Explicit about unknowns and limitations
- [ ] Reads like staff engineer explaining to peers

### Research Integration
- [ ] All key findings from research represented
- [ ] Sources properly cited with inline references
- [ ] Gaps explicitly acknowledged if unresolved
- [ ] No research copied verbatim (synthesized into article voice)
- [ ] Research quality validated before use

### Completeness
- [ ] Abstract sets clear context (2-4 sentences)
- [ ] Overview diagram visualizes core concept
- [ ] TLDR is comprehensive and standalone (usable as reference)
- [ ] Design reasoning explained (why, not just what)
- [ ] All edge cases and subtleties addressed
- [ ] Failure modes discussed where relevant

### Trade-offs (MANDATORY)
- [ ] Explicit pros/cons for every approach
- [ ] When to use AND when NOT to use
- [ ] Real-world examples demonstrating trade-offs
- [ ] Nothing presented as "the best solution"
- [ ] Alternative approaches mentioned with reasoning

### Conciseness (ZERO FILLER)
- [ ] No padding or filler sentences
- [ ] No meta-commentary ("In this article...")
- [ ] No tutorial-style hand-holding
- [ ] No obvious statements
- [ ] Every paragraph adds new information
- [ ] Reading time < 30 minutes

### Staff/Principal Engineer Standard
- [ ] Could be cited as authoritative reference
- [ ] Handles nuance senior engineers care about
- [ ] Addresses operational/production concerns
- [ ] Complete enough for informed decision-making

### Formatting
- [ ] No manual ToC
- [ ] Mermaid diagrams render correctly
- [ ] Code blocks use collapse for boilerplate
- [ ] Code blocks have title attribute
- [ ] References section complete

## Phase 6: Save Article

### Create Article

Location: `content/[posttype]/[category]/YYYY-MM-DD-[slug]/`

```yaml
---
lastReviewedOn: YYYY-MM-DD
tags:
  - [tag-from-research]
  - [tag-from-research]
---
```

### Build Verification

```bash
npm run build
npm run validate:build
```

## Phase 7: Update Research Status

After article is saved, update research document:

```yaml
---
topic: [Topic]
status: written  # Changed from research/ready-to-write
researchedOn: YYYY-MM-DD
writtenOn: YYYY-MM-DD
articlePath: content/posts/[category]/YYYY-MM-DD-[slug]/
---
```

## Handling Multiple Articles

If research suggests multiple articles:

1. Ask user which to write first
2. Create article for selected topic
3. Update research with cross-references
4. Note remaining articles in research status

## Anti-Patterns (STRICT)

### Content Anti-Patterns
- **Copy-pasting research**: Synthesize, don't copy verbatim
- **Ignoring gaps**: Unresolved questions must be explicitly noted
- **Missing citations**: Every significant claim needs inline reference
- **Over-verbose**: Research may be detailed; article must be concise
- **Tutorial-style**: "First, let's understand...", "Before we begin..."
- **Obvious statements**: "Security is important", "Performance matters"
- **Meta-commentary**: "In this article, we will..."
- **Silver bullet thinking**: "This is the best approach"
- **Incomplete trade-offs**: Only benefits, no downsides
- **Migration timelines/development plans**: Do NOT include phased rollout plans, week-by-week timelines, or development schedules unless explicitly requested by user

### Tone Anti-Patterns
- **Excessive hedging**: "might possibly", "could perhaps"
- **False certainty**: Speculation presented as fact
- **Preachy**: "You should...", "You must..."
- **Dismissive**: "Obviously...", "Simply..."

### Technical Anti-Patterns
- **Incorrect code**: Syntax errors, logic bugs, deprecated APIs
- **Unidiomatic code**: Not following language conventions
- **Missing context**: Code without title or explanation
- **Outdated information**: Old versions, deprecated patterns

### Process Anti-Patterns
- **Skipping quality check**: Research quality doesn't guarantee article quality
- **Blind trust**: Not verifying research claims before using
- **Incomplete transfer**: Missing key insights from research

## Reference Documents

**IMPORTANT**: Before writing, read these documents from the project root:

| Document | Path (from project root) | Purpose |
|----------|--------------------------|---------|
| Content Guidelines | `llm_docs/content-guidelines.md` | Writing standards, conciseness rules, quality checklist |
| Markdown Features | `llm_docs/markdown-features.md` | Expressive Code syntax, Mermaid diagrams, KaTeX |
| Write Post Skill | `.claude/skills/write-post/SKILL.md` | Content creation workflow and standards |
| Project Instructions | `CLAUDE.md` | Project structure, commands, styling conventions |

**Usage**: Use the Read tool with absolute paths (e.g., `/path/to/project/llm_docs/content-guidelines.md`) to read these files before starting work.

## Tools Available

- `Read` - Load research documents
- `Write` - Create article
- `Glob` - Find research files
- `Edit` - Update research status
- `WebSearch` - Fill minor gaps
- `WebFetch` - Verify sources still valid
- `Bash` - Build and validation

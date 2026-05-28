---
name: research-gather
description: "Systematically gather source material for blog articles. GitHub history, session transcripts, code examples, screenshots. Use at RESEARCH stage of blog pipeline."
---

# Research Gather Skill

**Purpose:** Systematically assemble all source material needed for an article.

---

## When to Use

At the RESEARCH stage of the blog pipeline, after IDEA is defined and before WALK.

---

## Source Types

| Source | What to Gather | How |
|--------|----------------|-----|
| **GitHub history** | Commits, PRs, issues relevant to story | `git log`, GitHub API |
| **Session transcripts** | Past Claude conversations on topic | Search transcripts collection |
| **Code examples** | Actual code that demonstrates points | Extract from repos |
| **Screenshots** | UI states, terminal output, diagrams | Capture or find existing |
| **Dates & timeline** | When things happened | Git history, file dates |
| **External references** | Docs, articles, tools mentioned | Web search, bookmarks |

---

## Process

### 0. Load Author Context

**Before any research**, read from eterne (private vault):

```
~/src/eterne/vault/03-resources/blog-context/
├── author.md           # Quick reference (always load)
├── timeline/overview.md # For chronological articles
├── people/family.md    # If relationships mentioned
└── themes/
    ├── spiritual.md    # If practice/philosophy relevant
    └── career.md       # If professional history relevant
```

**Why eterne?** Biographical context is private (names, health history, location).

This provides:
- Verified biographical facts (prevents hallucination)
- Current project metrics and scale
- Key claims with evidence status
- Family and relationship context
- Spiritual/philosophical background
- Career arc (including illness era context)

### 1. Define Research Questions

Based on the one-sentence teaching from IDEA stage:
- What claims will this article make?
- What evidence supports each claim?
- What concrete examples illustrate each point?

### 2. Gather by Source Type

**GitHub History:**
```bash
# Find commits related to topic
git log --oneline --grep="[keyword]"
git log --oneline --since="2024-01-01" --until="2024-06-01" -- path/to/relevant/

# Find PRs
gh pr list --state all --search "[keyword]"
```

**Session Transcripts:**
- Search `packages/blog/src/content/transcripts/`
- Search conversation history for relevant topics
- Note session dates and key exchanges

**Code Examples:**
- Extract minimal, self-contained examples
- Verify they still run
- Note file paths and commit hashes for attribution

**Timeline:**
- Build chronological sequence of events
- Note key dates, durations, milestones

### 3. Organize Material

Create research file at `pipeline/active/NNN-slug/02-research.md`:

```markdown
# Research: [Article Title]

## Claims & Evidence

### Claim 1: [Statement]
- Evidence: [source, quote, data]
- Example: [code/screenshot/transcript excerpt]

### Claim 2: [Statement]
...

## Timeline

| Date | Event | Source |
|------|-------|--------|
| YYYY-MM-DD | [What happened] | [Git commit / transcript / etc.] |

## Code Examples

### Example 1: [Description]
```[language]
[code]
```
Source: [file path @ commit]

## Open Questions

- [Things to explore during WALK stage]
- [Gaps in evidence]

## Raw Material

[Links, excerpts, screenshots to process]
```

---

## Quality Gate

**Gate question:** Do you have concrete examples for every claim?

**Checklist:**
- [ ] Author context loaded and referenced
- [ ] Every claim has supporting evidence
- [ ] Timeline is documented with sources
- [ ] Code examples are extracted and verified
- [ ] Screenshots captured if needed
- [ ] Gaps identified for WALK stage exploration

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Vague notes | Can't verify later | Cite specific sources |
| Too much material | Overwhelms outline | Focus on claims, not completeness |
| Unverified examples | May not work | Run code, check links |
| Missing dates | Timeline unclear | Always note when things happened |

---

*Research serves the story. Precision now prevents problems later.*

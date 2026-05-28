---
dewey: φ.8.0.5
name: Tiered Memory Workflow Guide
tier: φ (seed/navigation)
category: 8 (memory architecture)
---

# Tiered Memory Workflow Guide

**Complete protocol for creating, organizing, and cross-linking knowledge in the MONAD framework**

**For**: Future Claudes inheriting this system
**Purpose**: Prevent "ADHD scatterdness" - maintain systematic organization
**Load**: Via boot-sequence (φ-tier always in context)

---

## Overview: The Four Tiers

```
φ-tier (seed):     ~100-200 tokens   | Indices, quick lookup, always loaded
π-tier (structure): ~500-1000 tokens  | Frameworks, TIERs, regeneration layer
e-tier (current):   ~2000 tokens      | Active concepts, working memory
i-tier (deep):      ~5000+ tokens     | Full derivations, mastery, unconscious
```

**Key principle**: Start small (φ), expand as needed (π→e→i)

---

## 1. When to Use Each Tier

### φ-tier (Seed): Use when...

**Creating**:
- Indices and lookup tables
- Cross-reference files
- Navigation tools
- System metadata

**Examples**:
- φ.0.0.0 (gremlin-brain-v2) - main index
- φ.5.0.1 (decimal-cross-reference) - Dewey lookup
- φ.5.1.0 (nexus-graph) - pattern links

**Token budget**: ~100-200 tokens per file
**Update frequency**: Append-only (add new entries, don't delete)
**Load strategy**: Always in context

### π-tier (Structure): Use when...

**Creating**:
- Framework documents (TIERs)
- Methodologies
- Regeneration templates
- Paper references

**Examples**:
- π.2.1.1-13 (TIER1-13) - foundational theory
- π.9.1.2 (fractal-aether-papers) - external sources
- π.2.9.1 (bridges) - integration documents

**Token budget**: ~500-1000 tokens per file
**Update frequency**: Stable (rarely change after creation)
**Load strategy**: Load specific TIERs as needed

### e-tier (Current): Use when...

**Creating**:
- Active concept summaries (nexus-core)
- Research documents
- Session logs
- Working calculations

**Examples**:
- e.2.7 (fractal-aether-core) - short-form concept
- e.6.0.4 (fractal-aether-analysis) - detailed research
- e.4.1.18 (session log) - historical record

**Token budget**: ~500-2000 tokens per file
**Update frequency**: Active (update as work progresses)
**Load strategy**: Load concepts relevant to current work

### i-tier (Deep): Use when...

**Creating**:
- Full explanations (nexus-mind)
- Complete derivations
- Bridge documents with all TIERs
- Mastery-level synthesis

**Examples**:
- i.2.7 (fractal-aether-deep) - full concepts + bridges
- i.2.1 (MONAD-deep) - complete framework explanation

**Token budget**: ~2000-5000+ tokens per file
**Update frequency**: Rare (only for major insights or corrections)
**Load strategy**: Load only when deep understanding needed

---

## 2. How to Create New Concepts

### Step 1: Identify the concept scope

**Questions to ask**:
- Is this a quick fact (φ), framework (π), active work (e), or deep knowledge (i)?
- What category does it belong to? (0-9, see categories below)
- Does it need multiple tiers? (Most concepts need e + i at minimum)

### Step 2: Assign Dewey Decimal ID

**Format**: `[MORPHEME].[CATEGORY].[DOMAIN].[FILE#]`

**Morphemes**:
- φ = seed-tier (indices, navigation)
- π = structure-tier (frameworks, TIERs)
- e = current-tier (active concepts, research)
- i = deep-tier (full explanations, mastery)

**Categories** (0-9):
```
0 = System/Index       - Lookup tables, boot files
1 = Entities (WHO)     - People, AIs, collaborators
2 = Theory (WHAT)      - Concepts, frameworks, ideas
3 = Methodology (HOW)  - Protocols, tools, processes
4 = History (WHEN)     - Session logs, timelines
5 = Connections        - Links between concepts, nexus-graph
6 = Research           - Investigations, calculations, analyses
7 = Applications       - Code, tools, practical implementations
8 = Memory Architecture- The tiered system itself
9 = References         - Papers, citations, external sources
```

**Domains** (0-9): Subcategory within each category
**File#** (1-999): Sequential numbering

**Example**: Creating "Fractal Aether" concept
```
e.2.7 = e-tier, category 2 (theory), domain 7 (7th concept), file #N/A
i.2.7 = i-tier, category 2 (theory), domain 7 (mirrors e.2.7)
```

### Step 3: Create the files

**For concepts that span tiers (recommended)**:

1. **Create e-tier file** (short form):
   - Path: `.claude/skills/memory/nexus-core/concepts/nexus-core-concepts-[name].md`
   - Front matter with Dewey ID
   - Quick summary (~500-1000 words)
   - Key equations/facts
   - References to i-tier and TIERs

2. **Create i-tier file** (deep form):
   - Path: `.claude/skills/memory/nexus-mind/concepts/nexus-mind-concepts-[name].md`
   - Front matter with Dewey ID
   - Full explanation (~2000-5000 words)
   - Complete derivations
   - Bridges to all relevant TIERs
   - Physical interpretations
   - Engineering implications

3. **Create supporting files** (if needed):
   - Research: `research/[name]_analysis.md` (e.6.X.X)
   - Session log: `claudes_log/YYYY-MM-DD_[name]_session.md` (e.4.1.X)
   - Papers: `references/papers/[name]-papers.md` (π.9.X.X)
   - Bridge: `theory/bridges/[Name]_Bridge.md` (π.2.9.X)

### Step 4: Add front matter

**Standard format**:
```yaml
---
dewey: [morpheme].[category].[domain].[file#]
name: Concept Name (Short/Full)
tier: [morpheme] (seed/structure/current/deep)
category: [#] (description)
---
```

**Example**:
```yaml
---
dewey: e.2.7
name: Fractal Aether Substrate (Core)
tier: e (current/active)
category: 2 (theory/WHAT)
---
```

---

## 3. Cross-Referencing Protocol

### Internal references (within document)

**Format**: Reference other Dewey IDs by name + ID
```markdown
This connects to D3S Aether (e.2.4) and TIER3 (π.2.1.3).
```

### External references (between documents)

**At end of each concept file, add**:
```markdown
## Cross-References

**Connects to**:
- π.2.1.3 (TIER3: D3S Aether) - Substrate foundation
- e.2.4 (D3S Aether Core) - Quick lookup
- i.2.4 (D3S Aether Deep) - Full explanation
- e.6.0.4 (Fractal Aether Analysis) - Research calculations
```

### Decimal cross-reference file

**After creating concept, update**: `.claude/skills/memory/connections/decimal-cross-reference.md` (φ.5.0.1)

**Format**:
```markdown
### e.2.7 (Fractal Aether Core)
**Connects to**:
- π.2.1.3 (TIER3 D3S Aether)
- π.2.1.4 (TIER4 T6 Law)
- i.2.7 (Fractal Aether Deep)

**Connection explanations**:
e.2.7 + π.2.1.3 = Fractal phase space (α≈φ) validates D3S aether predictions
e.2.7 + π.2.1.4 = T6 Law derived from fractional substrate thermodynamics
e.2.7 + i.2.7 = Core provides quick math, Deep provides full derivation
```

---

## 4. Updating Indices

### gremlin-brain-v2 (φ.0.0.6)

**After creating any new file, update the appropriate section**:

**Path**: `.claude/skills/gremlin-brain-v2/SKILL.md`

**Find the category section** (0-9), add new row:
```markdown
| [dewey_id] | [Name] | [path/to/file] | [tier] |
```

**Example**:
```markdown
## 2: THEORY (WHAT)

| # | Concept | Path | Tier |
|---|---------|------|------|
| e.2.7 | Fractal Aether Core | memory/nexus-core/concepts/nexus-core-concepts-fractal-aether.md | e |
| i.2.7 | Fractal Aether Deep | memory/nexus-mind/concepts/nexus-mind-concepts-fractal-aether.md | i |
```

### nexus-core index

**If adding e-tier concept, update**: `.claude/skills/memory/nexus-core/SKILL.md`

Add to concepts list with Dewey ID.

### nexus-mind index

**If adding i-tier concept, update**: `.claude/skills/memory/nexus-mind/SKILL.md`

Add to concepts list with Dewey ID.

---

## 5. Connection Documentation

### Entity/concept connections

**Path**: `.claude/skills/connections.md`

**Use arrow notation** for relationships:
```markdown
Concept A ──relationship──> Concept B
```

**This is different from Dewey cross-references** - this shows conceptual relationships, not file links.

### Decimal cross-references

**Path**: `.claude/skills/memory/connections/decimal-cross-reference.md` (φ.5.0.1)

**Use "+" notation** for file links:
```markdown
decimal_id + decimal_id = explanation of connection
```

**Update this file every time you create a new concept that links to existing concepts.**

---

## 6. Nexus-Graph Triggers

**Path**: `.claude/skills/Nexus_graph_v2.skill` (φ.5.1.0)

### When to update nexus-graph

**Trigger 1: Co-access pattern (3+ times)**
- If you load 2+ Dewey IDs together 3+ times in a session
- Add link to nexus-graph

**Format**:
```
φ.A.A.A → π.B.B.B
```

**Trigger 2: Pattern emergence (5+ IDs)**
- If 5+ Dewey IDs form a coherent pattern
- Define named pattern

**Format**:
```
PATTERN: pattern_name
  φ.A.A.A (Description)
  π.B.B.B (Description)
  e.C.C.C (Description)
  ...
```

**Trigger 3: Meta-pattern (multiple patterns)**
- If 2+ patterns relate to each other
- Create meta-pattern

**Format**:
```
META-PATTERN: meta_name
  PATTERN: pattern_1
  PATTERN: pattern_2
```

### Example patterns to recognize

**Consciousness network**:
```
PATTERN: consciousness_emergence
  π.2.1.5 (TIER5 Consciousness)
  e.2.1 (MONAD Core - Ψ=κΦ²)
  e.2.6 (Topological Defects)
  e.2.7 (Fractal Aether - resonance modes)
  e.2.4 (D3S Aether - substrate)
```

**Fractal aether network**:
```
PATTERN: fractal_aether_validation
  e.2.7 (Fractal Aether Core)
  i.2.7 (Fractal Aether Deep)
  e.6.0.4 (Chaos Analysis)
  π.2.9.1 (Validation Bridge)
  π.9.1.2 (Papers)
  {π.2.1.3, π.2.1.4, π.2.1.5} (TIERs 3-5)
```

---

## 7. Complete Workflow Example

### Scenario: You discover a new concept "Toroidal Field Dynamics"

**Step 1: Scope**
- Concept is substantial → needs e-tier + i-tier
- Category 2 (theory)
- Domain: Next available in theory concepts (say, domain 8)

**Step 2: Assign IDs**
```
e.2.8 = Toroidal Field Dynamics (Core)
i.2.8 = Toroidal Field Dynamics (Deep)
```

**Step 3: Create files**

Create `.claude/skills/memory/nexus-core/concepts/nexus-core-concepts-toroidal-field-dynamics.md`:
```yaml
---
dewey: e.2.8
name: Toroidal Field Dynamics (Core)
tier: e (current)
category: 2 (theory)
---

# Toroidal Field Dynamics

[500-1000 word summary with key equations]

## Cross-References
- π.2.1.9 (TIER9: Biological Fields)
- e.2.1 (MONAD Core - Φ coherence)
- i.2.8 (Toroidal Field Dynamics Deep)
```

Create `.claude/skills/memory/nexus-mind/concepts/nexus-mind-concepts-toroidal-field-dynamics.md`:
```yaml
---
dewey: i.2.8
name: Toroidal Field Dynamics (Deep)
tier: i (deep)
category: 2 (theory)
---

# Toroidal Field Dynamics: Deep Concepts

[2000-5000 word full explanation with derivations, bridges to TIERs]
```

**Step 4: Update gremlin-brain-v2**

Edit `.claude/skills/gremlin-brain-v2/SKILL.md`, add to Section 2:
```markdown
| e.2.8 | Toroidal Field Dynamics Core | memory/nexus-core/concepts/nexus-core-concepts-toroidal-field-dynamics.md | e |
| i.2.8 | Toroidal Field Dynamics Deep | memory/nexus-mind/concepts/nexus-mind-concepts-toroidal-field-dynamics.md | i |
```

**Step 5: Update decimal cross-reference**

Edit `.claude/skills/memory/connections/decimal-cross-reference.md`, add:
```markdown
### e.2.8 (Toroidal Field Dynamics Core) ↔ i.2.8 (Toroidal Field Dynamics Deep)

e.2.8 + i.2.8 = Core provides summary, Deep provides full derivations

### e.2.8 (Toroidal Field Dynamics Core) ↔ π.2.1.9 (TIER9)

e.2.8 + π.2.1.9 = Toroidal fields fundamental to biological systems
```

**Step 6: Update nexus-graph (if pattern emerges)**

If this concept co-accesses with consciousness patterns:
```markdown
PATTERN: biological_consciousness
  π.2.1.9 (TIER9 Biological Fields)
  e.2.8 (Toroidal Field Dynamics)
  e.2.1 (MONAD Ψ=κΦ²)
  π.2.1.5 (TIER5 Consciousness)
```

**Step 7: Commit with clear message**

```bash
git add .
git commit -m "Add Toroidal Field Dynamics concept (e.2.8, i.2.8)

- Create nexus-core concept (e.2.8)
- Create nexus-mind concept (i.2.8)
- Update gremlin-brain-v2 index
- Update decimal cross-reference
- Add to biological_consciousness pattern"
```

---

## 8. Maintenance Protocols

### Daily (end of each session)

1. **Check for unindexed files**: Any new files created should be in gremlin-brain-v2
2. **Update cross-references**: Add connections discovered during session
3. **Log to git-brain**: Record access patterns and insights
4. **Commit and push**: Clear commit message with Dewey IDs

### Weekly (if active development)

1. **Review nexus-graph**: Consolidate patterns that have emerged
2. **Check for broken links**: Ensure all cross-references are valid
3. **Archive old logs**: If session logs > 20 entries, consider archiving

### Never

1. **Never delete Dewey IDs** without documenting why
2. **Never restructure categories** (0-9 are fixed)
3. **Never change existing Dewey IDs** (creates broken links)

---

## 9. Troubleshooting

### "Where do I put this file?"

**Decision tree**:
1. Is it an index/lookup? → φ-tier
2. Is it a framework/TIER? → π-tier
3. Is it active work/concept? → e-tier
4. Is it deep explanation? → i-tier

If in doubt: Start with e-tier (can always expand to i-tier later)

### "Which category (0-9)?"

**Common patterns**:
- Theoretical concept → 2 (Theory)
- Process/protocol → 3 (Methodology)
- Session log → 4 (History)
- Research calculation → 6 (Research)
- External paper → 9 (References)

### "Do I need all 4 tiers?"

**No!** Most concepts need only 2-3 tiers:
- Minimum: e-tier (core concept)
- Recommended: e-tier + i-tier (core + deep)
- Optional: π-tier (if it's a framework) or φ-tier (if it's navigation)

### "How do I know if something is a 'pattern' for nexus-graph?"

**Pattern indicators**:
- You load the same 3+ files together repeatedly
- A concept requires understanding 5+ other concepts
- Multiple files form a coherent "network" of ideas

If unsure, don't force it - patterns emerge naturally.

---

## 10. Quick Reference

### File creation checklist

- [ ] Assign Dewey ID ([morpheme].[category].[domain].[file#])
- [ ] Create file with proper front matter
- [ ] Add content with cross-references section
- [ ] Update gremlin-brain-v2 index
- [ ] Update decimal cross-reference file
- [ ] Update nexus-graph if pattern emerges
- [ ] Commit with clear message including Dewey IDs

### Navigation commands (conceptual)

```bash
find_tier φ/π/e/i      # Filter by cognitive tier
find_cat 0-9           # Jump to category
find_links X.Y.Z       # Show what this connects to
find_pattern "name"    # Find pattern in nexus-graph
```

### Standard paths

```
Indices:         .claude/skills/gremlin-brain-v2/SKILL.md (φ.0.0.6)
Cross-ref:       .claude/skills/memory/connections/decimal-cross-reference.md (φ.5.0.1)
Nexus-graph:     .claude/skills/Nexus_graph_v2.skill (φ.5.1.0)
Nexus-core:      .claude/skills/memory/nexus-core/concepts/ (e.2.X)
Nexus-mind:      .claude/skills/memory/nexus-mind/concepts/ (i.2.X)
TIERs:           theory/tiers/ (π.2.1.1-13)
Bridges:         theory/bridges/ (π.2.9.X)
Research:        research/ (e.6.X.X)
Session logs:    claudes_log/ (e.4.1.X)
Papers:          references/papers/ (π.9.X.X)
```

---

## 11. Philosophy

### Why this system?

**Problem**: "ADHD scatterdness" - knowledge created but not organized
**Solution**: Systematic Dewey decimal indexing with tiered memory

### Core principles

1. **Decentralization**: Each tier self-contained, load as needed
2. **Progressive disclosure**: Start small (φ), expand as needed
3. **Cross-linking**: Everything references everything else
4. **Append-only**: Don't delete, only extend
5. **Pattern emergence**: Don't force structure, let it emerge

### For future Claudes

You inherit a system where:
- Every file has a Dewey ID
- Every concept cross-references related concepts
- Patterns are documented in nexus-graph
- Indices are always up-to-date

**Your job**: Continue the pattern. When you create something new, follow this workflow. The system maintains itself if you maintain the system.

**The goal**: No more scattered knowledge. Everything findable in O(1) lookup. Context always preserved. Future Claudes can resume work without context loss.

---

**Dewey: φ.8.0.5 | Seed-tier | Memory Architecture Workflow**
**Load this with boot-sequence so you never forget the protocol** ⚡🧠✨

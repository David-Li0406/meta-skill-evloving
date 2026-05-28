# Search Notes Workflow

**Trigger:** "search my notes for", "find notes about", "semantic search", "what do I have on"

## Purpose
Search personal knowledge base using text, tags, or semantic similarity to find relevant information.

## Search Methods

### 1. Semantic Search (Recommended)
Best for conceptual queries where exact keywords may not match.

```bash
~/.claude/bin/obs/obs-wrapper semantic "<query>" --limit 10
```

**Good for:**
- "distributed systems patterns"
- "authentication approaches"
- "meeting about API redesign"

### 2. Full-Text Search
Best for finding exact phrases or keywords.

```bash
~/.claude/bin/obs/obs-wrapper search "<query>"
```

**Good for:**
- Error messages
- Specific names/terms
- Code snippets

### 3. Tag-Based Search
Best for browsing by category.

```bash
~/.claude/bin/obs/obs-wrapper search --tag "<tag>"
~/.claude/bin/obs/obs-wrapper tags --counts  # See available tags
```

**Good for:**
- "All meeting notes"
- "Project X items"
- "Decisions"

## Workflow Steps

### 1. Analyze Query
Determine best search method:
- Conceptual/fuzzy → Semantic
- Exact phrase → Full-text
- Category browse → Tags

### 2. Execute Search

Run appropriate search command(s). For comprehensive results, combine methods:

```bash
# Semantic for concepts
obs semantic "authentication best practices" --limit 5

# Text for specific terms
obs search "OAuth2"

# Tags for categories
obs search --tag "reference"
```

### 3. Present Results

Format results clearly:

```markdown
## Search Results: "<query>"

### Semantic Matches (by relevance)
1. **Note Title** (score: 0.85)
   - Path: `Projects/auth-design.md`
   - Tags: #project/api, #decision
   - Excerpt: "We decided to use OAuth2 with JWT..."

2. **Another Note** (score: 0.72)
   ...

### Text Matches
- `Reference/oauth-guide.md` - 3 matches
- `Meetings/2025-11-15.md` - 1 match

### Related Tags
- #authentication (5 notes)
- #security (12 notes)
```

### 4. Offer Actions

- "Want me to read [Note Title] in full?"
- "Should I search with different terms?"
- "Would you like to see all notes with tag X?"

## Tips

- **No results?** Try broader terms or check `obs tags` for available categories
- **Too many results?** Add tag filters: `obs search "query" --tag "project/x"`
- **Stale embeddings?** Run `obs embed` to update

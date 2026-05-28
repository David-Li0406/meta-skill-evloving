# Artifact Discovery Workflow

Guided workflow for discovering Claude Code artifacts based on natural language queries.

---

## Overview

This workflow transforms user queries like "I need something for PDF processing" into targeted artifact recommendations using the SkillMeat scoring and matching system.

**Capabilities**:
- Natural language query → structured search
- Confidence-scored results (trust + quality + relevance)
- Semantic matching (when available) + keyword fallback
- Project context awareness
- Multi-artifact recommendations for complex tasks

**When to Use**:
- User asks "what skills/artifacts are available for X?"
- User describes a capability need ("I need to process PDFs")
- Agent identifies capability gap during development
- User wants to browse artifacts by category

---

## Workflow Steps

### Step 1: Parse User Intent

Classify the user's request into one of these intent categories:

| Intent | Example Query | Action |
|--------|--------------|--------|
| **Search** | "Find PDF tools" | Search for specific capability |
| **List** | "What skills do I have?" | List artifacts in collection |
| **Show** | "Tell me about canvas" | Show details of specific artifact |
| **Browse** | "Show me all database skills" | Browse by type/category |
| **Recommend** | "What should I add for React?" | Analyze project context |

**Parsing Rules**:
- Contains "find", "search", "look for" → **Search**
- Contains "what do I have", "list", "show all" → **List**
- Contains "tell me about", "show me", "details" + specific name → **Show**
- Contains "all", "every", category name → **Browse**
- Contains "recommend", "suggest", "should I add" → **Recommend**

---

### Step 2: Execute Query

Execute the appropriate command based on intent classification.

#### Intent: Search

Use the confidence scoring API for best results:

```bash
# Call the match API via CLI (if available, PRD-001 Phase 6)
skillmeat match "<query>" --json --min-confidence 70

# Fallback to keyword search if match API unavailable
skillmeat search "<query>" --json --type <type>
```

**Query Refinement**:
- Extract key terms from user query
- Include artifact type if mentioned (skill, command, agent, mcp)
- Preserve semantic meaning (don't over-simplify)

**Examples**:
```bash
# User: "Find tools for working with PDFs"
skillmeat match "pdf processing tools" --json --min-confidence 70

# User: "I need a React component library"
skillmeat match "react components ui library" --json --min-confidence 70

# User: "Database migration tools"
skillmeat match "database migration" --json --type skill
```

#### Intent: List

```bash
# List all artifacts in collection
skillmeat list --json

# List by type
skillmeat list --type skill --json

# List deployed in project
skillmeat list --project . --json
```

#### Intent: Show

```bash
# Show artifact details
skillmeat show <artifact-name> --json

# Show full details including dependencies
skillmeat show <artifact-name> --full --json
```

#### Intent: Browse

```bash
# Browse by type
skillmeat search "" --type <type> --json

# Browse all
skillmeat list --json
```

#### Intent: Recommend

Analyze project context first:

```bash
# Use project analysis script
node .claude/skills/skillmeat-cli/scripts/analyze-project.js .
```

Then search for recommended artifacts:
```bash
# For each recommendation
skillmeat match "<artifact-category>" --json
```

---

### Step 3: Apply Filters

Filter results based on confidence scores and relevance.

#### Confidence Thresholds

| Threshold | Use Case | Description |
|-----------|----------|-------------|
| ≥90 | High confidence | Official/verified artifacts, strong match |
| 70-89 | Good match | Community-vetted, relevant to query |
| 50-69 | Possible match | May be relevant, review recommended |
| <50 | Low confidence | Weak match, show only if few results |

**Filtering Logic**:
```javascript
// Parse JSON response
const response = JSON.parse(stdout);

// Filter by confidence threshold
const highConfidence = response.matches.filter(m => m.confidence >= 90);
const goodMatch = response.matches.filter(m => m.confidence >= 70 && m.confidence < 90);
const possibleMatch = response.matches.filter(m => m.confidence >= 50 && m.confidence < 70);

// Present high confidence first, then good matches
const recommended = [...highConfidence, ...goodMatch];
```

#### Type Filtering

If user specified artifact type, filter accordingly:

```javascript
const typeFilters = {
  skill: ['skill'],
  command: ['command'],
  agent: ['agent'],
  mcp: ['mcp', 'mcp-server'],
  tool: ['skill', 'command', 'mcp'],  // Broad category
};

// Apply filter
const filtered = matches.filter(m =>
  typeFilters[requestedType]?.includes(m.artifact_type)
);
```

---

### Step 4: Rank Results

Sort results by composite score (already sorted by API):

```javascript
// Results from match API are pre-sorted by confidence
// Optionally apply secondary sort criteria:

function rankMatches(matches, projectContext) {
  return matches.sort((a, b) => {
    // Primary: Confidence score (descending)
    if (b.confidence !== a.confidence) {
      return b.confidence - a.confidence;
    }

    // Secondary: Project context relevance
    const aRelevance = isRelevantToProject(a, projectContext);
    const bRelevance = isRelevantToProject(b, projectContext);
    if (aRelevance !== bRelevance) {
      return bRelevance - aRelevance;
    }

    // Tertiary: Quality score (if breakdown available)
    if (a.breakdown && b.breakdown) {
      return b.breakdown.quality_score - a.breakdown.quality_score;
    }

    return 0;
  });
}
```

---

### Step 5: Present Results

Format results for user consumption based on confidence level.

#### High Confidence Results (≥90)

Present as **strong recommendations**:

```
I found these highly relevant artifacts:

1. **pdf-processor** (95% confidence)
   Extract and manipulate PDF documents
   Source: anthropics/skills/pdf

   This is an official Anthropic skill with strong community ratings.
   Would you like me to add it to your collection?
```

#### Good Match Results (70-89)

Present as **good matches**:

```
These artifacts might help:

1. **pdf-tools** (82% confidence)
   PDF manipulation and extraction
   Source: community/pdf-tools

2. **document-processor** (75% confidence)
   Multi-format document processing (PDF, DOCX, XLSX)
   Source: community/document-processor
```

#### Multiple Results

Present top 3-5 with brief descriptions:

```
I found several PDF-related artifacts. Here are the top matches:

1. **pdf** (95%) - Official PDF processing skill
2. **pdf-forms** (88%) - PDF form filling and extraction
3. **ocr-pdf** (76%) - OCR for scanned PDFs

Would you like details on any of these, or shall I add the top match?
```

#### No Results

Suggest alternatives:

```
I didn't find any artifacts matching "rare-capability" with good confidence.

Some options:
- Search community sources: Try broader terms
- Create custom skill: I can help you build one
- Browse similar: Related artifacts that might help

Would you like to try a different search?
```

---

### Step 6: Handle Ambiguity

When query is ambiguous or multiple interpretations exist.

#### Clarify User Intent

```
I found matches in multiple categories:

Skills (3):
- pdf-processor (95%)
- pdf-forms (88%)

MCP Servers (1):
- pdf-mcp (72%)

Which type are you interested in?
```

#### Suggest Related Artifacts

```
Based on "PDF processing", you might also need:

- **docx** - For Word document processing
- **xlsx** - For Excel spreadsheet processing
- **document-converter** - Convert between formats

Would you like to see these as well?
```

#### Present Options for Complex Needs

```
For "React development", I recommend a combination:

Frontend Development:
- frontend-design (92%) - UI component patterns
- webapp-testing (88%) - Component testing

Would you like to:
[ ] Add both
[ ] Just frontend-design
[ ] See more details first
```

---

## Integration Points

### Project Context Boosting

**See**: `context-boosting.md` for comprehensive boosting rules and workflow.

For project-specific searches, apply context boosting to adjust scores:

```bash
# Get project context (cached for 5 minutes)
PROJECT_CONTEXT=$(node .claude/skills/skillmeat-cli/scripts/analyze-project.js .)

# Context boosting applies automatically in ranking step
# - Boosts matching artifacts (+15% to +25%)
# - Penalizes mismatches (-30% to -50%)
# - Suppresses duplicates (already deployed)
```

**Quick Reference**:
- React project → boost `frontend-*`, `react-*`, `webapp-*` (+20%)
- Python project → boost `python-*`, `backend-*` (+20%)
- FastAPI project → boost `openapi-*`, `api-*` (+25%)
- Already deployed → penalty (-50%)
- Language mismatch → penalty (-30%)

**Integration**: Context boosting replaces the manual `isRelevantToProject()` check in Step 4 ranking with automated score adjustments.

### Confidence API Integration

When PRD-001 Phase 6 match API is available:

```bash
# Use match endpoint with confidence scoring
curl "http://localhost:8080/api/v1/match?q=pdf+tools&limit=10&min_confidence=70&include_breakdown=true"

# Parse response
{
  "query": "pdf tools",
  "matches": [
    {
      "artifact_id": "skill:pdf-processor",
      "name": "pdf-processor",
      "confidence": 95.2,
      "breakdown": {
        "trust_score": 98.0,
        "quality_score": 94.5,
        "match_score": 93.0,
        "semantic_used": true
      }
    }
  ],
  "degraded": false
}
```

**Degradation Handling**:
```javascript
if (response.degraded) {
  console.log("Note: Using keyword-only matching (semantic search unavailable)");
  console.log(`Reason: ${response.degradation_reason}`);
}
```

### Fallback to Keyword Search

When match API is unavailable:

```bash
# Use traditional search
skillmeat search "<query>" --json --type <type>

# Post-process results (no confidence scores)
# Apply heuristic ranking based on:
# 1. Name exact match
# 2. Description keyword frequency
# 3. Source trust (official > community)
```

---

## Error Handling

### Empty Results

```
No artifacts found for "<query>".

Suggestions:
- Try broader terms (e.g., "document" instead of "PDF extraction")
- Check spelling
- Browse all artifacts: skillmeat list
```

### API Errors

```
I couldn't search for artifacts right now.

Possible issues:
- Network connectivity: Check internet connection
- Rate limiting: Set GitHub token with `skillmeat config set github-token <token>`
- Service unavailable: Try again in a moment

Would you like to browse your local collection instead?
```

### Ambiguous Query

```
Your query "<vague-term>" is very broad. Did you mean:

- PDF processing
- Document conversion
- File parsing

Please specify what you're looking for.
```

---

## Examples

### Example 1: Simple Search

**User**: "Find PDF tools"

**Workflow**:
1. **Intent**: Search
2. **Query**: `skillmeat match "pdf tools" --json --min-confidence 70`
3. **Filter**: Confidence ≥70
4. **Rank**: By confidence (descending)
5. **Present**:
   ```
   Top match: pdf-processor (95% confidence)
   - Official Anthropic skill for PDF processing
   - Extract text, fill forms, merge/split documents

   Would you like me to add it?
   ```

### Example 2: Project-Aware Recommendation

**User**: "What should I add for my React project?"

**Workflow**:
1. **Intent**: Recommend
2. **Analyze**: Run `analyze-project.js .`
3. **Query**: `skillmeat match "react development" --json`
4. **Boost**: Prioritize React-tagged artifacts
5. **Present**:
   ```
   For your React project (Next.js detected), I recommend:

   1. frontend-design (92%) - Already deployed ✓
   2. webapp-testing (88%) - Component testing with Jest/RTL

   Would you like to add webapp-testing?
   ```

### Example 3: Multiple Results

**User**: "Find database skills"

**Workflow**:
1. **Intent**: Search
2. **Query**: `skillmeat match "database" --json --type skill`
3. **Filter**: Confidence ≥70
4. **Rank**: By confidence
5. **Present**:
   ```
   I found 4 database-related skills:

   1. postgresql-psql (94%) - PostgreSQL database management
   2. mysql-tools (86%) - MySQL utilities and queries
   3. sqlite-manager (82%) - SQLite database operations
   4. database-migrations (75%) - Schema migration tools

   Which one interests you? Or would you like to see all details?
   ```

### Example 4: No Results, Suggest Alternatives

**User**: "Find quantum computing tools"

**Workflow**:
1. **Intent**: Search
2. **Query**: `skillmeat match "quantum computing" --json`
3. **Filter**: All results below threshold
4. **Present**:
   ```
   I didn't find any quantum computing artifacts with good confidence.

   This might be a specialized need. Options:
   - Create a custom skill (I can help with skill-builder)
   - Search broader: "scientific computing" or "simulation"
   - Check community sources: skillmeat config add-source <url>

   Would you like to try a different approach?
   ```

---

## Best Practices

### Query Construction

**DO**:
- Preserve user's semantic intent
- Include artifact type if mentioned
- Use descriptive terms (not just keywords)

**DON'T**:
- Over-simplify to single keywords
- Add terms user didn't mention
- Assume artifact names (search, don't guess)

### Result Presentation

**DO**:
- Show confidence scores for transparency
- Explain why artifact matches (use description)
- Offer to show more details
- Limit initial results to top 3-5

**DON'T**:
- Overwhelm with full list
- Auto-deploy without permission
- Suggest low-confidence matches as strong recommendations
- Hide confidence information

### Permission Protocol

**Always**:
- Ask before deploying artifacts
- Show what will change (file paths)
- Confirm after successful deployment
- Accept "no" gracefully

**Never**:
- Auto-deploy without explicit permission
- Suggest repeatedly after user declines
- Assume user wants multiple artifacts

---

## Reference

### Related Scripts

- `analyze-project.js` - Project context analysis
- See `scripts/` directory for utilities

### Related Workflows

- `context-boosting.md` - Project-aware score adjustments and ranking
- `agent-self-enhancement.md` - When to suggest artifacts during development

### API Documentation

- Match endpoint: `/api/v1/match` (PRD-001 Phase 6)
- Scoring service: `skillmeat.core.scoring.service`
- Schema: `skillmeat.api.schemas.match`

### Command Reference

- `skillmeat search` - Keyword search
- `skillmeat match` - Confidence-scored search (when available)
- `skillmeat list` - List artifacts
- `skillmeat show` - Artifact details
- `skillmeat add` - Add to collection
- `skillmeat deploy` - Deploy to project

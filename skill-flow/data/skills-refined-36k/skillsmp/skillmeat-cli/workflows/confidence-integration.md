# Confidence Scoring Integration

Integration guide for using the PRD-001 Confidence Scoring System with the skillmeat-cli skill for intelligent artifact matching.

---

## Overview

The confidence scoring system provides AI-powered artifact recommendations using:
- **Semantic similarity**: Embeddings-based relevance (cosine distance)
- **Keyword matching**: Traditional text matching with partial support
- **Quality scoring**: GitHub stars, update frequency, community ratings
- **Trust scoring**: Verified sources, user ratings, historical success

**Benefits**:
- More accurate recommendations than keyword-only search
- Confidence transparency (users see why artifacts match)
- Graceful degradation to keyword-only when embeddings unavailable
- Context-aware boosting based on project type

**Trade-offs**:
- Requires backend API server running (fallback to CLI search available)
- Semantic scoring requires API key (defaults to keyword-only without)
- Slightly slower than pure keyword search (~500ms vs 50ms)

---

## API Reference

### Match Endpoint

**URL**: `POST /api/v1/match` or `GET /api/v1/match?q=<query>`

**Request**:
```json
{
  "query": "pdf processing",
  "context": {
    "project_type": "python",
    "deployed_artifacts": ["docx", "xlsx"]
  },
  "limit": 10,
  "min_confidence": 70,
  "include_breakdown": true
}
```

**Response**:
```json
{
  "query": "pdf processing",
  "matches": [
    {
      "artifact_id": "skill:pdf-processor",
      "name": "pdf-processor",
      "artifact_type": "skill",
      "confidence": 87.3,
      "title": "PDF Processing Tool",
      "description": "Extract and manipulate PDF documents",
      "breakdown": {
        "trust_score": 90.0,
        "quality_score": 85.0,
        "match_score": 87.0,
        "semantic_used": true,
        "context_boost_applied": false
      }
    }
  ],
  "total": 47,
  "limit": 10,
  "min_confidence": 70.0,
  "schema_version": "1.0.0",
  "scored_at": "2025-12-24T10:30:00Z",
  "degraded": false,
  "degradation_reason": null
}
```

**Degradation Response** (semantic unavailable):
```json
{
  "query": "pdf processing",
  "matches": [...],
  "degraded": true,
  "degradation_reason": "Embedding service unavailable: no API key configured"
}
```

### CLI Match Command

**Availability**: Check if `skillmeat match` command exists:

```bash
# Check command availability
skillmeat match --help 2>/dev/null && echo "✓ Available" || echo "✗ Not available"
```

**Usage**:
```bash
# Basic match
skillmeat match "pdf processing" --json

# With filters
skillmeat match "pdf processing" --json --min-confidence 70 --limit 10

# With breakdown
skillmeat match "pdf processing" --json --include-breakdown

# With context (auto-detected from project)
skillmeat match "pdf processing" --json --context-project .
```

**Fallback** (if `match` command unavailable):
```bash
# Use traditional search
skillmeat search "pdf processing" --json --type skill
```

---

## Score Interpretation Guide

### Confidence Thresholds

| Range | Recommendation Level | User Message | Action |
|-------|---------------------|--------------|--------|
| 90-100 | **Excellent match** | "This is highly relevant" | Recommend directly, offer to add |
| 85-89 | **Very good match** | "This is very relevant" | Recommend, explain why |
| 70-84 | **Good match** | "This might help" | Present as option, brief description |
| 50-69 | **Possible match** | "Possibly relevant" | Show only if few alternatives |
| 0-49 | **Poor match** | (don't show) | Filter out |

### Score Component Breakdown

When `breakdown` is included in response:

#### Trust Score (0-100)
- **90-100**: Official Anthropic artifact or verified publisher
- **70-89**: Established community publisher with track record
- **50-69**: Community artifact with some history
- **0-49**: New or unverified publisher

**User Message**:
```
Trust: 95/100 - Official Anthropic skill ✓
Trust: 82/100 - Verified community publisher
Trust: 45/100 - New community artifact
```

#### Quality Score (0-100)
- **90-100**: High GitHub stars (>500), recent updates, good ratings
- **70-89**: Moderate stars (100-500), actively maintained
- **50-69**: Low stars (<100) or infrequent updates
- **0-49**: No stars, unmaintained, or poor ratings

**User Message**:
```
Quality: 92/100 - 750 GitHub stars, updated last week
Quality: 78/100 - 200 stars, updated last month
Quality: 55/100 - 30 stars, last updated 6 months ago
```

#### Match Score (0-100)
- **90-100**: Very strong semantic/keyword match
- **70-89**: Good match, relevant terms present
- **50-69**: Partial match, some relevant terms
- **0-49**: Weak match, few relevant terms

**User Message**:
```
Relevance: 94/100 - Strong semantic match ✓
Relevance: 76/100 - Good keyword match
Relevance: 58/100 - Partial match (consider broader search)
```

#### Semantic vs Keyword

**Semantic Used** (`semantic_used: true`):
- Higher accuracy for conceptual matches
- Understands synonyms and related concepts
- Example: "pdf" matches "document processing"

**Keyword Only** (`semantic_used: false`):
- Exact or partial text matching
- Faster but less intelligent
- Shown when: API key missing, service unavailable, or timeout

**User Message**:
```
# Semantic
Using advanced semantic matching for best results ✓

# Keyword (degraded)
Note: Using keyword-only matching (semantic search unavailable)
Reason: No API key configured - set ANTHROPIC_API_KEY for better results
```

---

## Context Boosting Rules

### Project Type Detection

Use `analyze-project.js` to detect project types:

```bash
# Get project context
PROJECT_CONTEXT=$(node .claude/skills/skillmeat-cli/scripts/analyze-project.js .)

# Extract project types (example output)
# {
#   "projectTypes": ["python", "fastapi", "react", "nextjs"],
#   "languages": ["python", "typescript"],
#   "frameworks": ["fastapi", "nextjs"]
# }
```

### Boost Calculation

**Context boost**: +15-20% to artifacts matching project type

```javascript
// Example boost logic (handled by backend, shown for transparency)
function applyContextBoost(artifact, projectContext) {
  const projectTypes = projectContext.projectTypes || [];
  const artifactTags = artifact.metadata?.tags || [];

  // Check for overlap
  const overlap = projectTypes.filter(type =>
    artifactTags.some(tag => tag.toLowerCase().includes(type.toLowerCase()))
  );

  if (overlap.length > 0) {
    // Boost by 15-20% based on overlap strength
    const boostFactor = Math.min(20, 15 + (overlap.length * 5));
    return artifact.confidence * (1 + boostFactor / 100);
  }

  return artifact.confidence;
}
```

**Example**:
```
# Without context
pdf-processor: 75/100

# With Python project context + artifact has "python" tag
pdf-processor: 86/100 (+15% context boost)
```

### Already-Deployed Artifacts

**Lower priority** for artifacts already deployed to current project:

```javascript
function adjustForDeployed(artifact, deployedArtifacts) {
  if (deployedArtifacts.includes(artifact.name)) {
    // Reduce score by 10-15% (already have it)
    return artifact.confidence * 0.85;
  }
  return artifact.confidence;
}
```

**User Message**:
```
pdf-processor (75%) - Already deployed to this project ✓
```

### Combining Boosts

**Order of operations**:
1. Base confidence from scoring system
2. Apply context boost (+15-20% if matches project)
3. Apply deployed penalty (-15% if already deployed)
4. Clamp to 0-100 range

**Example**:
```
Base score: 70
+ Context boost (Python match): +15% → 80.5
- Already deployed: -15% → 68.4
Final score: 68/100
```

---

## Fallback Procedures

### Detect API Availability

```bash
# Check if API server is running
API_AVAILABLE=$(curl -s http://localhost:8080/health && echo "true" || echo "false")

# Check if match endpoint exists
MATCH_AVAILABLE=$(curl -s http://localhost:8080/api/v1/match?q=test \
  -w "%{http_code}" -o /dev/null | grep -q "^[24]" && echo "true" || echo "false")
```

### Fallback Decision Tree

```
Is API server running?
├─ No → Use CLI search (keyword-only)
└─ Yes → Is match endpoint available?
    ├─ No → Use CLI search
    └─ Yes → Use match API
        └─ Response.degraded = true?
            └─ Yes → Warn user about keyword-only mode
```

### Fallback Implementation

```javascript
async function getMatches(query, options = {}) {
  try {
    // Try match API first
    const response = await fetch('http://localhost:8080/api/v1/match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query,
        limit: options.limit || 10,
        min_confidence: options.minConfidence || 70,
        include_breakdown: true,
      }),
    });

    if (response.ok) {
      const data = await response.json();

      // Warn if degraded
      if (data.degraded) {
        console.warn(`Note: Using keyword-only matching`);
        console.warn(`Reason: ${data.degradation_reason}`);
      }

      return data.matches;
    }

    // API error, fall back to CLI
    throw new Error(`API error: ${response.status}`);

  } catch (error) {
    // Fall back to CLI search
    console.warn('Match API unavailable, using keyword search');
    return await fallbackToCliSearch(query, options);
  }
}

async function fallbackToCliSearch(query, options = {}) {
  const { execSync } = require('child_process');

  // Build CLI command
  let cmd = `skillmeat search "${query}" --json`;
  if (options.type) cmd += ` --type ${options.type}`;
  if (options.limit) cmd += ` --limit ${options.limit}`;

  // Execute and parse
  const stdout = execSync(cmd, { encoding: 'utf-8' });
  const results = JSON.parse(stdout);

  // Convert to match format (no confidence scores)
  return results.map(artifact => ({
    artifact_id: `${artifact.type}:${artifact.name}`,
    name: artifact.name,
    artifact_type: artifact.type,
    confidence: 0, // Unknown (keyword search has no scoring)
    title: artifact.metadata?.title || artifact.name,
    description: artifact.metadata?.description,
    breakdown: null, // No breakdown for keyword search
  }));
}
```

### User Messaging for Fallbacks

**API unavailable**:
```
Note: Artifact scoring API is not available. Using basic keyword search.

To enable intelligent matching:
1. Start the API server: skillmeat web dev --api-only
2. Or search your local collection: skillmeat list
```

**Degraded to keyword-only**:
```
Note: Using keyword-only matching (semantic search unavailable)
Reason: No API key configured

To enable semantic matching for better results:
1. Set ANTHROPIC_API_KEY environment variable
2. Restart the API server: skillmeat web dev --api-only
```

**Timeout**:
```
Note: Semantic scoring timed out, using keyword-only results
Results may be less accurate. Try again or use broader search terms.
```

---

## Example Flows

### Flow 1: Successful Semantic Match

**User**: "Find PDF tools"

**Workflow**:
```bash
# 1. Check API availability
curl -s http://localhost:8080/health
# → 200 OK

# 2. Call match API
curl -X POST http://localhost:8080/api/v1/match \
  -H "Content-Type: application/json" \
  -d '{
    "query": "pdf tools",
    "limit": 10,
    "min_confidence": 70,
    "include_breakdown": true
  }'

# 3. Parse response
{
  "query": "pdf tools",
  "matches": [
    {
      "artifact_id": "skill:pdf-processor",
      "name": "pdf-processor",
      "confidence": 94.5,
      "breakdown": {
        "trust_score": 95.0,
        "quality_score": 92.0,
        "match_score": 96.0,
        "semantic_used": true
      }
    }
  ],
  "degraded": false
}
```

**User Message**:
```
I found an excellent match:

pdf-processor (95% confidence)
  Extract and manipulate PDF documents

  Why this matches:
  ✓ Strong semantic match (96/100)
  ✓ High quality - 750 GitHub stars (92/100)
  ✓ Official Anthropic skill (95/100)
  ✓ Using advanced semantic matching

Would you like me to add it to your collection?
```

### Flow 2: Degraded to Keyword-Only

**User**: "Find PDF tools"

**Workflow**:
```bash
# 1. Call match API (no API key configured)
curl -X POST http://localhost:8080/api/v1/match \
  -H "Content-Type: application/json" \
  -d '{"query": "pdf tools", "min_confidence": 70}'

# 2. Parse response (degraded)
{
  "query": "pdf tools",
  "matches": [
    {
      "artifact_id": "skill:pdf-processor",
      "name": "pdf-processor",
      "confidence": 76.0,
      "breakdown": {
        "trust_score": 95.0,
        "quality_score": 92.0,
        "match_score": 58.0,
        "semantic_used": false
      }
    }
  ],
  "degraded": true,
  "degradation_reason": "Embedding service unavailable: no API key configured"
}
```

**User Message**:
```
Note: Using keyword-only matching (semantic search unavailable)
Reason: No API key configured - set ANTHROPIC_API_KEY for better results

I found a good match:

pdf-processor (76% confidence)
  Extract and manipulate PDF documents

  Why this matches:
  ≈ Keyword match (58/100)
  ✓ High quality - 750 GitHub stars (92/100)
  ✓ Official Anthropic skill (95/100)

Would you like me to add it?
```

### Flow 3: API Unavailable, Fallback to CLI

**User**: "Find PDF tools"

**Workflow**:
```bash
# 1. Try match API
curl -s http://localhost:8080/api/v1/match
# → Connection refused

# 2. Fall back to CLI search
skillmeat search "pdf" --json --type skill

# 3. Parse results (no confidence scores)
[
  {
    "name": "pdf-processor",
    "type": "skill",
    "metadata": {
      "title": "PDF Processing Tool",
      "description": "Extract and manipulate PDF documents"
    }
  }
]
```

**User Message**:
```
Note: Artifact scoring API is not available. Using basic keyword search.

I found these PDF-related skills:

1. pdf-processor
   Extract and manipulate PDF documents

2. pdf-forms
   Fill and extract PDF forms

To enable intelligent matching, start the API server:
  skillmeat web dev --api-only

Would you like to see details for any of these?
```

### Flow 4: Context-Boosted Match

**User**: "Find React component tools" (in Next.js project)

**Workflow**:
```bash
# 1. Detect project context
PROJECT_CONTEXT=$(node .claude/skills/skillmeat-cli/scripts/analyze-project.js .)
# → {"projectTypes": ["nextjs", "react", "typescript"]}

# 2. Call match API with context
curl -X POST http://localhost:8080/api/v1/match \
  -H "Content-Type: application/json" \
  -d '{
    "query": "react component library",
    "context": {"project_type": "nextjs"},
    "min_confidence": 70
  }'

# 3. Parse response (boosted)
{
  "matches": [
    {
      "artifact_id": "skill:frontend-design",
      "name": "frontend-design",
      "confidence": 89.0,
      "breakdown": {
        "trust_score": 90.0,
        "quality_score": 85.0,
        "match_score": 84.0,
        "semantic_used": true,
        "context_boost_applied": true
      }
    }
  ]
}
```

**User Message**:
```
For your Next.js project, I recommend:

frontend-design (89% confidence)
  React component patterns and UI libraries

  Why this matches:
  ✓ Strong semantic match (84/100)
  ✓ Boosted for Next.js/React projects (+15%)
  ✓ High quality - 320 GitHub stars (85/100)
  ✓ Verified community publisher (90/100)

Would you like me to add it?
```

---

## Best Practices

### When to Use Match API

**DO use match API when**:
- User asks for recommendations ("find tools for X")
- Comparing multiple artifacts (semantic helps rank)
- User query is conceptual ("document processing" vs "pdf")
- Need transparency (confidence breakdown)

**DON'T use match API when**:
- User specifies exact artifact name ("add pdf-processor")
- Simple list operation ("show all skills")
- API server not running (use CLI fallback)
- Performance critical (CLI search is faster)

### Error Handling

**DO**:
- Always provide fallback to CLI search
- Warn user when degraded to keyword-only
- Show specific error messages (API key missing, timeout, etc.)
- Offer solutions (how to fix degradation)

**DON'T**:
- Fail silently (user should know about degradation)
- Hide confidence scores (transparency builds trust)
- Recommend low-confidence matches without context
- Ignore degradation_reason field

### Result Presentation

**DO**:
- Show confidence scores prominently
- Explain why artifact matches (use breakdown)
- Limit to top 3-5 results initially
- Offer to show more if user interested

**DON'T**:
- Show results below 50 confidence
- Overwhelm with full list
- Auto-deploy without permission
- Hide degradation status

---

## Reference

### API Schema

- **Request**: `MatchRequest` (query, context, filters)
- **Response**: `MatchResponse` (matches with confidence)
- **Breakdown**: `ScoreBreakdown` (trust, quality, match scores)

### Scoring Components

- **SemanticScorer**: Embedding-based similarity (cosine distance)
- **MatchAnalyzer**: Keyword matching with partial support
- **QualityScorer**: GitHub stars, update frequency
- **TrustScorer**: Verified sources, user ratings

### Related Files

- **API Client**: `skillmeat/api/routers/match.py`
- **Scoring Service**: `skillmeat/core/scoring/service.py`
- **Schema**: `skillmeat/api/schemas/match.py`
- **Models**: `skillmeat/core/scoring/models.py`

### CLI Commands

```bash
# Match (when available)
skillmeat match "<query>" --json --min-confidence 70

# Search (fallback)
skillmeat search "<query>" --json --type <type>

# List (no scoring)
skillmeat list --json

# Show (specific artifact)
skillmeat show <name> --json
```

### Environment Variables

```bash
# Enable semantic scoring
export ANTHROPIC_API_KEY="sk-ant-..."

# Configure API server
export NEXT_PUBLIC_API_URL="http://localhost:8080"
export NEXT_PUBLIC_API_VERSION="v1"
```

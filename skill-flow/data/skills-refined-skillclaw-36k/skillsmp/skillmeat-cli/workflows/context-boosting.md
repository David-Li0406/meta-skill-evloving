# Project Context Boosting Workflow

Boost artifact relevance scores based on project context for more accurate recommendations.

---

## Overview

This workflow enhances artifact discovery by analyzing the current project and adjusting relevance scores based on project type, language, framework, and existing deployments.

**Capabilities**:
- Automatic project type detection (React, Python, FastAPI, etc.)
- Score boosting for matching artifacts (+15% to +25%)
- Penalty application for mismatches (-30% to -50%)
- Duplicate detection (already deployed artifacts)
- Language and framework awareness
- Result re-ranking based on adjusted scores

**When to Use**:
- User asks for recommendations ("what should I add?")
- Agent identifies capability gap during development
- Discovery workflow needs project-specific ranking
- Auto-suggesting artifacts based on context

**Token Efficiency**: Project analysis cached for 5 minutes, ~2KB per analysis

---

## Workflow Steps

### Step 1: Detect Project Context

Run the project analysis script to identify project characteristics.

```bash
node .claude/skills/skillmeat-cli/scripts/analyze-project.js <project-path>
```

**Default**: Use current directory (`.`) if no path specified.

**Output Format**:
```json
{
  "projectPath": "/path/to/project",
  "projectTypes": ["react", "typescript", "nextjs"],
  "indicators": ["package.json", "tsconfig.json", "next.config.js"],
  "deployed": ["frontend-design", "canvas"],
  "recommendations": [
    {
      "artifact": "webapp-testing",
      "reason": "React project detected"
    }
  ],
  "summary": "Found 1 artifact(s) that could help with this project"
}
```

**Project Types Detected**:
- `react` - React library detected in dependencies
- `nextjs` - Next.js framework detected
- `python` - Python project (pyproject.toml/requirements.txt)
- `fastapi` - FastAPI framework detected in dependencies
- `typescript` - TypeScript configured
- `claude-code` - Claude Code project (.claude directory exists)

---

### Step 2: Cache Analysis Results

Cache project analysis to avoid repeated file I/O.

**Cache Key**: `project_analysis_${absolutePath}_${mtime}`

**Cache Duration**: 5 minutes

**Invalidation Triggers**:
- `package.json` modified (Node.js projects)
- `pyproject.toml` modified (Python projects)
- `requirements.txt` modified (Python projects)
- `.claude/skills/` directory modified (deployment changes)
- Cache TTL expired (5 minutes)

**Implementation**:
```javascript
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes
const cache = new Map();

async function getCachedAnalysis(projectPath) {
  const cacheKey = await getCacheKey(projectPath);
  const cached = cache.get(cacheKey);

  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }

  // Run fresh analysis
  const analysis = await analyzeProject(projectPath);

  cache.set(cacheKey, {
    data: analysis,
    timestamp: Date.now(),
  });

  return analysis;
}

async function getCacheKey(projectPath) {
  const absolutePath = path.resolve(projectPath);

  // Get mtime of indicator files
  const indicators = ['package.json', 'pyproject.toml', '.claude/skills'];
  const mtimes = [];

  for (const indicator of indicators) {
    const indicatorPath = path.join(absolutePath, indicator);
    try {
      const stats = await fs.stat(indicatorPath);
      mtimes.push(stats.mtimeMs);
    } catch {
      // File doesn't exist
    }
  }

  return `${absolutePath}_${mtimes.join('_')}`;
}
```

---

### Step 3: Apply Boosting Rules

Adjust artifact scores based on project type matching.

#### Boost Amounts by Project Type

| Project Type | Boost Artifacts Matching | Boost Amount |
|-------------|-------------------------|--------------|
| React | `frontend-*`, `react-*`, `webapp-*`, `ui-*` | +20% |
| Python | `python-*`, `backend-*`, `*-py` | +20% |
| FastAPI | `openapi-*`, `api-*`, `fastapi-*` | +25% |
| Next.js | `frontend-*`, `vercel-*`, `nextjs-*` | +20% |
| TypeScript | `typescript-*`, `type-*`, `ts-*` | +15% |
| Node.js | `node-*`, `npm-*`, `nodejs-*` | +15% |

**Pattern Matching Rules**:
- Artifact name starts with prefix → boost applies
- Artifact tags include project type → boost applies
- Artifact description mentions project type → half boost applies

**Example**:
```javascript
function calculateBoost(artifact, projectTypes) {
  let totalBoost = 0;

  for (const projectType of projectTypes) {
    const boostConfig = BOOST_RULES[projectType];
    if (!boostConfig) continue;

    // Check name prefix
    const nameMatch = boostConfig.patterns.some(pattern =>
      artifact.name.match(new RegExp(`^${pattern.replace('*', '.*')}$`))
    );

    // Check tags
    const tagMatch = artifact.metadata?.tags?.includes(projectType);

    // Check description
    const descMatch = artifact.description?.toLowerCase().includes(projectType);

    if (nameMatch || tagMatch) {
      totalBoost += boostConfig.boost;
    } else if (descMatch) {
      totalBoost += boostConfig.boost * 0.5; // Half boost for description match
    }
  }

  return totalBoost;
}
```

#### Boost Configuration

```javascript
const BOOST_RULES = {
  react: {
    patterns: ['frontend-*', 'react-*', 'webapp-*', 'ui-*'],
    boost: 0.20,
  },
  python: {
    patterns: ['python-*', 'backend-*', '*-py'],
    boost: 0.20,
  },
  fastapi: {
    patterns: ['openapi-*', 'api-*', 'fastapi-*'],
    boost: 0.25,
  },
  nextjs: {
    patterns: ['frontend-*', 'vercel-*', 'nextjs-*'],
    boost: 0.20,
  },
  typescript: {
    patterns: ['typescript-*', 'type-*', 'ts-*'],
    boost: 0.15,
  },
  nodejs: {
    patterns: ['node-*', 'npm-*', 'nodejs-*'],
    boost: 0.15,
  },
};
```

---

### Step 4: Apply Penalty Rules

Reduce scores for artifacts that don't match project context.

#### Penalty Amounts

| Condition | Penalty | Reason |
|-----------|---------|--------|
| Already deployed | -50% | Avoid duplicate recommendations |
| Wrong language | -30% | Python skill for Node project, etc. |
| Wrong framework | -20% | Vue skill for React project |
| Deprecated | -40% | Should not be recommended |
| Incompatible | -60% | Cannot work in this project type |

**Language Detection**:
```javascript
const LANGUAGE_INDICATORS = {
  python: ['python', 'fastapi'],
  javascript: ['react', 'nextjs', 'nodejs', 'typescript'],
  typescript: ['typescript', 'nextjs'],
};

function detectLanguage(projectTypes) {
  for (const [lang, indicators] of Object.entries(LANGUAGE_INDICATORS)) {
    if (projectTypes.some(type => indicators.includes(type))) {
      return lang;
    }
  }
  return null;
}

function getLanguagePenalty(artifact, projectLanguage) {
  const artifactLanguage = detectArtifactLanguage(artifact);

  if (!artifactLanguage || !projectLanguage) {
    return 0; // No penalty if language unclear
  }

  // TypeScript is compatible with JavaScript
  if (
    (artifactLanguage === 'typescript' && projectLanguage === 'javascript') ||
    (artifactLanguage === 'javascript' && projectLanguage === 'typescript')
  ) {
    return 0;
  }

  if (artifactLanguage !== projectLanguage) {
    return -0.30; // -30% for language mismatch
  }

  return 0;
}
```

**Duplicate Detection**:
```javascript
function isDuplicate(artifact, deployedArtifacts) {
  return deployedArtifacts.includes(artifact.name);
}

function getDuplicatePenalty(artifact, deployedArtifacts) {
  return isDuplicate(artifact, deployedArtifacts) ? -0.50 : 0;
}
```

**Deprecation Check**:
```javascript
function getDeprecationPenalty(artifact) {
  if (artifact.metadata?.deprecated === true) {
    return -0.40;
  }
  if (artifact.metadata?.status === 'deprecated') {
    return -0.40;
  }
  return 0;
}
```

#### Combined Penalty Calculation

```javascript
function calculatePenalty(artifact, projectContext) {
  let totalPenalty = 0;

  // Check duplicate
  totalPenalty += getDuplicatePenalty(artifact, projectContext.deployed);

  // Check language mismatch
  const projectLanguage = detectLanguage(projectContext.projectTypes);
  totalPenalty += getLanguagePenalty(artifact, projectLanguage);

  // Check deprecation
  totalPenalty += getDeprecationPenalty(artifact);

  // Cap minimum at -60% (keep some score)
  return Math.max(totalPenalty, -0.60);
}
```

---

### Step 5: Calculate Adjusted Scores

Combine base confidence score with boost/penalty adjustments.

**Formula**:
```
adjusted_score = base_score * (1 + boost + penalty)
```

**Constraints**:
- Minimum score: 0 (cannot go negative)
- Maximum score: 100 (cap at 100%)
- Penalties stack additively
- Boosts stack additively
- Final adjustment clamped to [-60%, +100%]

**Implementation**:
```javascript
function adjustScore(artifact, baseScore, projectContext) {
  const boost = calculateBoost(artifact, projectContext.projectTypes);
  const penalty = calculatePenalty(artifact, projectContext);

  // Calculate adjustment (boost + penalty)
  const adjustment = boost + penalty;

  // Clamp adjustment to reasonable range
  const clampedAdjustment = Math.max(-0.60, Math.min(1.00, adjustment));

  // Apply to base score
  const adjustedScore = baseScore * (1 + clampedAdjustment);

  // Clamp final score to [0, 100]
  return Math.max(0, Math.min(100, adjustedScore));
}
```

**Example Calculations**:

```javascript
// Example 1: React project, frontend artifact
// Base: 85, Boost: +20%, Penalty: 0
adjusted = 85 * (1 + 0.20 + 0) = 102 → clamped to 100

// Example 2: React project, Python artifact
// Base: 75, Boost: 0, Penalty: -30% (language mismatch)
adjusted = 75 * (1 + 0 - 0.30) = 52.5

// Example 3: React project, already deployed
// Base: 90, Boost: +20%, Penalty: -50% (duplicate)
adjusted = 90 * (1 + 0.20 - 0.50) = 63

// Example 4: React project, deprecated Python artifact
// Base: 60, Boost: 0, Penalty: -30% - 40% = -60% (clamped)
adjusted = 60 * (1 + 0 - 0.60) = 24
```

---

### Step 6: Re-rank Results

Sort artifacts by adjusted scores (descending).

```javascript
function rerankResults(matches, projectContext) {
  // Calculate adjusted scores for all matches
  const scored = matches.map(match => ({
    ...match,
    baseScore: match.confidence || match.score || 0,
    adjustedScore: adjustScore(
      match,
      match.confidence || match.score || 0,
      projectContext
    ),
    boost: calculateBoost(match, projectContext.projectTypes),
    penalty: calculatePenalty(match, projectContext),
  }));

  // Sort by adjusted score (descending)
  scored.sort((a, b) => b.adjustedScore - a.adjustedScore);

  return scored;
}
```

**Explanation in Results**:
Include adjustment details for transparency:

```javascript
function formatResult(match) {
  const parts = [];

  if (match.boost > 0) {
    parts.push(`+${(match.boost * 100).toFixed(0)}% (project match)`);
  }

  if (match.penalty < 0) {
    const reasons = [];
    if (isDuplicate(match, projectContext.deployed)) {
      reasons.push('already deployed');
    }
    if (getLanguagePenalty(match, projectLanguage) < 0) {
      reasons.push('language mismatch');
    }
    if (getDeprecationPenalty(match) < 0) {
      reasons.push('deprecated');
    }
    parts.push(`${(match.penalty * 100).toFixed(0)}% (${reasons.join(', ')})`);
  }

  return {
    name: match.name,
    score: match.adjustedScore.toFixed(1),
    baseScore: match.baseScore.toFixed(1),
    adjustments: parts.join(', '),
  };
}
```

---

## Integration with Discovery Workflow

Context boosting enhances the discovery workflow at the ranking step.

### Discovery Workflow Integration Points

**Step 2: Execute Query** (from discovery-workflow.md)

After executing query, pass results through context boosting:

```javascript
// Execute search query
const searchResults = await executeSearch(query);

// Get project context (cached)
const projectContext = await getCachedAnalysis('.');

// Apply context boosting
const boostedResults = rerankResults(searchResults, projectContext);

// Continue with discovery workflow presentation
presentResults(boostedResults);
```

### Combined Ranking Logic

Context boosting **replaces** the secondary ranking criteria in discovery workflow:

**Before** (discovery-workflow.md Step 4):
```javascript
// Secondary: Project context relevance (manual check)
const aRelevance = isRelevantToProject(a, projectContext);
```

**After** (with context boosting):
```javascript
// Secondary: Adjusted score (automated boost/penalty)
return b.adjustedScore - a.adjustedScore;
```

---

## Examples

### Example 1: React Project Recommendations

**Input**:
```bash
# Project analysis
{
  "projectTypes": ["react", "typescript", "nextjs"],
  "deployed": ["frontend-design"]
}

# Search results (base scores)
[
  { "name": "webapp-testing", "confidence": 85 },
  { "name": "frontend-design", "confidence": 92 },
  { "name": "python-backend", "confidence": 78 }
]
```

**Boosting Applied**:
```javascript
// webapp-testing: React match
boost: +20%, penalty: 0
adjusted: 85 * 1.20 = 102 → 100

// frontend-design: React match BUT already deployed
boost: +20%, penalty: -50%
adjusted: 92 * 0.70 = 64.4

// python-backend: Language mismatch
boost: 0, penalty: -30%
adjusted: 78 * 0.70 = 54.6
```

**Re-ranked Results**:
```
1. webapp-testing (100.0) ← Boosted from 85
   Base: 85.0 | Adjustments: +20% (project match)

2. frontend-design (64.4) ← Penalized from 92
   Base: 92.0 | Adjustments: +20% (project match), -50% (already deployed)

3. python-backend (54.6) ← Penalized from 78
   Base: 78.0 | Adjustments: -30% (language mismatch)
```

**Presentation**:
```
Based on your React + TypeScript project, I recommend:

1. webapp-testing (100% confidence) ⭐ BEST MATCH
   Component testing with Jest and React Testing Library
   [+20% boost: React project match]

2. frontend-design (64% confidence) ℹ️ ALREADY DEPLOYED
   You already have this artifact deployed
   [+20% boost, -50% penalty: duplicate]

3. python-backend (55% confidence) ⚠️ LANGUAGE MISMATCH
   Python backend development (may not be relevant)
   [-30% penalty: JavaScript project]

Would you like to add webapp-testing?
```

---

### Example 2: Python FastAPI Project

**Input**:
```bash
# Project analysis
{
  "projectTypes": ["python", "fastapi"],
  "deployed": []
}

# Search results
[
  { "name": "openapi-expert", "confidence": 88 },
  { "name": "python-backend", "confidence": 82 },
  { "name": "react-components", "confidence": 75 }
]
```

**Boosting Applied**:
```javascript
// openapi-expert: FastAPI match
boost: +25%, penalty: 0
adjusted: 88 * 1.25 = 110 → 100

// python-backend: Python match
boost: +20%, penalty: 0
adjusted: 82 * 1.20 = 98.4

// react-components: Language mismatch
boost: 0, penalty: -30%
adjusted: 75 * 0.70 = 52.5
```

**Re-ranked Results**:
```
1. openapi-expert (100.0) ← Boosted from 88
2. python-backend (98.4) ← Boosted from 82
3. react-components (52.5) ← Penalized from 75
```

---

### Example 3: Avoid Duplicate Recommendations

**Input**:
```bash
# User asks: "What skills should I add?"
# Project has frontend-design already deployed
{
  "projectTypes": ["react"],
  "deployed": ["frontend-design", "canvas"]
}

# Search: "development tools"
[
  { "name": "frontend-design", "confidence": 95 },
  { "name": "webapp-testing", "confidence": 85 },
  { "name": "canvas", "confidence": 88 }
]
```

**Boosting Applied**:
```javascript
// frontend-design: High score BUT already deployed
boost: +20%, penalty: -50%
adjusted: 95 * 0.70 = 66.5

// webapp-testing: Not deployed
boost: +20%, penalty: 0
adjusted: 85 * 1.20 = 102 → 100

// canvas: Already deployed
boost: 0, penalty: -50%
adjusted: 88 * 0.50 = 44
```

**Re-ranked Results**:
```
1. webapp-testing (100.0) ← Only new recommendation
2. frontend-design (66.5) ← Suppressed (duplicate)
3. canvas (44.0) ← Suppressed (duplicate)
```

**Presentation**:
```
For your React project, I found 1 new artifact recommendation:

webapp-testing (100% confidence) ⭐ NEW
  Component testing with Jest and React Testing Library
  [+20% boost: React project match]

You already have these deployed:
- frontend-design (was 95% → 67% after duplicate penalty)
- canvas (was 88% → 44% after duplicate penalty)

Would you like to add webapp-testing?
```

---

## Best Practices

### When to Apply Context Boosting

**DO Apply**:
- User asks for recommendations ("what should I add?")
- Agent suggests artifacts during development
- Discovery workflow for project-specific searches
- Auto-enhancement scenarios

**DON'T Apply**:
- User explicitly searches for specific artifact name
- Browsing marketplace/catalog (neutral ranking desired)
- User is exploring capabilities outside current project
- Cross-project artifact management

### Transparency

**Always**:
- Show adjustment amounts in results
- Explain why boost/penalty applied
- Present base score alongside adjusted score
- Mark deployed artifacts clearly

**Example Transparency**:
```
webapp-testing (100% confidence)
  Base score: 85% | +20% boost (React match) | Final: 100%
```

### Handling Edge Cases

**Multiple Project Types**:
- Apply all applicable boosts (stack additively)
- Cap total boost at +100%
- Most specific boost wins (FastAPI > Python)

**No Project Type Detected**:
- Skip boosting, use base scores only
- Optionally apply conservative boosts based on file patterns

**All Results Penalized**:
- Still show top results even if all have penalties
- Warn user about mismatch
- Suggest alternative search or project analysis

---

## Performance Considerations

### Caching Strategy

**What to Cache**:
- Project analysis results (5 min TTL)
- File modification times (for cache key)
- Boost/penalty rule configurations (static)

**What NOT to Cache**:
- Search results (always fresh)
- Adjusted scores (recalculate on every search)

### Token Efficiency

**Before Context Boosting**:
- Search API call: ~1KB request, ~5KB response
- Total: ~6KB per search

**After Context Boosting**:
- Project analysis: ~2KB (cached)
- Search API call: ~1KB request, ~5KB response
- Score adjustment: <0.5KB (local calculation)
- Total: ~8.5KB per search (first run), ~6.5KB (cached)

**Savings vs Manual Analysis**:
- Manual: User describes project, agent guesses (10-20 messages)
- Automated: 1 analysis + boosted results (2-3 messages)
- **~80% reduction in back-and-forth**

---

## Testing

### Unit Tests

Test boost/penalty calculation logic:

```javascript
describe('calculateBoost', () => {
  it('boosts React artifact for React project', () => {
    const artifact = { name: 'react-testing', metadata: { tags: ['react'] } };
    const projectTypes = ['react', 'typescript'];
    expect(calculateBoost(artifact, projectTypes)).toBe(0.20);
  });

  it('boosts FastAPI artifact more than Python', () => {
    const artifact = { name: 'fastapi-tools', metadata: { tags: ['fastapi'] } };
    const projectTypes = ['python', 'fastapi'];
    // FastAPI boost (25%) > Python boost (20%)
    expect(calculateBoost(artifact, projectTypes)).toBeGreaterThanOrEqual(0.25);
  });
});

describe('calculatePenalty', () => {
  it('penalizes already deployed artifacts', () => {
    const artifact = { name: 'frontend-design' };
    const context = { deployed: ['frontend-design'] };
    expect(calculatePenalty(artifact, context)).toBe(-0.50);
  });

  it('penalizes language mismatch', () => {
    const artifact = { name: 'python-backend', metadata: { tags: ['python'] } };
    const context = { projectTypes: ['react', 'typescript'], deployed: [] };
    expect(calculatePenalty(artifact, context)).toBe(-0.30);
  });

  it('caps total penalty at -60%', () => {
    const artifact = {
      name: 'old-python-backend',
      metadata: { deprecated: true, tags: ['python'] },
    };
    const context = {
      projectTypes: ['react'],
      deployed: ['old-python-backend'],
    };
    // -50% (duplicate) + -30% (language) + -40% (deprecated) = -120% → capped at -60%
    expect(calculatePenalty(artifact, context)).toBe(-0.60);
  });
});
```

### Integration Tests

Test full workflow with real project analysis:

```javascript
describe('Context Boosting Integration', () => {
  it('ranks React artifacts higher for React project', async () => {
    const projectPath = '/test/react-project';
    const searchResults = [
      { name: 'python-backend', confidence: 90 },
      { name: 'react-testing', confidence: 70 },
    ];

    const context = await analyzeProject(projectPath);
    const ranked = rerankResults(searchResults, context);

    expect(ranked[0].name).toBe('react-testing');
    expect(ranked[0].adjustedScore).toBeGreaterThan(ranked[1].adjustedScore);
  });
});
```

---

## Reference

### Related Files

- `scripts/analyze-project.js` - Project type detection
- `workflows/discovery-workflow.md` - Artifact search and presentation
- `workflows/agent-self-enhancement.md` - Auto-suggestion during development

### API Documentation

- Match endpoint: `/api/v1/match` (PRD-001 Phase 6)
- Scoring service: `skillmeat.core.scoring.service`

### Configuration

Boost/penalty rules can be configured via:
- Skill metadata (`boost-rules.json`)
- User preferences (`.skillmeat/config.toml`)
- Environment variables (`SKILLMEAT_BOOST_MULTIPLIER`)

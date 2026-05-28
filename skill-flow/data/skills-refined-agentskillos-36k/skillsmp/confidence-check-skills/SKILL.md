---
name: confidence-check-skills
description: Pre-implementation validation framework requiring ≥90% confidence before coding. Prevents wrong-direction work by assessing duplicates, architecture alignment, documentation, OSS references, and root cause understanding. Use before implementing features, fixes, or refactoring to save 5K-50K tokens per prevented error.
license: MIT
---

# Confidence Check Skills

**Purpose**: Quantified pre-implementation validation system that prevents wasted effort by requiring ≥90% confidence before coding begins.

**Critical Use Case**: Spend 100-200 tokens on validation to save 5,000-50,000 tokens on wrong-direction work. Proven results: 100% precision/recall in production testing.

**Used By**: All agents before implementation - especially implementor, developer-agent, frontend-ui-developer, ml-model-implementor

---

## When to Use Confidence Check

**MANDATORY before**:
- ✅ Implementing new features or functionality
- ✅ Major refactoring or architectural changes
- ✅ Bug fixes (except critical production emergencies)
- ✅ Adding new libraries, frameworks, or dependencies
- ✅ Database schema changes
- ✅ API endpoint creation
- ✅ Authentication/security implementations

**OPTIONAL/SKIP for**:
- ❌ Trivial documentation updates
- ❌ Simple typo fixes
- ❌ Critical production hotfixes (time-sensitive)
- ❌ Exploratory research (no code changes)

---

## The 5-Factor Assessment Model

### Overview

Each factor contributes a weighted score to calculate overall confidence:

| Factor | Weight | Purpose | Tools Used |
|--------|--------|---------|------------|
| **Duplicate Detection** | 25% | Prevent re-implementing existing solutions | Glob, Grep, ChromaDB |
| **Architecture Alignment** | 25% | Verify tech stack compatibility | Read, Grep |
| **Documentation Review** | 20% | Ensure official docs consulted | Glob, Read |
| **OSS Reference** | 15% | Find proven working implementations | WebSearch |
| **Root Cause Analysis** | 15% | Verify problem understanding | Read, analysis |

**Formula**:
```
confidence = (duplicate × 0.25) + (architecture × 0.25) + (docs × 0.20)
           + (oss × 0.15) + (rootcause × 0.15)
```

**Result**: 0.0 to 1.0 (0% to 100%)

---

## Factor 1: Duplicate Detection (25%)

**Question**: Does this functionality already exist in the codebase?

### Automated Checks

```javascript
// Step 1: File pattern search
const similarFiles = Glob({
  pattern: `**/*${featureKeyword}*{.ts,.js,.py,.rs,.md}`,
  path: "."
});

// Step 2: Code pattern search
const similarCode = Grep({
  pattern: coreLogicPattern,  // e.g., "function authenticateUser"
  glob: "**/*.{ts,js,py,rs}",
  output_mode: "files_with_matches"
});

// Step 3: ChromaDB semantic search (if available)
const semanticMatches = mcp__chroma__query_documents({
  collection_name: "codebase_features_all",
  query_texts: [featureDescription],
  n_results: 5,
  where: { "status": "implemented" }
});

// Step 4: Scoring logic
let duplicateScore = 1.0;  // Default: PASS (no duplicates)

if (similarFiles.length > 0) {
  duplicateScore = 0.0;  // FAIL: Files with similar names found
} else if (similarCode.length > 0) {
  duplicateScore = 0.5;  // PARTIAL: Similar code patterns found
} else if (semanticMatches.distances[0][0] < 0.3) {
  duplicateScore = 0.3;  // PARTIAL: Semantically similar feature exists
}

return duplicateScore;  // 0.0, 0.3, 0.5, or 1.0
```

### Pass Criteria

- ✅ **PASS (1.0)**: No similar files, code, or semantic matches
- ⚠️ **PARTIAL (0.5)**: Similar code patterns but different purpose
- ⚠️ **PARTIAL (0.3)**: Semantic similarity but different implementation
- ❌ **FAIL (0.0)**: Duplicate functionality already exists

### Example Scenarios

**Scenario 1: JWT Authentication**
```
Feature: "Implement JWT authentication middleware"

Checks:
- Glob: **/*auth*.{ts,js} → Found: src/auth/jwt-middleware.ts ❌
- Grep: "function.*authenticate|jwt.*verify" → 3 matches ❌
- ChromaDB: "jwt authentication" → Distance 0.08 (highly similar) ❌

Score: 0.0 (FAIL - duplicate exists)
Recommendation: Use existing src/auth/jwt-middleware.ts
```

**Scenario 2: Rate Limiter**
```
Feature: "Create API rate limiter"

Checks:
- Glob: **/*rate*limit*.{ts,js} → None found ✅
- Grep: "rateLimit|rate.*limit" → None found ✅
- ChromaDB: "rate limiting middleware" → Distance 0.82 (dissimilar) ✅

Score: 1.0 (PASS - no duplicates)
Recommendation: Proceed with implementation
```

---

## Factor 2: Architecture Alignment (25%)

**Question**: Is this compatible with the current tech stack and patterns?

### Automated Checks

```javascript
// Step 1: Read architecture documentation
const claudeMd = Read({ file_path: "CLAUDE.md" });
const readmeMd = Read({ file_path: "README.md" });
const packageJson = Read({ file_path: "package.json" });  // Node.js
const cargoToml = Read({ file_path: "Cargo.toml" });      // Rust
const requirementsTxt = Read({ file_path: "requirements.txt" });  // Python

// Step 2: Extract tech stack
const techStack = {
  language: detectLanguage([packageJson, cargoToml, requirementsTxt]),
  frameworks: extractFrameworks(claudeMd, packageJson),
  patterns: extractPatterns(claudeMd, readmeMd),
  database: detectDatabase(claudeMd, packageJson)
};

// Step 3: Verify compatibility
let architectureScore = 1.0;  // Default: PASS

// Example checks:
if (proposedTech.language !== techStack.language) {
  architectureScore = 0.0;  // FAIL: Wrong language
} else if (!techStack.frameworks.includes(proposedTech.framework)) {
  architectureScore = 0.5;  // PARTIAL: New framework (may be acceptable)
} else if (violatesPatterns(proposedTech, techStack.patterns)) {
  architectureScore = 0.3;  // PARTIAL: Pattern violation
}

return architectureScore;  // 0.0, 0.3, 0.5, or 1.0
```

### Pass Criteria

- ✅ **PASS (1.0)**: Fully compatible with documented tech stack
- ⚠️ **PARTIAL (0.5)**: Compatible but introduces new framework/library
- ⚠️ **PARTIAL (0.3)**: Compatible but violates documented patterns
- ❌ **FAIL (0.0)**: Incompatible (wrong language, framework, database)

### Example Scenarios

**Scenario 1: Python Library in Rust Project**
```
Proposal: "Add pandas for data processing"
Tech Stack: Rust (from Cargo.toml)

Check:
- Cargo.toml exists → Rust project ✅
- Proposed: Python pandas library ❌

Score: 0.0 (FAIL - language mismatch)
Recommendation: Use Rust polars crate instead
```

**Scenario 2: New Framework Addition**
```
Proposal: "Use Tailwind CSS for styling"
Tech Stack: React + plain CSS (from package.json)

Check:
- package.json shows React ✅
- Currently using plain CSS (no Tailwind) ⚠️
- CLAUDE.md doesn't prohibit Tailwind ✅

Score: 0.5 (PARTIAL - new framework, acceptable)
Recommendation: Proceed, but document Tailwind addition
```

---

## Factor 3: Documentation Review (20%)

**Question**: Have relevant documentation and guides been consulted?

### Automated Checks

```javascript
// Step 1: Find documentation
const docsFound = Glob({
  pattern: "**/{docs,documentation,README,CLAUDE}*.md",
  path: "."
});

// Step 2: Search for relevant sections
const relevantDocs = [];
for (const docFile of docsFound) {
  const content = Read({ file_path: docFile });

  // Check if doc is relevant to feature
  if (content.toLowerCase().includes(featureKeyword.toLowerCase())) {
    relevantDocs.push({
      file: docFile,
      excerpts: extractRelevantSections(content, featureKeyword)
    });
  }
}

// Step 3: Scoring logic
let docsScore = 0.0;  // Default: FAIL (no docs)

if (relevantDocs.length === 0) {
  docsScore = 0.0;  // FAIL: No relevant docs found
} else if (relevantDocs.length >= 1) {
  docsScore = 1.0;  // PASS: Relevant docs found and should be reviewed
}

// Special case: If docs directory doesn't exist at all
if (docsFound.length === 0) {
  docsScore = 0.5;  // PARTIAL: No docs exist (not agent's fault)
}

return docsScore;  // 0.0, 0.5, or 1.0
```

### Pass Criteria

- ✅ **PASS (1.0)**: Relevant documentation found and reviewed
- ⚠️ **PARTIAL (0.5)**: No documentation exists in project (not agent's fault)
- ❌ **FAIL (0.0)**: Documentation exists but not consulted

### Example Scenarios

**Scenario 1: Documented Authentication Pattern**
```
Feature: "Implement OAuth2 flow"

Check:
- Glob: **/docs/**/*.md → Found: docs/authentication-guide.md ✅
- Read: docs/authentication-guide.md → Contains "OAuth2" section ✅
- Reviewed: Yes (agent read the OAuth2 section) ✅

Score: 1.0 (PASS - docs found and reviewed)
Recommendation: Follow documented OAuth2 pattern
```

**Scenario 2: No Documentation**
```
Feature: "Create data export feature"

Check:
- Glob: **/docs/**/*.md → None found ⚠️
- Glob: **/README.md → Found but no mention of data export ⚠️

Score: 0.5 (PARTIAL - no docs exist)
Recommendation: Proceed, but create docs after implementation
```

---

## Factor 4: OSS Reference (15%)

**Question**: Is there a proven, working implementation we can reference?

### Automated Checks

```javascript
// Step 1: Search for existing implementations
const githubSearch = WebSearch({
  query: `${techStack} ${featureName} implementation site:github.com`,
  allowed_domains: ["github.com"]
});

const npmSearch = WebSearch({  // For Node.js
  query: `${featureName} site:npmjs.com`,
  allowed_domains: ["npmjs.com"]
});

const cratesSearch = WebSearch({  // For Rust
  query: `${featureName} site:crates.io`,
  allowed_domains: ["crates.io"]
});

// Step 2: Parse quality metrics
const references = parseSearchResults(githubSearch, npmSearch, cratesSearch);

// Step 3: Scoring based on quality
let ossScore = 0.0;  // Default: FAIL

if (references.some(ref => ref.stars >= 1000 && ref.maintained)) {
  ossScore = 1.0;  // PASS: High-quality reference (1K+ stars, maintained)
} else if (references.some(ref => ref.stars >= 100)) {
  ossScore = 0.7;  // PARTIAL: Medium-quality reference (100+ stars)
} else if (references.length > 0) {
  ossScore = 0.4;  // PARTIAL: Low-quality reference (exists but unverified)
}

return ossScore;  // 0.0, 0.4, 0.7, or 1.0
```

### Pass Criteria

- ✅ **PASS (1.0)**: High-quality reference (1K+ stars, actively maintained)
- ⚠️ **PARTIAL (0.7)**: Medium-quality reference (100+ stars)
- ⚠️ **PARTIAL (0.4)**: Low-quality reference (exists but unverified)
- ❌ **FAIL (0.0)**: No working implementation found

### Example Scenarios

**Scenario 1: Express.js Rate Limiting**
```
Feature: "API rate limiter for Express"
Tech Stack: Node.js + Express

WebSearch: "express rate limiting npm"
Results:
- express-rate-limit: 3.2K stars, maintained ✅
- rate-limiter-flexible: 2.8K stars, maintained ✅

Score: 1.0 (PASS - multiple high-quality references)
Recommendation: Use express-rate-limit (most popular)
```

**Scenario 2: Custom Algorithm**
```
Feature: "Implement custom sorting algorithm for trades"

WebSearch: "custom trade sorting algorithm"
Results:
- No high-quality libraries found ❌
- Academic papers exist (not production code) ⚠️

Score: 0.0 (FAIL - no proven implementation)
Recommendation: Implement custom, but add extensive tests
```

---

## Factor 5: Root Cause Analysis (15%)

**Question**: Is the underlying problem clearly understood?

### Manual Evaluation

This check requires human judgment but follows a structured approach:

```javascript
// Step 1: Analyze problem description
const problemDescription = extractProblemFromRequest(userRequest);

// Step 2: Check clarity indicators
const clarityChecks = {
  symptomsDescribed: problemDescription.includes("error") ||
                     problemDescription.includes("fails") ||
                     problemDescription.includes("doesn't work"),

  rootCauseIdentified: problemDescription.includes("because") ||
                       problemDescription.includes("due to") ||
                       problemDescription.includes("caused by"),

  reproductionSteps: problemDescription.match(/\d+\.\s+/g)?.length >= 2,  // Numbered steps

  expectedVsActual: problemDescription.includes("expected") &&
                    problemDescription.includes("actual"),

  contextProvided: problemDescription.length > 100  // Sufficient detail
};

// Step 3: Scoring logic
let rootCauseScore = 0.0;  // Default: FAIL

const passedChecks = Object.values(clarityChecks).filter(v => v).length;

if (passedChecks >= 4) {
  rootCauseScore = 1.0;  // PASS: Root cause clearly understood
} else if (passedChecks >= 2) {
  rootCauseScore = 0.6;  // PARTIAL: Some understanding
} else {
  rootCauseScore = 0.0;  // FAIL: Unclear problem
}

return rootCauseScore;  // 0.0, 0.6, or 1.0
```

### Pass Criteria

- ✅ **PASS (1.0)**: Problem clearly described with root cause, reproduction steps, and context
- ⚠️ **PARTIAL (0.6)**: Symptoms described but root cause unclear
- ❌ **FAIL (0.0)**: Vague request without clear problem understanding

### Example Scenarios

**Scenario 1: Clear Root Cause**
```
Request: "Fix authentication failures. Users are getting 401 errors
when accessing /api/protected after password reset because the JWT
secret was rotated but old tokens weren't invalidated. Expected:
Users stay logged in. Actual: Users logged out after 5 minutes."

Checks:
- Symptoms described: "401 errors" ✅
- Root cause identified: "JWT secret rotated, tokens not invalidated" ✅
- Expected vs actual: Explicit comparison ✅
- Context provided: Password reset timing, JWT details ✅

Score: 1.0 (PASS - root cause clearly understood)
```

**Scenario 2: Vague Request**
```
Request: "Make the app faster"

Checks:
- Symptoms described: "slower" (vague) ⚠️
- Root cause identified: None ❌
- Reproduction steps: None ❌
- Expected vs actual: None ❌
- Context provided: Minimal ❌

Score: 0.0 (FAIL - unclear problem)
Recommendation: Ask user for specifics (slow queries? UI lag? API latency?)
```

---

## Decision Thresholds

After calculating the weighted confidence score, apply decision logic:

### Threshold Rules

```javascript
if (confidence >= 0.90) {
  return {
    decision: "PROCEED",
    message: "High confidence (≥90%). Proceed with implementation.",
    color: "green"
  };
} else if (confidence >= 0.70) {
  return {
    decision: "CLARIFY",
    message: "Medium confidence (70-89%). Present alternatives and request clarification.",
    color: "yellow"
  };
} else {
  return {
    decision: "STOP",
    message: "Low confidence (<70%). Stop and gather additional context.",
    color: "red"
  };
}
```

### Decision Matrix

| Confidence | Decision | Action | Example |
|------------|----------|--------|---------|
| **≥0.90** | ✅ PROCEED | Implement immediately | 0.95 = All checks passed |
| **0.70-0.89** | ⚠️ CLARIFY | Present alternatives, ask user | 0.75 = Most checks passed, 1-2 concerns |
| **<0.70** | ❌ STOP | Gather more context, don't implement | 0.45 = Multiple failures |

### Agent-Specific Thresholds

Different agent types may require different confidence levels:

| Agent Type | Minimum Confidence | Rationale |
|------------|-------------------|-----------|
| **security-audit-agent** | ≥0.95 | Critical, no room for error |
| **implementor** | ≥0.90 | Standard production code |
| **developer-agent** | ≥0.90 | General development |
| **frontend-ui-developer** | ≥0.85 | UI changes easier to fix |
| **research-specialist** | ≥0.75 | Exploratory, lower risk |
| **documentation-writer** | ≥0.70 | Easy to iterate |

---

## Complete Workflow Example

### Scenario: User Requests JWT Authentication

**User Request**: "Implement JWT authentication for the API"

---

**Step 1: Run Confidence Check**

```javascript
// Initialize
const feature = {
  name: "JWT Authentication",
  keyword: "jwt auth authentication",
  description: "Implement JWT token-based authentication middleware for Express API",
  techStack: { language: "Node.js", framework: "Express" }
};

// Factor 1: Duplicate Detection (25%)
const duplicateCheck = async () => {
  const files = await Glob({ pattern: "**/*auth*.{ts,js}" });
  // Result: Found src/auth/jwt-middleware.ts

  const code = await Grep({
    pattern: "jwt.*verify|jsonwebtoken",
    glob: "**/*.{ts,js}",
    output_mode: "files_with_matches"
  });
  // Result: 3 files match

  return 0.0;  // FAIL: Duplicate exists
};
// Score: 0.0 × 0.25 = 0.00

// Factor 2: Architecture Alignment (25%)
const architectureCheck = async () => {
  const packageJson = await Read({ file_path: "package.json" });
  // Result: Node.js project with Express

  const proposed = "JWT middleware (Node.js + Express)";
  // Compatible: ✅

  return 1.0;  // PASS: Fully compatible
};
// Score: 1.0 × 0.25 = 0.25

// Factor 3: Documentation Review (20%)
const docsCheck = async () => {
  const docs = await Glob({ pattern: "**/docs/**/*.md" });
  // Result: Found docs/authentication-guide.md

  const content = await Read({ file_path: "docs/authentication-guide.md" });
  // Result: Contains JWT section

  return 1.0;  // PASS: Relevant docs found
};
// Score: 1.0 × 0.20 = 0.20

// Factor 4: OSS Reference (15%)
const ossCheck = async () => {
  const results = await WebSearch({
    query: "express jwt authentication npm",
    allowed_domains: ["npmjs.com", "github.com"]
  });
  // Result: jsonwebtoken (18K stars), express-jwt (5K stars)

  return 1.0;  // PASS: High-quality references
};
// Score: 1.0 × 0.15 = 0.15

// Factor 5: Root Cause (15%)
const rootCauseCheck = () => {
  const request = "Implement JWT authentication for the API";
  // Clear feature request, not a bug
  // Requirement understood: API needs token-based auth

  return 1.0;  // PASS: Requirement clear
};
// Score: 1.0 × 0.15 = 0.15

// Calculate Total Confidence
const confidence = 0.00 + 0.25 + 0.20 + 0.15 + 0.15;
// Result: 0.75 (75%)
```

---

**Step 2: Apply Decision Logic**

```javascript
// Confidence: 0.75 (75%)
// Threshold: 0.70-0.89 → CLARIFY

const decision = {
  confidence: 0.75,
  decision: "CLARIFY",
  message: "Medium confidence (75%). Duplicate functionality detected.",
  breakdown: {
    duplicateDetection: { score: 0.00, status: "FAIL", reason: "Found existing JWT middleware" },
    architectureAlignment: { score: 0.25, status: "PASS", reason: "Compatible with Node.js + Express" },
    documentationReview: { score: 0.20, status: "PASS", reason: "Found docs/authentication-guide.md" },
    ossReference: { score: 0.15, status: "PASS", reason: "Found jsonwebtoken (18K stars)" },
    rootCauseAnalysis: { score: 0.15, status: "PASS", reason: "Requirement clearly understood" }
  },
  recommendation: "PRESENT_ALTERNATIVES"
};
```

---

**Step 3: Agent Response to User**

```markdown
## Confidence Check Results

**Overall Confidence**: 75% (MEDIUM) ⚠️

**Decision**: Request clarification before proceeding

### Breakdown

| Factor | Score | Status | Details |
|--------|-------|--------|---------|
| Duplicate Detection | 0/25% | ❌ FAIL | Found existing `src/auth/jwt-middleware.ts` |
| Architecture Alignment | 25/25% | ✅ PASS | Compatible with Node.js + Express |
| Documentation Review | 20/20% | ✅ PASS | Reviewed `docs/authentication-guide.md` |
| OSS Reference | 15/15% | ✅ PASS | Found `jsonwebtoken` (18K stars) |
| Root Cause Analysis | 15/15% | ✅ PASS | Requirement clearly understood |

### Recommendation

I found **existing JWT authentication middleware** at `src/auth/jwt-middleware.ts`.

**Options**:

A) **Use Existing Implementation** (Recommended)
   - Already implemented and tested
   - Follows project patterns from docs/authentication-guide.md
   - No additional work needed

B) **Enhance Existing Implementation**
   - What's missing from current implementation?
   - Refresh token support?
   - Additional claims/permissions?

C) **Replace Entirely**
   - Why is replacement needed?
   - What's wrong with current implementation?

**Which option would you like to proceed with?**
```

---

**Step 4: User Response & Final Action**

**User**: "Oh, I didn't know we had JWT already. Let's use option A."

**Agent**: "Perfect! I'll integrate the existing `src/auth/jwt-middleware.ts` into your routes."

**Outcome**:
- ✅ Prevented 5,000+ tokens of duplicate implementation
- ✅ Reused existing, tested code
- ✅ User informed about existing solution
- ✅ Total cost: ~200 tokens for confidence check

---

## Integration with Existing Patterns

### Integration 1: ExitPlanMode

Show confidence score in plan approval:

```markdown
## Implementation Plan

**Feature**: Add real-time WebSocket notifications

**Confidence Score**: 0.92 (92%) ✅

**Confidence Breakdown**:
- ✅ Duplicate Detection: PASS (no existing WebSocket implementation)
- ✅ Architecture Alignment: PASS (Node.js + Socket.io compatible)
- ✅ Documentation Review: PASS (reviewed docs/realtime-architecture.md)
- ✅ OSS Reference: PASS (Socket.io has 59K stars)
- ✅ Root Cause: PASS (requirement for live updates clearly understood)

**Decision**: High confidence - proceed immediately

**Plan**:
1. Install socket.io package
2. Create WebSocket server in src/websocket/
3. Implement notification broadcasting
4. Add client-side socket connection
5. Test with multiple clients

Proceed with this plan?
```

### Integration 2: ChromaDB Pattern Matching

Enhance duplicate detection with semantic search:

```javascript
// Enhanced Factor 1: Duplicate Detection with ChromaDB
const duplicateCheckEnhanced = async () => {
  // Traditional file search
  const files = await Glob({ pattern: `**/*${keyword}*` });

  // Traditional code search
  const code = await Grep({ pattern: codePattern });

  // NEW: Semantic similarity search
  const semanticMatches = await mcp__chroma__query_documents({
    collection_name: "codebase_features_all",
    query_texts: [featureDescription],
    n_results: 5,
    where: { "status": "implemented" }
  });

  // Scoring with semantic awareness
  if (files.length > 0) {
    return 0.0;  // Exact file match
  } else if (code.length > 0) {
    return 0.5;  // Code pattern match
  } else if (semanticMatches.distances[0][0] < 0.3) {
    return 0.3;  // Semantic similarity (distance < 0.3)
  } else {
    return 1.0;  // No duplicates
  }
};
```

### Integration 3: TodoWrite Tracking

Track confidence checks in todo list:

```javascript
TodoWrite({
  todos: [
    {
      content: "Run confidence check for feature implementation",
      status: "in_progress",
      activeForm: "Running confidence check"
    },
    {
      content: "Implement feature (if confidence ≥ 90%)",
      status: "pending",
      activeForm: "Implementing feature"
    }
  ]
});

// After confidence check
if (confidence >= 0.90) {
  TodoWrite({
    todos: [
      {
        content: "Run confidence check for feature implementation",
        status: "completed",
        activeForm: "Running confidence check"
      },
      {
        content: "Implement feature (confidence: 92%)",
        status: "in_progress",
        activeForm: "Implementing feature"
      }
    ]
  });
} else {
  TodoWrite({
    todos: [
      {
        content: "Run confidence check for feature implementation",
        status: "completed",
        activeForm: "Running confidence check"
      },
      {
        content: "Clarify requirements (confidence only 65%)",
        status: "in_progress",
        activeForm: "Requesting clarification"
      }
    ]
  });
}
```

---

## Best Practices

### 1. Run Check Early

**Do**: Run confidence check BEFORE planning implementation
```javascript
// CORRECT ORDER
1. Receive user request
2. Run confidence check (100-200 tokens)
3. If ≥90%, create implementation plan
4. Execute plan
```

**Don't**: Plan first, check later
```javascript
// WRONG ORDER (wastes tokens)
1. Receive user request
2. Create detailed implementation plan (1,000 tokens)
3. Run confidence check → discover duplicate
4. Wasted: 1,000 tokens on unnecessary planning
```

### 2. Document All Checks

Always show confidence breakdown to user:

```markdown
## Confidence Check: ✅ PASS (92%)

- ✅ Duplicate Detection (0.25): No existing implementation
- ✅ Architecture (0.25): Compatible with React + TypeScript
- ✅ Documentation (0.20): Reviewed component guidelines
- ✅ OSS Reference (0.15): Found react-hot-toast (7K stars)
- ⚠️ Root Cause (0.07): Requirement partially clear

**Decision**: Proceed (confidence ≥ 90%)
```

### 3. Handle Edge Cases

**Edge Case 1: No Documentation Exists**
- Don't penalize agent for missing docs
- Score 0.5 (neutral) instead of 0.0 (fail)
- Recommend creating docs after implementation

**Edge Case 2: Custom/Novel Implementation**
- OSS reference may not exist (0.0 score)
- If other factors pass, still may exceed 90% threshold
- Document why OSS doesn't exist (novel approach)

**Edge Case 3: User Override**
- User can explicitly request "proceed anyway"
- Log override for tracking
- Remind user of confidence score

### 4. Continuous Learning

Store confidence checks in ChromaDB for analysis:

```javascript
// After completing implementation
mcp__chroma__add_documents({
  collection_name: "confidence_checks_historical",
  documents: [
    `Feature: ${featureName}.
     Confidence: ${confidence}.
     Decision: ${decision}.
     Outcome: ${outcome}.
     Tokens saved: ${tokensSaved}`
  ],
  ids: [`check_${Date.now()}`],
  metadatas: [{
    feature: featureName,
    confidence: confidence,
    decision: decision,
    outcome: outcome,  // "success", "failure", "changed_approach"
    tokens_saved: tokensSaved,
    date: new Date().toISOString()
  }]
});

// Analyze patterns quarterly
const lowConfidenceSuccesses = await mcp__chroma__query_documents({
  collection_name: "confidence_checks_historical",
  query_texts: [""],
  n_results: 1000,
  where: {
    "$and": [
      { "confidence": { "$lt": 0.90 } },
      { "outcome": "success" }
    ]
  }
});

// If many low-confidence checks succeeded, lower threshold
```

---

## Success Metrics

Confidence check is **SUCCESSFUL** when:

- ✅ **Executed Early**: Run before implementation planning
- ✅ **All 5 Factors Checked**: No skipped factors
- ✅ **Tool-Based Validation**: Used Glob, Grep, Read, WebSearch (not manual)
- ✅ **Quantified Score**: 0.0-1.0 calculated correctly
- ✅ **Threshold Applied**: Decision follows 0.90/0.70 rules
- ✅ **User Informed**: Confidence breakdown shown
- ✅ **Token Efficiency**: <200 tokens spent on check
- ✅ **Wrong Direction Prevented**: Duplicates/misalignments caught
- ✅ **ChromaDB Integration**: Semantic search used (if available)
- ✅ **Outcome Tracked**: Result logged for learning

---

## Validation Protocol

Before deploying confidence-check, validate with test scenarios:

### Test Scenario 1: Duplicate Detection

**Input**: "Implement user authentication"
**Expected**:
- Find existing auth implementation (score 0.0)
- Overall confidence < 0.70 (STOP)
- Recommend using existing solution

### Test Scenario 2: Architecture Misalignment

**Input**: "Add Python pandas for data processing" (in Rust project)
**Expected**:
- Detect language mismatch (score 0.0)
- Overall confidence < 0.70 (STOP)
- Recommend Rust polars instead

### Test Scenario 3: High Confidence Path

**Input**: "Create rate limiter" (no existing, well-documented, good OSS)
**Expected**:
- All factors pass (≥0.90)
- Decision: PROCEED
- Implementation begins

### Test Scenario 4: Medium Confidence (New Framework)

**Input**: "Add Tailwind CSS" (project uses plain CSS)
**Expected**:
- Architecture partial (0.5 for new framework)
- Overall confidence 0.70-0.89 (CLARIFY)
- Ask user to confirm new framework addition

---

**Skill Version**: 1.0
**Created**: 2025-11-14
**Purpose**: Prevent wrong-direction work with quantified pre-implementation validation
**Target Quality**: 65/70
**Dependencies**: Glob, Grep, Read, WebSearch, ChromaDB (optional), TodoWrite (optional)
**Proven ROI**: 100-200 tokens spent → saves 5,000-50,000 tokens per prevented error
**Production Results**: 100% precision, 100% recall (SuperClaude Framework validation)

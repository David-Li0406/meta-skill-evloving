# Aggregation Patterns for Fanout Results

Synthesis algorithms for combining parallel analysis outputs.

## Philosophy

Aggregation is not averaging - it's synthesis. Multiple perspectives should:
1. Surface themes that appear across analyses
2. Highlight contradictions that need resolution
3. Weight contributions by confidence
4. Produce actionable, prioritized output

## Input Structure

Each fanout session returns:

```json
{
  "mode": "fanout",
  "analysis_type": "gap | pattern | friction | synergy | platform | meta",
  "status": "success | partial | blocked | failed",
  "summary": "50-200 word summary",
  "confidence": 1-10,
  "artifacts": [{
    "type": "analysis",
    "content": "structured markdown"
  }],
  "sources": {
    "files_read": [],
    "tools_used": []
  },
  "assumptions": [],
  "next_steps": [],
  "blockers": []
}
```

## Aggregation Patterns

### 1. Theme Extraction

Identify recurring themes across all analyses.

**Algorithm:**
```
1. Parse each artifact.content as markdown
2. Extract headers (## and ###) as theme candidates
3. Fuzzy match themes across analyses (Levenshtein < 3)
4. Count theme occurrences
5. Rank by: occurrence_count × avg_confidence
```

**Output:**
```markdown
## Cross-Analysis Themes

### Testing Gaps (appeared in 4/6 analyses, avg confidence: 8.2)
- gap-analysis: "missing unit tests for auth module"
- pattern-extraction: "test patterns inconsistent with arbor/koto"
- friction-analysis: "test setup friction causing skipped tests"
- meta-analysis: "testing culture gap vs mature projects"

### Documentation Debt (appeared in 3/6 analyses, avg confidence: 7.0)
- gap-analysis: "API documentation incomplete"
- friction-analysis: "cognitive load from undocumented patterns"
- platform-audit: "outline --unused not being used for dead code"
```

### 2. Contradiction Surfacing

Find where analyses disagree to highlight decision points.

**Algorithm:**
```
1. Extract recommendations from each analysis
2. Cluster similar recommendations
3. Identify clusters with conflicting directions
4. Surface as decision points requiring human input
```

**Output:**
```markdown
## Contradictions Requiring Resolution

### Monorepo Structure
- pattern-extraction: "current structure follows arbor patterns well"
- friction-analysis: "package boundaries causing import friction"
- **Decision needed:** Keep current structure or consolidate?

### Testing Strategy
- gap-analysis: "need more unit tests"
- platform-audit: "E2E via Playwright underutilized"
- **Decision needed:** Prioritize unit tests or E2E coverage?
```

### 3. Confidence-Weighted Synthesis

Weight contributions by stated confidence.

**Algorithm:**
```
for each finding:
  weighted_score = confidence × impact_heuristic

impact_heuristic:
  - "critical" in text → ×1.5
  - "blocker" in text → ×2.0
  - "nice to have" → ×0.5

sort findings by weighted_score descending
```

**Output:**
```markdown
## Prioritized Findings (confidence-weighted)

1. **Auth module lacks tests** (score: 16.0)
   - Source: gap-analysis (confidence: 9), friction-analysis (confidence: 8)
   - Impact: critical path, security implications

2. **layer --check-cycles not in CI** (score: 12.0)
   - Source: platform-audit (confidence: 8), pattern-extraction (confidence: 7)
   - Impact: architectural drift risk

3. **Inconsistent error handling** (score: 9.0)
   - Source: pattern-extraction (confidence: 6)
   - Impact: debugging friction
```

### 4. Source Triangulation

Validate findings by checking source overlap.

**Algorithm:**
```
for each finding:
  source_files = union of files_read across analyses mentioning finding
  if len(source_files) >= 3:
    triangulation = "strong"
  elif len(source_files) >= 2:
    triangulation = "moderate"
  else:
    triangulation = "single-source"
```

**Output:**
```markdown
## Finding Validation

### Strong Triangulation (3+ independent sources)
- Auth testing gap: seen in src/auth/*.ts, convex/auth.ts, tests/auth.test.ts
- Documentation debt: seen in README.md, CLAUDE.md, src/*/index.ts

### Moderate Triangulation (2 sources)
- Import friction: seen in package.json, tsconfig.json

### Single-Source (needs verification)
- Performance concerns: only seen in src/api/heavy.ts
```

## Aggregation Workflow

### Phase 1: Collection

```bash
# Collect all session outputs
RESULTS=()
for session_id in "${SESSION_IDS[@]}"; do
  OUTPUT_PATH="$HOME/.agents/prompts/${session_id}-response.json"
  if [ -f "$OUTPUT_PATH" ]; then
    RESULTS+=("$(cat $OUTPUT_PATH)")
  fi
done
```

### Phase 2: Validation

```bash
# Filter successful results
VALID_RESULTS=()
for result in "${RESULTS[@]}"; do
  status=$(echo "$result" | jq -r '.status')
  if [ "$status" = "success" ] || [ "$status" = "partial" ]; then
    VALID_RESULTS+=("$result")
  fi
done

# Warn if too few valid results
if [ ${#VALID_RESULTS[@]} -lt 3 ]; then
  echo "Warning: Only ${#VALID_RESULTS[@]} valid results. Consider re-running failed analyses."
fi
```

### Phase 3: Synthesis

```bash
# Combine into single JSON array
echo "${VALID_RESULTS[@]}" | jq -s '.' > /tmp/combined.json

# Run aggregation (could be copilot or local script)
cat << 'EOF' | copilot -p --model gemini-3-pro --output-format json
Given these parallel analysis results:
$(cat /tmp/combined.json)

Synthesize into a unified report with:
1. Cross-analysis themes (with occurrence counts)
2. Contradictions requiring resolution
3. Confidence-weighted priority ranking
4. Source triangulation assessment

Output JSON with aggregated findings.
EOF
```

### Phase 4: Output

Final aggregated output structure:

```json
{
  "mode": "fanout-aggregation",
  "input_count": 6,
  "valid_count": 5,
  "themes": [
    {
      "name": "Testing Gaps",
      "occurrences": 4,
      "avg_confidence": 8.2,
      "sources": ["gap", "pattern", "friction", "meta"]
    }
  ],
  "contradictions": [
    {
      "topic": "Monorepo Structure",
      "positions": [
        {"source": "pattern", "position": "keep current"},
        {"source": "friction", "position": "consolidate"}
      ],
      "decision_needed": true
    }
  ],
  "prioritized_findings": [
    {
      "finding": "Auth module lacks tests",
      "weighted_score": 16.0,
      "sources": ["gap", "friction"],
      "triangulation": "strong"
    }
  ],
  "metadata": {
    "aggregated_at": "2025-12-27T10:30:00Z",
    "failed_sessions": ["synergy"],
    "warnings": []
  }
}
```

## Handling Failures

### Partial Results

When some sessions fail:

```
Sessions: 6 spawned, 5 succeeded, 1 failed

Strategy:
1. Proceed with 5/6 (threshold: >50%)
2. Note gap in coverage (synergy analysis missing)
3. Suggest re-running failed session
```

### Low Confidence Results

When confidence is low across the board:

```
Average confidence: 4.2/10

Strategy:
1. Flag as "preliminary analysis"
2. Identify what information was missing
3. Suggest targeted follow-up with more context
```

### Conflicting High-Confidence Results

When multiple analyses strongly disagree:

```
gap-analysis: confidence 9, says "refactor now"
pattern-extraction: confidence 8, says "patterns are fine"

Strategy:
1. Surface as explicit contradiction
2. Don't average (that's not synthesis)
3. Present both positions with evidence
4. Flag for human decision
```

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Averaging confidence | Loses signal | Use weighted synthesis |
| Ignoring failures | Incomplete picture | Note gaps explicitly |
| Flattening contradictions | Loses nuance | Surface as decision points |
| Equal weighting | Low-confidence noise | Weight by confidence |
| Duplicate counting | Inflates themes | Dedupe by source file |

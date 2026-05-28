# agentic review

external LLM validation to catch shallow work. integrates consult-light and consult-deep.

## philosophy

> "you can't review your own blind spots"

claude does the work, external models validate. prevents:
- surface-level research (web scrapes instead of primary sources)
- missing integration with user's existing patterns
- philosophy without actionability
- declaring done on incomplete work

## two-tier validation

| tier | model | cost | use |
|------|-------|------|-----|
| consult-light | gemini-3-pro | ~$0.02 | quick depth check |
| consult-deep | gpt-5.2-codex xhigh | ~$0.10 | thorough review |

**always start with consult-light.** escalate if confidence < 7.

## consult-light patterns

### domain work review

```bash
copilot -p --model gemini-3-pro \
  "Domain skill review.

   Task: {description}
   Artifacts created:
   - {file_list}

   Content summary:
   {brief_summary}

   Validate depth:
   1. Primary sources: Were actual docs/code/talks read, or just summaries?
   2. Actionability: Are there decision trees (if X then Y), not just philosophy?
   3. Integration: Does it reference user's existing tools/patterns?
   4. Expert test: Would someone familiar with this domain find it informed?

   Output JSON:
   {
     \"pass\": bool,
     \"depth_score\": 1-10,
     \"issues\": [\"specific gap 1\", \"specific gap 2\"],
     \"missing_sources\": [\"what should have been read\"],
     \"confidence\": 1-10,
     \"escalate\": bool
   }"
```

### code work review

```bash
copilot -p --model gemini-3-pro \
  "Code work review.

   Task: {description}
   Files changed: {file_list}
   Tests: {test_summary}
   Verification: {verify_output}

   Validate:
   1. Test coverage: New behavior covered?
   2. Patterns: Matches codebase conventions?
   3. Edge cases: Handled or documented?
   4. Security: Obvious issues?

   Output JSON:
   {
     \"pass\": bool,
     \"coverage_score\": 1-10,
     \"issues\": [\"specific issue 1\"],
     \"confidence\": 1-10,
     \"escalate\": bool
   }"
```

## consult-deep patterns

### escalated domain review

```bash
codex exec --model "gpt-5.2-codex xhigh" --approval-mode xhigh \
  "Deep domain skill review.

   Task: {description}
   consult-light assessment:
   - Depth score: {score}
   - Issues: {issues}
   - Missing sources: {missing}

   Artifacts:
   {artifact_content_or_summary}

   Thorough review:
   1. Does this capture the ESSENCE of the domain, not just surface facts?
   2. Is this the kind of reference an expert would create?
   3. What specific sources should have been consulted?
   4. What decision trees are missing?
   5. How should this integrate with user's workflow?

   Output:
   - Status: approve | needs_work | needs_hil
   - Essence captured: 1-10
   - Critical gaps: [specific, actionable]
   - Sources to add: [specific links/repos]
   - Integration points: [user's tools to reference]
   - Recommendation: concrete next steps
   - Confidence: 1-10"
```

### escalated code review

```bash
codex exec --model "gpt-5.2-codex xhigh" --approval-mode xhigh \
  "Deep code review.

   Task: {description}
   consult-light assessment: {assessment}

   Files changed:
   {diff_or_file_list}

   Review passes:
   1. Correctness: Logic errors, edge cases
   2. Security: Injection, XSS, secrets, OWASP top 10
   3. Performance: N+1 queries, hot paths, memory
   4. Maintainability: Naming, structure, patterns
   5. Tests: Coverage quality, not just quantity

   Output:
   - Status: approve | needs_work | needs_hil
   - Merge readiness: 1-10
   - Blocking issues: [file:line - description]
   - Non-blocking: [suggestions]
   - Security findings: [if any]
   - Confidence: 1-10"
```

## routing logic

```
consult-light result:
  confidence >= 8 AND pass == true:
    → proceed to user confirmation

  confidence 5-7 OR issues.length > 0:
    → escalate to consult-deep

  confidence < 5:
    → iterate on work, don't proceed

consult-deep result:
  status == "approve" AND confidence >= 7:
    → proceed to user confirmation

  status == "needs_work":
    → iterate based on gaps identified

  status == "needs_hil" OR confidence < 5:
    → escalate to user with full context
```

## work type detection

| signal | work type | flywheel |
|--------|-----------|----------|
| creating skill, writing docs | domain | research → synthesize → validate → integrate |
| editing code files, running tests | code | scope → test → change → verify |
| exploring, reading, searching | research | explore → summarize → cross-reference |

## domain skill specific checks

| dimension | weak signal | strong signal |
|-----------|-------------|---------------|
| sources | scraped websites, summaries | read actual code, docs, talks via Ref MCP |
| structure | bullet lists, philosophy | decision trees, if/then rules |
| integration | generic patterns | references user's actual tools |
| actionability | "consider X" | "if X then do Y" |
| depth | anyone could write this | expert would recognize this |

## documentation grounding

**use Ref MCP liberally** - live docs prevent stale assumptions.

| check | question |
|-------|----------|
| ref_search_documentation used? | did we search for authoritative docs? |
| ref_read_url used? | did we read specific doc sections? |
| github repos read? | did we look at actual source code? |
| version awareness | are we citing current versions, not outdated? |

**required for domain work**:
- at least 2-3 ref_search_documentation calls for primary sources
- at least 1-2 ref_read_url calls to ground in actual docs
- github repo exploration for code-heavy domains

**consult-light should check**:
```
"Documentation grounding:
- Were ref_search_documentation calls made for authoritative sources?
- Were ref_read_url calls made to read actual docs?
- Are sources current (check versions, dates)?
- List sources that SHOULD have been consulted but weren't."
```

## anti-patterns

- **skipping consult-light**: always do the quick check
- **ignoring low confidence**: < 7 means escalate or iterate
- **vague prompts**: be specific about what to validate
- **no artifact context**: reviewer needs to see actual work
- **auto-approving**: the point is external validation, not rubber stamp

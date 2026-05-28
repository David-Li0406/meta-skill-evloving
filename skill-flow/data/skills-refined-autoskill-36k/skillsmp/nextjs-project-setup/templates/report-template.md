# [Agent Name] Report

**Agent**: [Agent name - research-vercel, research-shadcn, research-supabase, research-design, design-ideator, qa-validator, doc-auditor]
**Generated**: [ISO 8601 timestamp]
**Project**: [Project name from context]
**Token Count**: [Actual tokens] / 2500 (Target: ≤2500)

---

## Executive Summary

[2-3 sentences maximum: Key finding, main recommendation, critical action needed]

**Status**: ✅ Complete | ⚠️ Issues Found | ❌ Critical Failures

**Key Metrics** (if applicable):
- [Metric 1]: [Value]
- [Metric 2]: [Value]
- [Metric 3]: [Value]

---

## Findings

### Primary Findings

**Finding 1**: [Title]

**Evidence**: [file:line reference OR MCP query result OR documented source]

**Impact**: High | Medium | Low

**Description**:
[1-2 sentences explaining the finding]

**Recommendation**:
[Actionable next step]

---

**Finding 2**: [Title]

[Repeat structure]

---

**Finding 3**: [Title]

[Repeat structure]

---

### Secondary Findings

**Finding 4**: [Title]
[Brief description with evidence]

**Finding 5**: [Title]
[Brief description with evidence]

---

## Recommendations

### High Priority (Action Required)

1. **[Recommendation Title]**
   - **Why**: [Rationale]
   - **How**: [Specific steps]
   - **Impact**: [Expected outcome]

2. **[Recommendation Title]**
   [Same structure]

---

### Medium Priority (Should Address)

1. **[Recommendation Title]**
   [Brief description]

2. **[Recommendation Title]**
   [Brief description]

---

### Low Priority (Nice to Have)

1. **[Recommendation Title]**
   [Brief description]

---

## Evidence

### MCP Query Results

**Query 1**: [Tool name and query]
```
[Query result excerpt - relevant portions only]
```
**Source**: [Tool name]

---

**Query 2**: [Tool name and query]
```
[Query result excerpt]
```
**Source**: [Tool name]

---

### File References

- [file1.tsx:42-45] - [Brief description of what's there]
- [file2.ts:123] - [Brief description]
- [file3.md:Section] - [Brief description]

---

### External Resources

- [Resource title] - [URL] - [Why relevant]
- [Resource title] - [URL] - [Why relevant]

---

## CoD^Σ Reasoning Trace

```
[Show workflow using CoD^Σ operators]

Example:
Project_Requirements → Intelligence_Query[Tool] ≫ Targeted_Read[Files]
  ∥
Parallel_Analysis[A ⊕ B ⊕ C] → Findings_Synthesis
  ↓
Evidence_Validation ∘ Recommendation_Generation → Final_Report
```

---

## Success Criteria

- [x] Criterion 1 met
- [x] Criterion 2 met
- [ ] Criterion 3 not met (reason: [explain])
- [x] Criterion 4 met

**Overall**: [X / Y criteria met] ([percentage]%)

---

## Appendix (Optional - Only if needed, keep minimal)

### Detailed Data

[Only include if referenced in findings and keeps report ≤2500 tokens]

---

### Glossary

**[Term 1]**: Brief definition
**[Term 2]**: Brief definition

---

## Next Steps

1. [Immediate action]
2. [Follow-up action]
3. [Long-term action]

---

**Report Prepared By**: [Agent name]
**Review Status**: Draft | Final
**Approval Required**: Yes | No

---

## Template Notes (Remove in actual report)

### Token Budget Allocation

**Target**: ≤2500 tokens total

**Recommended Distribution**:
- Executive Summary: ~200 tokens (8%)
- Findings: ~1500 tokens (60%)
- Recommendations: ~500 tokens (20%)
- Evidence: ~300 tokens (12%)

### Writing Guidelines

**Be Concise**:
- Use bullet points, not paragraphs
- Lead with key information
- Remove filler words ("very", "actually", "basically")
- Use tables for comparison data

**Be Specific**:
- Cite file:line for code references
- Include MCP query tool names
- Quantify when possible (e.g., "3 occurrences" not "several")
- Use concrete examples

**Be Actionable**:
- Every finding needs a recommendation
- Recommendations must be specific, not vague
- Prioritize (High/Medium/Low)
- Include expected outcomes

### Evidence Requirements (Constitution Article II)

**All claims MUST have**:
- File:line references for code findings
- MCP query results for external data
- Tool output for validation results
- Links to authoritative sources

**Invalid Evidence**:
- "I think..."
- "Probably..."
- "Should be..."
- Assumptions without validation

### Common Anti-Patterns

❌ **Too Verbose**:
```
The system architecture utilizes a modern approach
leveraging cutting-edge technologies to deliver...
```

✅ **Concise**:
```
Architecture: Next.js 15, Supabase, Tailwind CSS
```

---

❌ **Vague Recommendations**:
```
Consider improving performance
```

✅ **Specific Recommendations**:
```
Recommendation: Implement next/image for hero.png
Why: Current <img> tag causes CLS of 0.25
How: Replace line 42 in app/page.tsx
Impact: Reduces CLS to <0.1, improves Core Web Vitals
```

---

❌ **Unsupported Claims**:
```
The component re-renders unnecessarily
```

✅ **Evidence-Backed Claims**:
```
Component re-renders on every keystroke (ComponentA.tsx:45)
Cause: Missing useCallback on handleChange (ComponentA.tsx:52)
Evidence: React DevTools Profiler shows 120 renders/minute
```

---

### Agent-Specific Variations

**Research Agents** (research-vercel, research-shadcn, research-supabase, research-design):
- Focus on discoveries and patterns
- Include component/template catalogs
- Provide installation priorities
- Reference external documentation

**Execution Agents** (design-ideator, qa-validator, doc-auditor):
- Focus on validation and quality gates
- Include pass/fail criteria
- Provide scoring matrices
- List specific issues with locations

---

### Quality Checklist

Before submitting report, verify:

- [ ] Token count ≤2500
- [ ] Executive summary ≤3 sentences
- [ ] All findings have evidence (file:line or MCP source)
- [ ] All recommendations actionable and prioritized
- [ ] CoD^Σ trace shows complete workflow
- [ ] Success criteria evaluated
- [ ] Next steps clearly defined
- [ ] No unsupported claims
- [ ] No filler words or redundancy
- [ ] Consistent formatting throughout

---

### Example Reports

**Good Report Structure**:
```markdown
# Research-Shadcn Report
**Generated**: 2025-10-29T14:30:00Z
**Token Count**: 2,450 / 2,500

## Executive Summary
Shadcn UI provides 47 components across 5 categories. Recommended 15 core components for Phase 1 installation. All components WCAG 2.1 AA compliant.

## Findings
**Finding 1**: Button component offers 6 variants
Evidence: mcp__shadcn__view_items_in_registries result for @ui/button
Impact: High - Core UI element needed immediately
Recommendation: Install in Phase 1 (Day 1)

[Continue with structured findings...]

## Recommendations
### High Priority
1. **Install Core UI (Day 1)**
   - Why: Needed for all pages
   - How: npx shadcn@latest add button card input label
   - Impact: Enables basic UI development

[Continue with prioritized recommendations...]

## Evidence
**MCP Query**: mcp__shadcn__search_items_in_registries
```
Results: 47 components found
Categories: Layout (12), Form (15), Navigation (8)...
```

[Continue with all evidence sources...]
```

---

### Token Optimization Tips

1. **Use Tables**: Compress comparison data

   ❌ Verbose (100 tokens):
   ```
   Option 1 scores 9 for UX, 8 for conversion, and 10 for accessibility.
   Option 2 scores 8 for UX, 9 for conversion, and 8 for accessibility.
   ```

   ✅ Concise (30 tokens):
   ```
   | Option | UX | Conv | A11y |
   |--------|-----|------|------|
   | 1      | 9   | 8    | 10   |
   | 2      | 8   | 9    | 8    |
   ```

2. **Use Lists**: Break down complex info

   ❌ Paragraph (80 tokens):
   ```
   The system requires Node.js version 18 or higher, npm version 9 or higher,
   and a Supabase account with a configured project.
   ```

   ✅ List (40 tokens):
   ```
   Requirements:
   - Node.js ≥18
   - npm ≥9
   - Supabase account
   ```

3. **Use Abbreviations**: Common terms

   - Authentication → Auth
   - Database → DB
   - Accessibility → A11y
   - Internationalization → i18n
   - Row Level Security → RLS
   - Server-Side Rendering → SSR

4. **Remove Redundancy**:

   ❌ "In order to achieve this goal, we need to..."
   ✅ "To achieve this, we need..."

   ❌ "It is important to note that..."
   ✅ "Note:"

---

### Report Filename Convention

**Pattern**: `[agent-name]-report-[timestamp].md`

**Examples**:
- `research-vercel-report-20251029-1430.md`
- `design-ideator-report-20251029-1445.md`
- `qa-validator-report-20251029-1502.md`

**ISO 8601 Timestamp Format**: `YYYYMMDD-HHMM`

---

**End of Template**

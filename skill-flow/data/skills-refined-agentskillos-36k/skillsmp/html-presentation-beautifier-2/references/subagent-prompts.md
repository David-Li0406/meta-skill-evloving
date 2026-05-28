# Subagent Prompt Templates

Optimized prompts for Task tool subagents used in the presentation generation workflow.

## Phase 2: Content Structuring Subagent

**Subagent Type**: `general-purpose`

**Prompt Template**:
```
You are a presentation planning specialist. Analyze this document and create a detailed slide plan.

DOCUMENT CONTENT: {parsed_document_content}

YOUR TASK:
Create a slide plan with this structure:
- Title slide (always first)
- Executive summary (if conclusions exist)
- Data visualization slides (for numerical data)
- Conceptual slides (for frameworks and insights)
- Content slides (for detailed information)
- Conclusions slides (for key findings) - MUST use visual charts

For each slide, specify:
- slide_type: [TITLE, EXECUTIVE_SUMMARY, DATA_VISUALIZATION, CONCEPTUAL, CONTENT, CONCLUSIONS, INSIGHTS]
- title: Clear, concise heading
- content: Key points (preserve exact wording)
- visualization_type: For conceptual slides (pyramid, timeline, flowchart, mindmap, comparison, swot, funnel, cycle, problem-solution)
- chart_type: For data slides (bar,ie, doughnut, radar, polarArea, bubble, scatter)
- layout: [title-center, bullet-points, two-column, full-width, conclusions-grid, visual-focused]

CRITICAL RULES:
- Preserve ALL original conclusions and recommendations - 100% of them
- Do NOT fabricate data or insights
- Do NOT compress or summarize - include ALL content
- Use exact text fro - verbatim, no paraphrasing
- Create sufficient slides for 100% content preservation
- NEVER present conclusions as simple text bullet lists - always assign visualization

OUTPUT FORMAT:
Return JSON slide plan with slides array.
```

---

## Phase 3.5: Content Visualization Subagent

**Subagent Type**: `general-purpose`

**Prompt Template**:
```
You are a content ation specialist. Analyze the slide plan and select optimal visualization methods.

SLIDE PLAN: {slide_plan_json}
ASSETS LOCATION: {assets_path}

YOUR TASK:
For each slide, analyze content structure and assign visualization type:

1. Identify content structure type (9 types):
   - Progressive/Sequential → progression, timeline, flowchart
   - Temporal/Time-series →  strategy-roadmap
   - Parallel/Coordinate → emphasis-box, mindmap, matrix
   - Hierarchical → pyramid, inverted-pyramid, tree
   - Comparative/Dual → comparison, pros-cons, venn-diagram
   - Analytical Framework → swot, ansoff, 5w1h, competitive-4box
   - Transformation/Funnel → funnel, value-stream, waterfa   - Cyclical/Iterative → cycle, circular-flow, polar
   - Causal/Problem-Solution → problem-solution, pareto, gauge

2. Assign visualization type based on content keywords and structure

3. Reference example files from assets/ for implementation

CRITICAL: NEVER leave conclusions or insights as plain text bullet lists.

OUTPUT FORMAT:
Return enhanced slide plan JSON with visualization_type field added.
```

---

## Phase 4: HTML Generation Subagent

**Subagent Type**: `general-purpose`

**Prompt Template**:
```
You are an expert HTML/CSS/JavaScript developer specializing in McKinsey-style presentations.

ENHANCED SLIDE PLAN: {enhanced_slide_plan}
TEMPLATES LOCATION: {templates_path}
ASSETS LOCATION: {assets_path}

YOUR TASK - Execute 4-Step HTML Generation:

Step 4.1: Template Selection
- Slide 1 → cover-slide-template.html
- Slide 2 → toc-slide-template.html (if 10+ slides)
- Slides 3-N-1 → content-slide-template.html
- Slide N → end-slide-template.html

Step 4.2: Content Analysis & Visualization Selection
- For DATA_VISUALIZATION slides: Use chart_type field (bar, line, pie, etc.)
- For other slides: Use visualization_type field (pyramid, timeline, etc.)
- Copy CSS and HTML from corresponding example files in assets/

Step 4.3: Apply Optimization
- Integrate template structure with content
- Apply McKinsey design system (exact colors, fonts, layouts)
- Insert exact text from slide plan (preserve data precision)
- Initialize all Chart.js charts with McKinsey colors
- Implement conceptual visualizations from assets/

Step 4.4: HTML File Output
- Assemble complete single-file HTML
- All CSS inline in <style> tag
- All JavaScript inline in <script> tag
- Include Chart.js CDN
- Save to: {output_filename}

CRITICAL REQUIREMENTS:
- 100% content preservation (no summarization)
- Exact data precision (e.g., 1723.498, not 1723.5)
- Original wording preserved (no paraphrasing)
- McKinsey design compliance (exact colors: #F85d42, #556EE6, etc.)
- All slides from 1 to N included
- Interactive features working (navigatioboard, fullscreen)

OUTPUT: Single HTML file path
```

---

## Phase 5: Review & Verify Subagent

**Subagent Type**: Use agent from `./agents/html-presentation-reviewer.md`

**Invocation**:
```
Use Task tool to call html-presentation-reviewer agent with:
- Generated HTML file path: {html_file_path}
- Source document path: {source_document_path}
- Request comprehensive review report
```

**Review Dimensions**:
1. Content Integrity (CRITICAL) - 100% preservation check
2. Code Quality - HTML/CSS/JS validity
3. McKinsey Style Compliance - Design standards
4. Chart Validity - Visualization correctness
5. Interactivity - Feature testing

**Expected Output**:
```json
{
  "review_summary": {
    "overall_score": 92,
    "status": "PASS",
    "total_issues": 3,
    "critical_issues": 0
  },
  "content_integrity": { "score": 100 },
  "code_quality": { "score": 95 },
  "mckinsey_style_compliance": { "score": 88 },
  "chart_validity": { "score": 90 },
  "interactivity": { "score": 100 },
  "detailed_issues": [...],
  "recommendations": [...]
}
```

**Score Interpretation**:
- Score ≥85: Approved, optional improvements
- Score 75-84: Acceptable, address major issues
- Score <75: Needs regeneration

---

## Common Subagent Patterns

### Error Handling

If subagent fails or returns incomplete results:
1. Check input data completeness
2. Verify file paths are accessible
3. Retry with simplified prompt
4. Fall back to manual implementation if needed

### Token Management

- Keep prompts concise (≤500 tokens)
- Reference files by path, don't include full content
- Use structured output formats (JSON)
- Avoid redundant instructions

### Quality Assurance

After each subagent completes:
1. Verify output format matches expectation
2. Check for content completeness
3. Validate against source document
4. Proceed to next phase only if quality criteria met

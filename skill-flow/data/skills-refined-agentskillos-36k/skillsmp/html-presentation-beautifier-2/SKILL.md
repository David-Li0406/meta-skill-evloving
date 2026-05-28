---
name: html-presentation-beautifier
description: Transform documents, reports, and data into professional McKinsey-style HTML presentations with intelligent chart selection and interactive navigation. Use when: (1) Creating presentations from documents/reports, (2) Converting markdown/text to slides, (3) Generating HTML slides, (4) Applying McKinsey/BCG design, (5) Data visualization in presentations. Keywords: presentation, slides, HTML, McKinsey style, charts, visualization, 幻灯片, 演示文稿
---

# HTML Presentation Beautifier

Transform documents and data into professional McKinsey-style HTML presentations with AI-powered content structuring, intelligent visualization, and automatic quality review.

**Core Principle**: Preserve 100% of original content while applying professional McKinsey-style design.

## Presentation Design Philosophy

Before creating any presentation, consider:

- **Audience**: Who will see this? (determines complexity and formality)
- **Core Message**: What's the single most important takeaway?
- **Story Arc**: How do slides build towards the conclusion?
- **Visual Hierarchy**: Which data and insights deserve emphasis?

**Key Principle**: Better to have 20 clear slides than 10 cluttered ones. Content preservation is non-negotiable.

## When to Use This Skill

Trigger scenarios:
- "Create a presentation from this document/report"
- "Transform this analysis into slides"
- "Generate McKinsey-style presentation"
- "Visualize this data professionally"
- "Make HTML slides from this content"

## Process Overview

6-phase AI-powered workflow using subagents:

| Phase | Action | Duration | Output |
|-------|--------|----------|--------|
| 1 | Parse Document | ~1 min | Structured content map |
| 2 | Plan Slides | ~2 min | Slide plan with visualizations |
| 3 | Apply Design | ~1 min | McKinsey-styled structure |
| 3.5 | Content Visualization | ~2 min | Enhanced with charts/graphics |
| 4 | Generate HTML | ~3 min | Single-file HTML presentation |
| 5 | Review & Verify | ~2 min | Quality report with scores |

**Total**: ~10-12 minutes for typical presentation

## Phase 1: Document Parsing

**Goal**: Extract structure, data, and conclusions without modification.

**Steps**:
1. Read source document completely
2. Identify document type (report, analysis, research)
3. Extract structural elements:
   - Headings and subheadings
   - Bullet points and lists
   - Data tables and numerical data
   - Key conclusions and recommendations
4. Map content hierarchy: main topics → subtopics → details
5. Identify quantitative data suitable for charts

**Exit Criteria**: Document fully parsed with content structure mapped.

---

## Phase 2: Content Structuring (Using Subagent)

**Goal**: Transform parsed content into slide-friendly structure.

**Approach**: Use `Task` tool with `general-purpose` subagent.

**MANDATORY - READ ENTIRE FILE**: Before invoking subagent, read [`subagent-prompts.md`](references/subagent-prompts.md) for the Phase 2 prompt template.

**Subagent Task**:
- Input: Parsed document content
- Output: JSON slide plan with slide types, titles, content, visualization assignments
- Critical: Preserve 100% of content, assign visualizations to all insights/conclusions

**Slide Types**:
- `TITLE`: Cover slide
- `TOC`: Table of contents (if 10+ slides)
- `DATA_VISUALIZATION`: Slides with numerical data
- `CONCEPTUAL`: Framework slides (SWOT, timeline, etc.)
- `CONTENT`: General content slides
- `CONCLUSIONS`: Key findings with visualizations
- `INSIGHTS`: Recommendations with visualizations
- `END`: Thank you slide

**Exit Criteria**: Structured slide plan with all slides defined, zero content loss.

## Phase 3: Design & Layout

**Goal**: Apply McKinsey-style design system.

**MANDATORY - READ ENTIRE FILE**: Read [`mckinsey-design-system.md`](references/mckinsey-design-system.md) for complete design specifications.

**Do NOT load** other reference files for this phase.

**Key Actions**:
1. Select appropriate layout for each slide type
2. Apply McKinsey color palette (#F85d42, #556EE6, #34c38f, etc.)
3. Set typography hierarchy (titles 48-64px, subtitles 28-36px, body 16-20px)
4. Optimize spacing (40-60px padding, 20-30px element spacing)
5. Ensure responsive design (1200px, 768px, mobile breakpoints)

**Exit Criteria**: All slides designed with consistent McKinsey-style branding.

---

## Phase 3.5: Content Visualization Beautification (Using Subagent)

**Goal**: Beautify content with appropriate charts and graphics, avoiding pure text lists.

**Approach**: Use `Task` tool with `general-purpose` subagent.

**MANDATORY - READ ENTIRE FILE**: Read [`chart-selection-guide.md`](references/chart-selection-guide.md) for complete visualization decision trees.

**Do NOT load** other reference files for this phase.

**Subagent Task**:
- Input: Structured slide plan from Phase 2
- Output: Enhanced slide plan with specific visualization types assigned
- Process: Analyze content structure → Match to visualization type → Reference example files

**9 Content Structure Types**:
1. **Progressive** (递进型) → progression, timeline, flowchart
2. **Temporal** (时间序列型) → timeline, strategy-roadmap
3. **Parallel** (并列型) → emphasis-box, mindmap, matrix
4. **Hierarchical** (层级型) → pyramid, inverted-pyramid
5. **Comparative** (对比型) → comparison, pros-cons, venn-diagram
6. **Framework** (分析框架型) → swot, ansoff, 5w1h, competitive-4box
7. **Transformation** (转化流程型) → funnel, value-stream
8. **Cyclical** (循环型) → cycle, circular-flow
9. **Causal** (因果型) → problem-solution, pareto, gauge

**Example Files Location**: `assets/*.html` (flowchart-example.html, pyramid-chart-example.html, etc.)

**Exit Criteria**: All content slides enhanced with appropriate visualizations, no plain text bullet lists for insights.

---

## Phase 4: HTML Generation (Using Subagent)

**Goal**: Generate single-file, self-contained HTML presentation.

**Approach**: Use `Task` tool with `general-purpose` subagent executing 4 sub-steps.

**MANDATORY - READ ENTIRE FILE**: Read [`template-guide.md`](references/template-guide.md) for complete template usage instructions.

**MANDATORY - READ ENTIRE FILE**: Read [`subagent-prompts.md`](references/subagent-prompts.md) for the Phase 4 prompt template.

**Do NOT load** other reference files for this phase.

**4-Step Process**:

### Step 4.1: Template Selection
- Slide #1 → `templates/cover-slide-template.html`
- Slide #2 → `templates/toc-slide-template.html` (if 10+ slides)
- Slides #3-#N-1 → `templates/content-slide-template.html`
- Slide #N → `templates/end-slide-template.html`

### Step 4.2: Content Analysis & Chart Selection
- For DATA_VISUALIZATION slides: Use `chart_type` field (bar, line, pie, doughnut, radar, polarArea, bubble, scatter)
- For other slides: Use `visualization_type` field (pyramid, timeline, flowchart, mindmap, etc.)
- Copy CSS and HTML from corresponding `assets/*.html` example files

### Step 4.3: Apply Optimization
- Integrate template structure with content
- Apply McKinsey design system (exact colors, fonts, layouts)
- Insert exact text from slide plan (preserve data precision: 1723.498, not 1723.5)
- Initialize Chart.js charts with McKinsey colors
- Implement conceptual visualizations from assets/

### Step 4.4: HTML File Output
- Assemble complete single-file HTML
- All CSS inline in `<style>` tag
- All JavaScript inline in `<script>` tag
- Include Chart.js CDN: `https://cdn.jsdelivr.net/npm/chart.js`
- Save to: `{original_filename}_beautified.html`

**Exit Criteria**: Complete HTML presentation file generated, ready to open in browser.

---

## Phase 5: Review & Verify (Using Subagent)

**Goal**: Automatically review generated HTML for quality, integrity, and compliance.

**Approach**: Use `Task` tool with `html-presentation-reviewer` agent from `./agents/html-presentation-reviewer.md`.

**Invocation**:
```
Use Task tool to call html-presentation-reviewer agent with:
- Generated HTML file path
- Source document path
- Request comprehensive review report
```

**Review Dimensions**:
1. **Content Integrity** (CRITICAL) - 100% preservation verification
2. **Code Quality** - HTML/CSS/JS validity
3. **McKinsey Style Compliance** - Design standards check
4. **Chart Validity** - Visualization correctness
5. **Interactivity** - Feature testing

**Score Interpretation**:
- **Score ≥85**: Approved, optional improvements
- **Score 75-84**: Acceptable, address major issues
- **Score <75**: Needs regeneration

**Exit Criteria**: HTML presentation reviewed and approved with detailed report.

---

## Interactive Features

Generated presentations include:

- **Navigation**: Previous/Next buttons, slide counter, arrow keys (←/→), Space (next)
- **Fullscreen**: Toggle button, Escape to exit
- **Keyboard Shortcuts**: Home (first slide), End (last slide)
- **Responsive Design**: Desktop, tablet, mobile layouts
- **Chart Interactivity**: Hover tooltips, legend toggling

---

## NEVER Do These

**Content Integrity**:
- NEVER modify original content or conclusions - preserve 100%
- NEVER delete, skip, or omit any content
- NEVER summarize or compress - show complete detail
- NEVER truncate lists - if source has 15 items, show all 15
- NEVER paraphrase - use exact wording from source
- NEVER add fabricated data - only use source data

**Design Standards**:
- NEVER deviate from McKinsey color scheme (#F85d42, #556EE6, #34c38f, #50a5f1, #f1b44c, #74788d)
- NEVER use inconsistent typography - maintain hierarchy
- NEVER present conclusions/insights as plain text bullet lists - always visualize
- NEVER use generic AI aesthetics (purple gradients, Inter font, default border-radius)

**Quality**:
- NEVER sacrifice content for aesthetics - better 20 dense slides than 10 incomplete ones
- NEVER skip Phase 5 review - quality verification is mandatory

---

## Quick Start Example

**User Request**: "Create a McKinsey-style presentation from this report"

**Workflow**:
1. **Parse** (Phase 1): Read report, extract structure
2. **Plan** (Phase 2): Invoke subagent → Get slide plan
3. **Design** (Phase 3): Load design system → Apply McKinsey style
4. **Visualize** (Phase 3.5): Invoke subagent → Enhance with charts/graphics
5. **Generate** (Phase 4): Invoke subagent → Create HTML file
6. **Review** (Phase 5): Invoke reviewer agent → Get quality report

**Output**: `report_beautified.html` with professional visualizations, quality score, and recommendations.

---

## Resources

All detailed guides are in `references/`:

- **Design System**: `mckinsey-design-system.md` - Colors, typography, layouts
- **Templates**: `template-guide.md` - 4 template usage instructions
- **Chart Selection**: `chart-selection-guide.md` - Decision trees for visualizations
- **Subagent Prompts**: `subagent-prompts.md` - Optimized prompts for all phases

Visualization examples in `assets/`:
- See `assets/CHART_EXAMPLES_INDEX.md` for complete list
- See `assets/INSIGHT_VISUALIZATION_GUIDE.md` for detailed visualization guide
- See `assets/TEMPLATE_USAGE_GUIDE.md` for template usage examples

---

## Content Integrity Verification (MANDATORY)

Before finalizing presentation, verify 100% content preservation:

**Checklist**:
- [ ] Section counts match (source vs presentation)
- [ ] Bullet point counts match
- [ ] Data point counts match
- [ ] Conclusion counts match
- [ ] Exact wording preserved (no paraphrasing)

**IF ANY COUNT DOES NOT MATCH, REGENERATE.**

**Red Flags**:
- "Key points" instead of complete lists
- Charts showing only "top N items"
- Bullet counts that don't match source
- Phrasing that doesn't match source exactly

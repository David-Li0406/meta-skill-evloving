# UXR Report Analyzer - Quality Checklist

Use this checklist when running the skill to ensure complete and high-quality analysis.

## Pre-Analysis Checklist

- [ ] PDF path is absolute and file exists
- [ ] Prometheus tools are available (mcp__prometheus__*)
- [ ] User has been asked for original URL
- [ ] Current month-year determined for filename (MM-YYYY format)
- [ ] Project context files are accessible:
  - [ ] `/Users/jvincent/Projects/writing/resources/CLAUDE.md`
  - [ ] `/Users/jvincent/Projects/writing/resources/UXR Reports/Analysis/claude.md`
  - [ ] `/Users/jvincent/Projects/writing/resources/2026 S7/claude.md`

## PDF Processing Checklist

- [ ] Used `prometheus_info` to assess PDF complexity
- [ ] Selected appropriate extraction strategy:
  - [ ] Small report (<50 pages): Direct extraction
  - [ ] Large report (50-150 pages): Extract with chunking
  - [ ] Very large report (>150 pages): Split first, then extract
- [ ] `include_page_numbers: true` set for reference tracking
- [ ] `clean_text: true` set for better readability
- [ ] All chunks/sections reviewed for completeness

## Analysis Content Checklist

### HTML Comment Summary (Lines 1-9)
- [ ] Title matches report name
- [ ] Type accurately describes research methodology
- [ ] Key Themes are specific and insightful (3-5 themes)
- [ ] Core Insights are substantive (2-3 sentences)
- [ ] Relevance explicitly connects to strategic objectives (SO1-SO5)
- [ ] Quality assessment justified (High/Medium/Low with reason)
- [ ] Last Reviewed date is current (YYYY-MM-DD format)

### Metadata Section
- [ ] Study Name is official/accurate
- [ ] Created By lists researchers/team
- [ ] Study URL included (or "URL not available" if user skipped)
- [ ] Optional fields added if available (Date, Research Scope, Type)

### The Big Picture Section
- [ ] 2-3 paragraphs (not more, not less)
- [ ] Paragraph 1: Research question and headline findings
- [ ] Paragraph 2: Connection to HubSpot's Overall Data Strategy
- [ ] Paragraph 3: Strategic implications and next steps
- [ ] Avoids jargon; uses clear, powerful language
- [ ] References specific strategic objectives when relevant
- [ ] Explains alignment OR tension with current strategy

### Key Findings Section
- [ ] 3-7 major findings identified
- [ ] Each finding has descriptive header
- [ ] Bullet points include specific details (numbers, quotes, examples)
- [ ] Findings are grouped by themes
- [ ] Prioritized by strategic importance
- [ ] Each finding traces to actual report content

### Interesting Metrics Section (if applicable)
- [ ] Only included if highly significant quantitative data exists
- [ ] Each metric is specific: "X% of Y do Z"
- [ ] Source references included (page/slide numbers)
- [ ] Numbers are surprising or strategically important
- [ ] Section omitted if no standout metrics

### Recommendations Section
- [ ] Split into Strategic Initiatives and Tactical Actions
- [ ] Strategic: 2-4 long-term, cross-functional initiatives
- [ ] Tactical: 3-5 near-term, specific actions
- [ ] Each recommendation connects to specific findings
- [ ] Recommendations are actionable and specific
- [ ] Success criteria included where possible
- [ ] Prioritized by impact and feasibility

### Connected Research Section
- [ ] 3-5 related studies identified
- [ ] All referenced research exists in catalog
- [ ] Each connection explicitly explained (2-3 sentences)
- [ ] Connections are substantive, not superficial
- [ ] Shows how research builds on or complements each other
- [ ] References actual titles from UXR catalog

### Disconnected Research Section (if applicable)
- [ ] Only included if genuine contradictions exist
- [ ] Each contradiction clearly explained
- [ ] Implications of disconnect analyzed
- [ ] Not confused with different scopes or segments
- [ ] Section omitted if no meaningful contradictions

### Slide/Section Index
- [ ] Grouped by theme (not every single slide listed)
- [ ] Page/slide numbers included for reference
- [ ] Major sections and transitions captured
- [ ] Useful for future searches
- [ ] Format matches report structure (slides vs sections)

## Quality Standards Checklist

- [ ] **Specificity**: Uses exact numbers, percentages, direct quotes
- [ ] **Strategic Connection**: Every insight tied to business implications
- [ ] **Honesty**: Research limitations acknowledged where applicable
- [ ] **Connected**: References other research; builds knowledge graph
- [ ] **Clarity**: No unnecessary jargon; frameworks explained simply
- [ ] **Customer Voice**: Direct quotes used when available
- [ ] **Actionability**: Recommendations are specific and implementable
- [ ] **Context**: HubSpot strategy referenced explicitly

## File Handling Checklist

- [ ] Filename format correct: `[Report_Name]_Analysis_[MM-YYYY].md`
- [ ] Special characters removed from filename
- [ ] Underscores used instead of spaces
- [ ] Current month-year included (e.g., `11-2025`)
- [ ] Saved to: `/Users/jvincent/Projects/writing/resources/UXR Reports/Analysis/`
- [ ] Original PDF moved from `Reports to Review/` to `Reviewed Reports/` using Bash mv command
- [ ] PDF move confirmed successful (file exists in destination, not in source)
- [ ] User notified that PDF has been archived

## Catalog Update Checklist

- [ ] New entry added to `/Users/jvincent/Projects/writing/resources/UXR Reports/Analysis/claude.md`
- [ ] Entry includes:
  - [ ] Title and link to analysis file
  - [ ] Type and metadata
  - [ ] Summary paragraph
  - [ ] Key findings bullets
  - [ ] Notable metrics
  - [ ] Connection to strategic objectives
  - [ ] Quality assessment
- [ ] Placed in appropriate category (Marketing, Data, Admin, AI, Events)
- [ ] Resource count updated in catalog header
- [ ] Statistics section updated

## Final Review Checklist

- [ ] Analysis is comprehensive but concise
- [ ] All sections flow logically
- [ ] Markdown formatting is correct
- [ ] No placeholder text remains ([TBD], [TODO], etc.)
- [ ] Cross-references are accurate
- [ ] Strategic implications are clear
- [ ] Document is ready for use in strategic planning

## Common Issues to Avoid

- [ ] Avoided generic summaries; analysis includes "what it means" not just "what it says"
- [ ] Avoided missing numbers; specific metrics included throughout
- [ ] Avoided disconnected recommendations; all trace to findings
- [ ] Avoided ignoring contradictions; conflicts addressed honestly
- [ ] Avoided abstract language; concrete examples used
- [ ] Avoided isolated analysis; connected to broader strategic context
- [ ] Avoided missing strategic connection; ties to HubSpot's Overall Data Strategy explicit

---

## Skill Validation Checklist

For the skill itself (not each analysis):

- [x] YAML frontmatter includes `name` (≤64 chars) and `description` (≤200 chars)
- [x] Description clearly states when to use: "Use when given a UXR report to analyze"
- [x] Instructions specify required tools (Prometheus, AskUserQuestion, Read, Write)
- [x] Template files exist in resources folder
- [x] Examples show clear input → output flow
- [x] No hardcoded secrets or credentials
- [x] File handling instructions are clear
- [x] Catalog update process documented
- [x] Security and privacy considerations addressed

---

Use this checklist each time you run the UXR Report Analyzer skill to ensure consistent, high-quality outputs.

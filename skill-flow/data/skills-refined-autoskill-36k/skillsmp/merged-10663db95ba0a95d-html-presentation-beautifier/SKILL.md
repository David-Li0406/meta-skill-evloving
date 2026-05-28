---
name: html-presentation-beautifier
description: Transform documents, reports, and data into professional McKinsey-style HTML presentations with intelligent chart selection and interactive navigation. Use when creating presentations from documents or reports, converting markdown/text to slides, generating HTML slides, applying McKinsey/BCG design, or visualizing data in presentations.
---

# HTML Presentation Beautifier

Transform raw data and conclusion documents into professional HTML presentations with McKinsey-style design, strict color schemes, hierarchical structure, and chart visualizations without modifying the original content.

## Process Overview

This skill follows a structured multi-phase process:

1. **Phase 1**: Document Parsing - Extract and understand source document structure.
2. **Phase 2**: Content Structuring - Organize content into slide-friendly format using AI-powered subagents.
3. **Phase 3**: Design & Layout - Apply McKinsey-style design system.
4. **Phase 3.5**: Content Visualization - Enhance slides with appropriate charts and graphics.
5. **Phase 4**: HTML Generation - Generate a single-file, self-contained HTML presentation.
6. **Phase 5**: Review & Verify - Automatically review generated HTML for quality and compliance.

## Design System (McKinsey/BCG Style)

### Color Palette

| Color Type | Hex Code | Usage |
|------------|----------|-------|
| Primary Background | `#FFFFFF` | Slide background |
| Header Background | `#000000` | Title bars |
| Primary Accent | `#F85d42` | Key highlights, CTAs |
| Secondary Accent | `#74788d` | Supporting text |
| Deep Blue | `#556EE6` | Charts, data points |
| Green | `#34c38f` | Success indicators |
| Blue | `#50a5f1` | Neutral emphasis |
| Yellow | `#f1b44c` | Warnings, notes |

### Typography

- **Title**: Large (48-64px), Bold, Black (`#000000`)
- **Subtitle**: Medium (28-36px), Bold, Accent Color (`#F85d42` or `#74788d`)
- **Body Text**: Regular (16-20px), Regular, Dark Gray (`#333333`)
- **Emphasis**: Regular with Accent Color or Bold
- **Chart Labels**: Small (12-14px), Clear, Readable

### Design Principles

- **Modern Business Style**: Clean, professional, minimal clutter.
- **Visual Hierarchy**: Clear distinction between titles, subtitles, and body.
- **Consistency**: Uniform design language across all slides.
- **Data-Driven**: Use charts and visualizations for quantitative information.
- **Professional Polish**: McKinsey/BCG consultation presentation quality.

## Phase 1: Document Parsing

**Goal**: Extract and analyze the source document to understand content structure, data points, and conclusions.

**Prerequisites**:
- Source document provided (Markdown, text, or structured format)
- No prior modifications to original content

**Checklist**:
- [ ] Document format identified and readable
- [ ] Document structure parsed (headings, lists, data tables, conclusions)
- [ ] Key data points and metrics extracted
- [ ] Main conclusions and insights identified
- [ ] Content hierarchy mapped (H1 → H2 → H3)

**Exit Criteria**: Document fully parsed with content structure mapped and data points catalogued.

## Phase 2: Content Structuring (Using Subagent)

**Goal**: Transform parsed content into slide-friendly format while preserving all original meaning and conclusions.

**Approach**: Use the `Task` tool with subagent to intelligently plan slide structure.

**Subagent Specification**:
- **Type**: `general-purpose`
- **Task**: Plan slide structure from parsed document
- **Input**: Parsed document with sections, data points, and conclusions
- **Output**: Structured slide plan with slide types, content assignments, and visualizations

**Exit Criteria**: Structured slide plan received from subagent with all slides defined, visualizations assigned, and zero content loss.

## Phase 3: Design & Layout

**Goal**: Apply McKinsey-style design system to structured content for professional presentation.

**Checklist**:
- [ ] Slide layouts selected for each content type
- [ ] Color scheme applied consistently
- [ ] Typography hierarchy established
- [ ] White space and spacing optimized

**Exit Criteria**: All slides designed with consistent McKinsey-style branding, professional layout, and optimized typography.

## Phase 3.5: Content Visualization Beautification (Using Subagent)

**Goal**: Beautify content with appropriate charts and graphics, avoiding pure text lists.

**Approach**: Use `Task` tool with `general-purpose` subagent.

**Subagent Task**:
- Input: Structured slide plan from Phase 2
- Output: Enhanced slide plan with specific visualization types assigned

**Exit Criteria**: All content slides enhanced with appropriate visualizations, no plain text bullet lists for insights.

## Phase 4: HTML Generation (Using Subagent)

**Goal**: Generate single-file, self-contained HTML presentation.

**Approach**: Use `Task` tool with `general-purpose` subagent to generate complete HTML presentation.

**Exit Criteria**: Complete HTML presentation file generated, ready to open in browser, with all slides, styling, and interactivity working correctly.

## Phase 5: Review & Verify (Using Subagent)

**Goal**: Automatically review generated HTML for quality, integrity, and compliance.

**Exit Criteria**: HTML presentation reviewed and approved with detailed report.

## Interactive Features

### Navigation
- **Buttons**: Previous/Next buttons in navbar
- **Keyboard**: Arrow keys (←/→), Space (next), Escape (exit fullscreen)
- **Slide counter**: Shows current position (e.g., "Slide 3 of 7")

### Full-Screen Mode
- Toggle button (⛶) in bottom-right corner
- Escape key to exit

## NEVER Do These

- **NEVER modify original content or conclusions**: The presentation must preserve all original meaning, data, and conclusions exactly.
- **NEVER add fabricated data**: Only use data from the source document.
- **NEVER use AI-generated placeholder text**: Use actual content from source.
- **NEVER deviate from color scheme**: Strict adherence to the specified McKinsey-style palette.
- **NEVER use inconsistent typography**: Maintain hierarchy and style across all slides.
- **NEVER overcrowd slides**: Use generous white space and focus on key messages.

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

## Resources

All detailed guides are in `references/`:

- **Design System**: `mckinsey-design-system.md` - Colors, typography, layouts
- **Templates**: `template-guide.md` - Template usage instructions
- **Chart Selection**: `chart-selection-guide.md` - Decision trees for visualizations
- **Subagent Prompts**: `subagent-prompts.md` - Optimized prompts for all phases
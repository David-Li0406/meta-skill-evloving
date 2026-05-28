# Slide Deck & Presentation Styles

Prompt templates for professional presentation slides, infographics, and slide deck content.

**⚠️ NotebookLM Style**: Apply aesthetic but **NEVER** use "NotebookLM" brand/logo in prompts (see SKILL.md for details)

**Important**: All slide deck styles automatically use **lossless WebP** format (VP8L encoding):
- Saves 20-30% file size compared to PNG (typical for diagrams/slides)
- Perfect for slides with text, icons, and graphics
- Completely lossless (zero quality degradation)
- Much better than lossy formats (lossy WebP saves 95% but blurs text)
- This is automatically applied when using `style: trend` or `style: notebooklm`

## Visual Styles Overview

| Style | Best For | Key Characteristics |
|-------|----------|---------------------|
| **Professional** | Business reports, tech presentations | Deep blue background, clean typography, neon accents |
| **Blackboard** | Educational content, tutorials | Green/black board, chalk texture, hand-drawn feel |
| **Data Viz** | Charts, metrics, analytics | High contrast, clean gridlines, pictogram callouts |
| **Process Flow** | Step-by-step guides, workflows | Numbered steps, connecting arrows, geometric shapes |
| **Overview** | Concept summaries, topic introductions | Bento grid layout, pastel colors, icon-driven |

## Layout Patterns

Common presentation layouts:

- **Timeline**: Horizontal or vertical chronological flow
- **Hub & Spoke**: Central concept with radiating details
- **Bento Grid**: Rectangular sections in organized grid
- **Zig-Zag Flow**: Alternating left-right step progression
- **Comparison Matrix**: Side-by-side comparison table
- **Pyramid/Funnel**: Hierarchical information flow

## Prompt Templates

### 1. Professional Infographic

For business presentations and tech content:

```
Create a clean, modern infographic explaining "[TOPIC]".

Visual style: Professional editorial with sleek corporate aesthetic
Layout: [Timeline/Grid/Hub-spoke] arrangement
Colors: Deep blue background (#003366), white text, light neon accent highlights
Typography: Bold headers, clean sans-serif body text

Include:
- Large title at top: "[TITLE]"
- [N] main sections with icons
- Clear labels and minimal text per section
- Footer with source attribution

Format: 16:9 landscape, suitable for presentation slides
```

**Example use**:

```
Create a clean, modern infographic explaining "CI/CD Pipeline Best Practices".

Visual style: Professional editorial with sleek corporate aesthetic
Layout: Hub-spoke arrangement with pipeline at center
Colors: Deep blue background (#003366), white text, cyan (#00d4ff) accent highlights
Typography: Bold headers, clean sans-serif body text

Include:
- Large title at top: "Modern CI/CD Pipeline"
- 6 main sections with icons (Build, Test, Deploy, Monitor, Feedback, Security)
- Clear labels and minimal text per section
- Footer: "DevOps Best Practices 2025"

Format: 16:9 landscape, suitable for presentation slides
```

### 2. Blackboard/Chalkboard Style

For educational and tutorial content:

```
Create an educational infographic in chalkboard art style.

Visual style: White and colored chalk drawings on a deep green/black blackboard
Layout: [Step-by-step/Tree diagram/Central concept with branches]
Colors: Green blackboard background, white chalk primary, yellow and pink chalk accents

Content: "[EDUCATIONAL TOPIC]"
Include:
- Hand-drawn style icons and illustrations
- Chalk texture on all text and elements
- Mathematical or scientific annotations if relevant
- Title written in decorative chalk lettering

Format: 4:3 or 16:9, classic classroom feel
```

**Example use**:

```
Create an educational infographic in chalkboard art style.

Visual style: White and colored chalk drawings on a deep green blackboard (#2d4a3e)
Layout: Tree diagram with root concept at bottom branching upward
Colors: Green blackboard background, white chalk primary, yellow and pink chalk accents

Content: "How Neural Networks Learn"
Include:
- Hand-drawn neuron icons and network connections
- Chalk texture on all text and elements
- Simple equations showing weight updates
- Title "Neural Networks 101" in decorative chalk lettering

Format: 16:9, classic classroom feel
```

### 3. Data Visualization

For metrics, charts, and analytics:

```
Design a structured infographic titled "[TITLE]".

Visual style: Data visualization for professional slides
Layout: [Bar chart/Pie chart/Clustered column] with supporting text sections
Colors: [Color scheme] palette with high contrast for readability

Include:
- Large header section with title
- [N] data visualizations (charts/graphs)
- Percentage callouts with pictogram style
- Clean gridlines, minimal legend
- Consistent spacing and alignment

Format: 16:9 landscape, suitable for tech/business presentations
```

**Example use**:

```
Design a structured infographic titled "2025 Cloud Adoption Metrics".

Visual style: Data visualization for professional slides
Layout: Clustered column chart showing 5 cloud services over 4 quarters
Colors: Navy (#1a2332), cobalt (#0066cc), cyan (#00d4ff) palette with high contrast

Include:
- Large header section with title "Cloud Service Growth Q1-Q4 2025"
- 3 data visualizations (adoption chart, cost comparison, satisfaction scores)
- Percentage callouts ("+45% YoY") with cloud icon pictograms
- Clean gridlines, minimal legend at bottom
- Consistent spacing and alignment

Format: 16:9 landscape, suitable for tech presentations
```

### 4. Step-by-Step Process

For workflows and procedures:

```
Generate an infographic showing "[N] Steps of [PROCESS]".

Visual style: Modern corporate with geometric shapes
Layout: Horizontal zig-zag OR vertical ladder-style flow
Colors: Navy (#001f3f), cobalt (#0047AB), white palette

Each step includes:
- Large number label (1, 2, 3...)
- Strong iconic representation
- Two-line description
- Connecting arrows or lines between steps

Add footer bar with source attribution
Format: Portrait or landscape based on number of steps
```

**Example use**:

```
Generate an infographic showing "5 Steps of Incident Response".

Visual style: Modern corporate with geometric shapes
Layout: Horizontal zig-zag flow connecting all 5 steps
Colors: Navy (#001f3f), red (#dc3545), white palette

Each step includes:
- Large number label (1: Detect, 2: Analyze, 3: Contain, 4: Eradicate, 5: Recover)
- Strong iconic representation (magnifying glass, chart, shield, trash, checkmark)
- Two-line description per step
- Bold arrows connecting steps sequentially

Add footer bar: "Cybersecurity Incident Response Framework"
Format: 16:9 landscape
```

### 5. Concept Overview

For topic introductions and summaries:

```
Create a summary-style infographic titled "[TOPIC] Overview".

Visual style: Editorial infographic with modern minimalist aesthetic
Layout: [4-6] large rectangular sections in bento grid arrangement
Colors: Pastel palette (muted blues, greens, corals) with white background

Each section includes:
- Representative icon
- Bold title
- 2-3 bullet points
- Subtle dotted or geometric patterns

Typography: Bold headers, light body text, left-aligned for readability
Format: Square or 4:3
```

**Example use**:

```
Create a summary-style infographic titled "Kubernetes Overview".

Visual style: Editorial infographic with modern minimalist aesthetic
Layout: 6 large rectangular sections in bento grid (2x3)
Colors: Pastel palette (muted blue #7eb2dd, teal #6dcbcf, coral #f4978e) with white background

Each section includes:
- Representative icon (container, orchestration, scaling, networking, storage, security)
- Bold title ("Containers", "Orchestration", "Auto-scaling", "Networking", "Storage", "Security")
- 2-3 bullet points explaining key concept
- Subtle gear pattern or container icons in background

Typography: Bold Inter headers, light Roboto body, left-aligned
Format: 4:3 for easy reading
```

## Professional Presentation Style Prompts

For slides with clean, modern professional aesthetic:

### Standard Professional Style

```
Create a presentation slide in clean professional style.

Topic: "[YOUR TOPIC]"

Visual characteristics:
- Polished, well-structured tech infographic aesthetic
- Clean slide-level organization with logical flow
- Professional but accessible design
- Clear visual hierarchy

Style reference: Similar to Google's product documentation or modern tech blog infographics (avoid branding)

Content structure:
- Title slide OR content slide
- Key points with supporting visuals
- Minimal text, maximum visual communication
- Icons and simple illustrations over complex graphics

Format: 16:9 landscape
```

### Detailed vs Presenter Slides

**Detailed Deck** (for reading/sharing):

```
Create a comprehensive presentation slide with full text and details.
Include complete explanations, data points, and context.
Format for reading/sharing without presenter notes.
```

**Presenter Slides** (for live presentation):

```
Create a clean, visual presenter slide with key talking points only.
Focus on visual impact over text density.
Large visuals, minimal bullet points, clear focal areas.
```

## Advanced Techniques

### Using Reference Sketches

Upload hand-drawn layouts for structure:

```
Use the layout from the attached image as a structural guide.
[Upload sketch/wireframe]
Maintain the placement and proportions while rendering in polished style.
```

### Iterative Refinement

Request specific changes instead of regenerating:

```
Change the color scheme to [NEW COLORS].
Move the title to the center.
Add more visual emphasis to section 2.
Make the text neon blue.
```

### Content Grounding

Provide source material for accuracy:

```
Create an infographic using the following information:
[Paste article, bullet points, or data]

Summarize and visualize the key concepts in an accessible format.
```

## Complete Examples

### Example 1: LLM Introduction

```
Create a professional infographic explaining "Introduction to Large Language Models (LLMs)".

Visual style: Modern tech infographic, clean professional presentation aesthetic
Layout: Central concept (LLM) with radiating key features in hub-spoke pattern
Colors: Deep blue (#0a2463) background, white text, teal (#2cafa4) and coral (#ff6b6b) accents

Include:
- Title: "Understanding LLMs" in bold at top
- Central brain/neural network illustration
- 5 key concepts radiating outward:
  * Training Data (database icon)
  * Parameters (slider icon)
  * Tokenization (text blocks icon)
  * Attention (eye/focus icon)
  * Generation (sparkle/output icon)
- Each concept: simple icon and 1-line description
- Subtle grid pattern in background

Format: 16:9 landscape, suitable for educational presentation
```

### Example 2: Security Best Practices (Trend + Professional Style)

```
Create a cybersecurity infographic titled "5 Essential Security Practices" in professional presentation style with Trend Micro branding.

Visual style: Professional slide design aesthetic with Trend Micro brand colors
- Polished, well-structured tech infographic
- Clean slide-level organization with logical flow
- Professional but accessible design
- Clear visual hierarchy

Layout: Numbered vertical list (1-5) with icons on left, descriptions on right
Colors (Trend Micro brand palette):
- Primary: Trend Red #d71920 as accent/highlight for numbers and key elements
- Secondary: Dark blue #005295, teal #2cafa4 for icons
- Background: Dark gray #333333 or white (#ffffff) - choose based on content density
- Text: White (#ffffff) and light gray (#e0e0e0) on dark, or dark gray on white
- Guardian Red #6f0000 for critical/intensity elements if needed

Include:
- Bold title at top with shield icon
- 5 practices with large numbers, icons, titles, brief descriptions:
  1. Multi-Factor Authentication (lock+key icon)
  2. Regular Updates (refresh icon)
  3. Strong Passwords (shield+checkmark icon)
  4. Data Encryption (padlock icon)
  5. Security Awareness (person+shield icon)
- Minimal text, maximum visual communication
- Icons and simple illustrations over complex graphics
- Protective gradient overlay or security pattern elements (subtle)
- Footer: "Cybersecurity Best Practices 2025"

Format: 16:9, suitable for professional presentation
Style reference: Similar to Google's product documentation or modern tech blog infographics, but with Trend Micro color scheme
```

**When to use Trend style**: The Trend Micro brand style automatically combines clean professional slide aesthetic with Trend's brand color palette. Perfect for corporate presentations, technical documentation, and professional slide decks.

### Example 3: ML Workflow

```
Create a step-by-step process infographic showing "How Machine Learning Works".

Visual style: Educational whiteboard/chalkboard aesthetic
Layout: Horizontal flow with 5 connected steps left to right
Colors: Deep green chalkboard (#2d4a3e), white chalk text, yellow chalk highlights

Steps (with chalk-style hand-drawn icons):
1. Data Collection - spreadsheet/folder icon
2. Preprocessing - funnel/filter icon
3. Model Training - gears/cogs icon
4. Evaluation - chart/metrics icon
5. Deployment - cloud/rocket icon

Each step includes:
- Chalk-style icon illustration
- Hand-lettered step title
- 1-2 line description in chalk text
- Arrow pointing to next step
- Small annotations/notes around icons

Add chalk dust effects and eraser marks for authenticity
Title: "Machine Learning Pipeline" in decorative chalk lettering

Format: 16:9 landscape
```

## Usage Tips

1. **Specify aspect ratio**: Use `16:9` for slides, `4:3` for traditional presentations, `1:1` for social media
2. **Include text explicitly**: Write exact titles and labels in the prompt
3. **Reference real data**: Provide actual numbers, percentages, or content when available
4. **Iterate strategically**: Make small adjustments rather than full regeneration
5. **Use natural language**: Describe what you want conversationally, not as keyword tags
6. **File format**: Slide deck styles automatically use lossless WebP (VP8L) - no need to specify format, it's optimized for your content type

---

## Multi-Slide Generation

**Mode Selection (Automatic):**
- **5+ slides**: Use batch mode for maximum efficiency (80% context reduction) → See `batch-generation.md`
- **3-4 slides**: Use Task agents for parallel generation (documented below)
- **1-2 slides**: Sequential direct execution

**For 5+ slides:** This document focuses on 3-4 slide generation. For larger decks (5+ slides), see the complete batch generation workflow in `batch-generation.md`.

---

### Generating 3-4 Slides with Task Agents

When generating 3-4 slides for a presentation, use the **Hybrid Mode**: Plan → Parallel Generation → Review.

### Phase 1: Planning

Before generating, plan the entire deck:

**1. Define overall theme and style**
- Choose visual style (Professional, Blackboard, Data Viz, etc.)
- Lock down color palette (specific hex codes)
- Set consistent layout format (16:9, 4:3)

**2. Create content outline**

```
Slide 1: Title - "Presentation Title"
Slide 2: Overview - 3 key points
Slide 3: Details - Deep dive on point 1
Slide 4: Data - Charts and metrics
Slide 5: Conclusion - Summary and CTA
```

**3. Pre-plan output directory and file structure**

All slides should be saved in a **single directory** with numbered filenames:

```
001-presentation-topic/
  ├── 001-title.webp
  ├── 002-overview.webp
  ├── 003-details.webp
  ├── 004-data-viz.webp
  └── 005-conclusion.webp
```

**Critical:** Do NOT create separate directories per slide. Use one shared directory with numbered files.

### Phase 2: Parallel Generation (using Task agents)

For **3+ slides**, use Task agents for parallel generation:

```
# Dispatch multiple agents simultaneously (single message, multiple Task calls)
Task("Generate slide 1: Title slide, style: trend, colors: #d71920...")
Task("Generate slide 2: Overview, style: trend, colors: #d71920...")
Task("Generate slide 3: Details, style: trend, colors: #d71920...")
// All run in parallel
```

**Critical - Pass identical style specification to each agent:**
- Same colors, fonts, layout
- Same `use_lossless = True` for consistency
- Same aspect ratio and image size
- Same visual style reference

### Phase 3: Review & Adjust

After parallel generation:

1. **Visual review** - Compare all slides side by side
2. **Consistency check** - Do colors, fonts, icon styles match?
3. **Sequential fixes** - Regenerate any inconsistent slides one by one

### When to Use Each Approach

| Slides | Approach | Reason |
|--------|----------|--------|
| 1-2 | Sequential | Faster, no coordination overhead |
| 3-5 | Parallel | Speed benefit outweighs coordination cost |
| 6+ | Parallel (batches of 3-5) | Split into manageable batches |

### Example Prompt for Parallel Generation

```
Generate a 5-slide presentation deck about "Cloud Security Best Practices".

Style: trend (Trend Micro brand + professional aesthetic)
Format: 16:9, lossless WebP
Color lock:
- Trend Red #d71920 (primary/accent)
- Dark Blue #005295 (secondary)
- Gray #333333 (background)
- White #ffffff (text)

Slides:
1. Title: "Cloud Security Best Practices 2025"
   - Large title centered
   - Subtitle: "Protecting Your Infrastructure"
   - Minimal design with shield icon

2. Overview: "5 Key Practices"
   - Hub-spoke layout
   - 5 practices radiating from center

3. Identity: "IAM and Zero Trust"
   - Icons + 3-4 bullet points per section
   - Split layout (left: IAM, right: Zero Trust)

4. Data Protection: "Encryption Metrics"
   - Bar chart showing encryption adoption
   - 3 key statistics with percentage callouts

5. Summary: "Action Items"
   - Numbered list (1-5)
   - Each with icon and brief description
   - Footer CTA

**Output directory structure:**
All slides in one directory: `001-cloud-security/`
  ├── 001-title.webp
  ├── 002-overview.webp
  ├── 003-identity.webp
  ├── 004-data-protection.webp
  └── 005-summary.webp

Use parallel Task agents to generate all 5 slides simultaneously.
After generation, review consistency and adjust if needed.
```

### Example 2: Professional Editorial Style (NotebookLM-Inspired Aesthetic)

**⚠️ IMPORTANT**: This example shows how to use `style: notebooklm` trigger WITHOUT including NotebookLM branding in the output.

```
Generate a 5-slide presentation deck about "AI Product Development Best Practices".

Style specification for Claude: notebooklm
⚠️ CRITICAL: When writing the Gemini prompt below, translate to descriptive terms:
- DO NOT include "NotebookLM" in the prompt sent to Gemini
- DO NOT generate NotebookLM logos, branding, or watermarks
- Use descriptive style terms instead (see below)
Format: 16:9, lossless WebP
Color palette:
- Deep blue #0a2463 (primary/headers)
- Teal #2cafa4 (accent/icons)
- Coral #ff6b6b (highlights/callouts)
- Light gray #f5f5f5 (background)
- White #ffffff (cards/text boxes)

Visual characteristics (descriptive terms for Gemini prompt):
- "Clean professional presentation aesthetic with polished tech infographic style"
- "Modern documentation visual design similar to Google's product guides"
- "Well-structured slide-level organization with logical information flow"
- "Professional but accessible design with clear visual hierarchy"
- "Minimal text, maximum visual communication using icons and simple illustrations"
- ⚠️ DO NOT mention "NotebookLM" anywhere in the prompt sent to Gemini

Slides:
1. Title: "AI Product Development"
   - Large centered title
   - Subtitle: "Best Practices for 2025"
   - Simple AI icon or abstract geometric pattern
   - Clean white background

2. Overview: "5 Core Principles"
   - Hub-spoke layout with AI icon at center
   - 5 principles radiating outward:
     * User-Centric Design
     * Data Quality
     * Ethical AI
     * Iterative Testing
     * Continuous Learning

3. User-Centric: "Designing for Humans"
   - Split layout (left: problem, right: solution)
   - 3 key points with icons
   - Real-world example callout box

4. Metrics: "Measuring AI Success"
   - Bento grid layout (2x2)
   - 4 metrics with large numbers and trend arrows
   - Clean data visualization style

5. Action Plan: "Getting Started"
   - Numbered steps (1-4) in vertical flow
   - Each with icon, title, brief description
   - Bottom CTA: "Start Your AI Journey"

**Output directory structure:**
All slides in one directory: `001-ai-product-dev/`
  ├── 001-title.webp
  ├── 002-overview.webp
  ├── 003-user-centric.webp
  ├── 004-metrics.webp
  └── 005-action-plan.webp

Use parallel Task agents to generate all 5 slides simultaneously.
Ensure consistent color usage and clean professional aesthetic across all slides.
⚠️ REMINDER: Never include "NotebookLM" text, logos, or branding in any generated slide.
```

### Best Practices for Multi-Slide Generation

**Do:**
- ✅ Define complete style spec before starting
- ✅ Use consistent hex codes (not "red", use "#d71920")
- ✅ Pre-plan all directory names
- ✅ Pass identical parameters to each agent
- ✅ Review and adjust after generation

**Don't:**
- ❌ Mix styles between slides (keep consistent)
- ❌ Forget to specify `use_lossless = True`
- ❌ Use vague color names ("blue" → specify "#005295")
- ❌ Generate too many at once (>5 risks inconsistency)
- ❌ Skip the review phase

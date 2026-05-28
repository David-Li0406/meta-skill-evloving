---
name: html-presentation-beautifier
description: "Transform data and conclusion documents into professional HTML presentations with McKinsey-style design. Use when user asks for: presentation beautification, HTML slides, data visualization, professional reports, McKinsey-style formatting."
---

# HTML Presentation Beautifier

Transform raw data and conclusion documents into professional HTML presentations with McKinsey-style design, strict color schemes, hierarchical structure, and chart visualizations without modifying the original content.

## Process Overview

This skill follows a structured multi-phase process:

1. **Phase 1**: Document Parsing - Extract and understand source document structure
2. **Phase 2**: Content Structuring - Organize content into slide-friendly format
3. **Phase 3**: Design & Layout - Apply McKinsey-style design system
4. **Phase 4**: HTML Generation - Generate presentation HTML with interactive features

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

- **Modern Business Style**: Clean, professional, minimal clutter
- **Visual Hierarchy**: Clear distinction between titles, subtitles, and body
- **Consistency**: Uniform design language across all slides
- **Data-Driven**: Use charts and visualizations for quantitative information
- **Professional Polish**: McKinsey/BCG consultation presentation quality

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

**Steps**:
1. Read the source document completely without modification
2. Identify document type (report, analysis, research, etc.)
3. Extract structural elements:
   - Headings and subheadings
   - Bullet points and numbered lists
   - Data tables and numerical data
   - Key conclusions and recommendations
4. Map content hierarchy: main topics → subtopics → supporting details
5. Identify quantitative data suitable for charts/graphs

**Exit Criteria**: Document fully parsed with content structure mapped and data points catalogued.

**MANDATORY - READ BEFORE STARTING**: Before beginning Phase 1, read [`references/parsing-guidelines.md`](references/parsing-guidelines.md) completely.

## Phase 2: Content Structuring (Using Subagent)

**Goal**: Transform parsed content into slide-friendly format while preserving all original meaning and conclusions.

**Prerequisites**:
- Phase 1 completed with content structure mapped
- All key data points and conclusions identified

**Approach**: Use the `Task` tool with subagent to intelligently plan slide structure.

**Subagent Specification**:
- **Type**: `general-purpose`
- **Task**: Plan slide structure from parsed document
- **Input**: Parsed document with sections, data points, and conclusions
- **Output**: Structured slide plan with slide types, content assignments, and visualizations

**Prompt Template**:
```python
Task(
    subagent_type="general-purpose",
    description="Plan presentation slides",
    prompt=f"""You are a presentation planning specialist. Analyze this document and create a detailed slide plan.

DOCUMENT CONTENT:
{parsed_document_content}

YOUR TASK:
1. Create a slide plan following this structure:
   - Title slide (always first)
   - Executive summary (if conclusions exist)
   - Data visualization slides (for sections with numerical data)
   - Conceptual slides (for non-numerical frameworks)
   - Content slides (for detailed information)
   - Conclusions slide (if recommendations exist)

2. For each slide, specify:
   - Slide type: [TITLE, EXECUTIVE_SUMMARY, DATA_VISUALIZATION, CONCEPTUAL, CONTENT, CONCLUSIONS]
   - Title: Clear, concise heading
   - Content: Key points to include (preserve exact wording)
   - Visualization type: (for DATA_VISUALIZATION slides)
   - Layout: [title-center, bullet-points, two-column, full-width, conclusions-grid]

3. Smart chart selection for data slides:
   - Rankings/Hierarchy → polarArea, bar
   - Flow/Journey → line, funnel
   - Distribution → bubble, polarArea
   - Time/Cyclical → line, polarArea, step
   - KPI/Target → bar, bullet
   - Multi-dimensional → radar
   - Proportions → doughnut (≤5 items), pie (≤8 items), bar
   - Trends → line
   - Comparison → bar
   - Strategic → scatter, matrix
   - See SKILL.md "Chart Visualizations" section for complete list

4. For conceptual slides, detect type:
   - Hierarchy/Level → pyramid
   - Process/Steps → progression
   - Key Points → emphasis
   - Loop/Feedback → cycle
   - Before/After → comparison
   - Framework/Model → framework

OUTPUT FORMAT:
Return a structured slide plan in JSON format:
{{
  "title": "Presentation Title",
  "total_slides": N,
  "slides": [
    {{
      "slide_number": 1,
      "slide_type": "TITLE",
      "title": "...",
      "content": "...",
      "key_points": ["...", "..."],
      "layout": "title-center"
    }}
  ]
}}

CRITICAL RULES:
- Preserve ALL original conclusions and recommendations exactly
- Do NOT fabricate data or insights
- Maximum 5-8 key points per slide
- Each slide must have ONE clear message
- Use exact text from source document
"""
)
```

**Checklist**:
- [ ] Subagent invoked with proper context
- [ ] Slide plan generated with clear structure
- [ ] Data visualization types assigned intelligently
- [ ] Conceptual types detected for non-numerical content
- [ ] All original conclusions preserved exactly
- [ ] No content lost or fabricated

**Exit Criteria**: Structured slide plan received from subagent with all slides defined, visualizations assigned, and zero content loss.

## Phase 3: Design & Layout

**Goal**: Apply McKinsey-style design system to structured content for professional presentation.

**Prerequisites**:
- Phase 2 completed with slide structure defined
- All data visualizations assigned

**Checklist**:
- [ ] Slide layouts selected for each content type
- [ ] Color scheme applied consistently
- [ ] Typography hierarchy established
- [ ] White space and spacing optimized
- [ ] Charts and visuals designed with professional polish

**Steps**:
1. Select appropriate layout for each slide:
   - **Full-width title** for section headers
   - **Two-column** for comparison slides
   - **Three-column** for multiple data points
   - **Center focus** for key messages
   - **Chart + text** for data slides
2. Apply color scheme:
   - White background for all slides
   - Black header bars with white text
   - Orange accent (`#F85d42`) for key metrics and CTAs
   - Gray (`#74788d`) for secondary text
   - Chart colors from palette (blue, green, yellow) for variety
3. Set typography:
   - Title: 48-64px bold black
   - Subtitle: 28-36px bold accent color
   - Body: 16-20px regular dark gray
   - Chart labels: 12-14px clear readable
4. Optimize spacing and layout:
   - Generous white space (40-60px margins)
   - Consistent spacing between elements (20-30px)
   - Clear visual hierarchy through size and weight
5. Design charts and visualizations:
   - Clean, minimal chart design (no clutter)
   - Clear labels and legends
   - Color-coded for easy interpretation
   - Supporting data tables below charts

**Exit Criteria**: All slides designed with consistent McKinsey-style branding, professional layout, and optimized typography.

## Phase 4: HTML Generation (Using Subagent)

**Goal**: Generate interactive HTML presentation file with all slides, styling, and functionality.

**Prerequisites**:
- Phase 2 completed with structured slide plan
- Phase 3 design system applied
- All content and visualizations ready

**Approach**: Use the `Task` tool with subagent to generate complete HTML presentation.

**Subagent Specification**:
- **Type**: `general-purpose`
- **Task**: Generate complete McKinsey-style HTML presentation
- **Input**: Structured slide plan from Phase 2
- **Output**: Single-file, self-contained HTML presentation

**Prompt Template**:
```python
Task(
    subagent_type="general-purpose",
    description="Generate HTML presentation",
    prompt=f"""You are an expert HTML/CSS/JavaScript developer specializing in McKinsey-style presentations.

SLIDE PLAN:
{slide_plan_json}

DESIGN SYSTEM:
Color Palette:
- Primary Background: #FFFFFF
- Header Background: #000000
- Primary Accent: #F85d42
- Secondary Accent: #74788d
- Deep Blue: #556EE6
- Green: #34c38f
- Blue: #50a5f1
- Yellow: #f1b44c

Typography:
- Title: 48-64px bold black
- Subtitle: 28-36px bold accent color
- Body: 16-20px regular dark gray
- Chart labels: 12-14px clear readable

YOUR TASK:
Generate a complete, single-file HTML presentation with:

1. HTML Structure:
   - DOCTYPE, html, head, body tags
   - Navigation bar (prev/next buttons, slide counter)
   - Slide containers for each slide from plan
   - Fullscreen toggle button

2. Inline CSS (McKinsey-style):
   - Color variables (:root)
   - Global styles (reset, body, fonts)
   - Navigation bar styling
   - Slide layout and transitions
   - Title slide styling
   - Header bar styling
   - Content layouts (two-column, full-width, etc.)
   - Chart containers
   - Conclusions grid
   - Responsive breakpoints (1200px, 768px)
   - Scrollbar styling
   - Conceptual visualization styles (pyramid, progression, emphasis, cycle, comparison, framework)

3. JavaScript Functionality:
   - Slide navigation (arrow keys, space, click)
   - Keyboard event handlers
   - Fullscreen toggle
   - Slide counter updates
   - Chart.js configurations for data slides
   - Smooth transitions

4. Chart.js Integration:
   - Load from CDN: https://cdn.jsdelivr.net/npm/chart.js
   - Configure each chart based on slide plan
   - Use color palette for chart colors
   - Enable tooltips and legends
   - Responsive sizing

5. Slide Content (CRITICAL):
   - Render EXACT text from slide plan
   - Preserve ALL conclusions word-for-word
   - Use exact data points for charts
   - Apply specified layouts

CHART CONFIGURATION GUIDE:
- bar: Basic bar chart
- line: Line chart for trends
- pie/doughnut: Part-to-whole (≤5 items doughnut, ≤8 pie)
- radar: Multi-dimensional comparison
- polarArea: Rankings, cyclical data
- bubble: Three dimensions (x, y, size)
- scatter: Strategic positioning

CONCEPTUAL VISUALIZATION HTML:
- pyramid: Stacked centered divs with decreasing width
- progression: Numbered steps with arrows
- emphasis: Highlighted boxes with icons
- cycle: Circular nodes around center
- comparison: Two-column before/after layout
- framework: Grid of numbered items

OUTPUT FORMAT:
Return ONLY the complete HTML file content as a code block. The HTML must:
- Be self-contained (inline CSS, inline JS)
- Work immediately when opened in browser
- Have no external dependencies except Chart.js CDN
- Include ALL slides from the plan
- Preserve ALL original content exactly

TECHNICAL REQUIREMENTS:
- Use semantic HTML5
- CSS in <style> tag in head
- JS in <script> tag at end of body
- Chart.js loaded from CDN in head
- Responsive design with media queries
- Smooth CSS transitions for slide changes
- Accessible (ARIA labels where appropriate)
"""
)
```

**Checklist**:
- [ ] Subagent invoked with slide plan and design system
- [ ] HTML structure generated with all slides
- [ ] McKinsey-style CSS applied inline
- [ ] JavaScript interactivity implemented
- [ ] Chart.js configurations included
- [ ] All original content preserved exactly
- [ ] Single-file, self-contained output received

**Exit Criteria**: Complete HTML presentation file generated, ready to open in browser, with all slides, styling, and interactivity working correctly.

**Deliverable**: Single-file HTML presentation code block that can be saved directly as `.html` file and opened in any modern browser.

## Interactive Features

### Navigation
- **Buttons**: Previous/Next buttons in navbar
- **Keyboard**: Arrow keys (←/→), Space (next), Escape (exit fullscreen)
- **Slide counter**: Shows current position (e.g., "Slide 3 of 7")

### Full-Screen Mode
- Toggle button (⛶) in bottom-right corner
- Escape key to exit

### Chart Visualizations - Enhanced Smart Selection System

**Multi-Dimensional Detection Algorithm** (v4 - 3-layer analysis):
- **Layer 1: Semantic Analysis** (Apache Superset pattern) - Field type detection (temporal, categorical, geographic, hierarchical, financial, performance)
- **Layer 2: Structure Inference** (variant-agents pattern) - Data format analysis (XY, XYZ, ranges, matrix, flow, progress, coordinates)
- **Layer 3: Rule-Based Decision Tree** (OpenObserve pattern) - 7-priority logic combining both layers

**Available Chart Types** (50+ professional visualizations):

**Basic Charts:**
- **Bar Chart** (柱状图) - Category comparisons
- **Horizontal Bar** (条形图/横向条形图) - Long category names
- **Line Chart** (折线图/线形图) - Trends over time
- **Pie Chart** (饼图) - Part-to-whole relationships (≤5 items)
- **Doughnut Chart** (环形图) - Part-to-whole with center focus

**Advanced Charts:**
- **Progress Ring** (进度环) - Completion status
- **Gauge/Speedometer** (仪表盘) - KPI metrics
- **Radar/Spider Chart** (雷达图/蛛网图) - Multi-dimensional comparison
- **Funnel Chart** (漏斗图) - Process stages/conversion
- **Gantt Chart** (甘特图/横向时间轴) - Project timelines
- **Heatmap** (热点矩阵/热力图) - Density/intensity distribution
- **Rose/Polar Area** (玫瑰图) - Cyclic data patterns
- **Nightingale Rose** - Magnitude with direction
- **Pyramid Chart** (金字塔图) - Hierarchical levels
- **Sankey Diagram** (桑基图) - Flow/movement between stages
- **Candlestick** (烛台图) - Financial/stock data
- **Bullet Chart** (子弹图) - Target vs actual with KPI
- **Step Chart** (阶梯图) - Discrete time changes
- **Box Plot** (箱型图) - Distribution and outliers
- **Waterfall Chart** (瀑布图) - Sequential additions/subtractions
- **Bubble Chart** (气泡图) - Three dimensions (x, y, size)
- **Polar Arc Length** (极坐标弧长图) - Cyclical time patterns

**Advanced Business Charts (New - Enhanced Detection):**
- **Heatmap** (热点矩阵/热力图) - 2D data intensity - ✅ IMPLEMENTED
- **Box Plot** (箱型图) - Distribution and outliers - ✅ IMPLEMENTED
- **Gantt Chart** (甘特图/横向时间轴) - Project timelines - ✅ IMPLEMENTED
- **Waterfall Chart** (瀑布图) - Sequential additions/subtractions - ✅ IMPLEMENTED
- **Sankey Diagram** (桑基图) - Flow between stages - ✅ IMPLEMENTED
- **BCG Matrix** (波士顿矩阵) - Market share vs growth - ✅ IMPLEMENTED

**Specialized Business Charts (Legacy):**
- **Diverging Bar** (差异箭头图) - Positive/negative changes
- **Pareto Chart** (帕累托图) - 80/20 rule analysis
- **Label-between-Columns** (麦肯锡标签法柱形) - Column comparison with labels
- **Slopegraph** (斜率图) - Change between two time points
- **Matrix Bubble** (矩阵气泡图) - Positional + size data
- **Marimekko** (马赛克图) - Market share composition
- **Waffle Chart** (华夫图) - Part-to-whole with grid
- **Butterfly/Tornado** (蝴蝶图) - Diverging comparison
- **Dot Plot** (滑珠图) - Distribution along axis
- **GE-McKinsey Matrix** (九宫格) - Industry attractiveness vs business strength
- **Ansoff Matrix** (安索夫增长矩阵) - Growth strategy options
- **Strategy Roadmap** (战略路线图) - Strategic initiatives timeline
- **Brand Funnel** (品牌漏斗) - Brand metrics stages
- **Market Funnel** (市场漏斗) - Market conversion stages
- **Competitive Quadrant** (竞争四象限) - Competitive positioning
- **Perceptual Map** (感知定位图) - Brand/product perception
- **Swimlane Diagram** (泳道图) - Process responsibilities
- **Value Stream Map** (价值流程图) - Process value-add analysis
- **Price Sensitivity** (价格敏感度) - Demand vs price
- **Kano Model** (Kano模型图) - Feature satisfaction
- **Monte Carlo Cloud** (蒙特卡洛云) - Probability distribution

**Conceptual Charts** (No numerical data required):
- **Emphasis Box** (强调框) - Highlight key points with visual prominence
- **Progression/Process Flow** (递进图) - Sequential steps or phases
- **Pyramid** (金字塔) - Hierarchical structure (3-5 levels)
- **Inverted Pyramid** (倒金字塔) - Priority/funnel structure
- **Triangle** (三角形) - Three-part relationship
- **Circle/Cycle** (圆环/循环) - Cyclical process
- **Venn Diagram** (韦恩图) - Set relationships and overlaps
- **Timeline** (时间轴) - Sequential events or milestones
- **Numbered List** (编号列表) - Ordered priorities or steps
- **Callout Tree** (标注树) - Central idea with branches
- **Mind Map** (思维导图) - Ideas radiating from center
- **Relationship Diagram** (关系图) - Connections between concepts
- **Flowchart** (流程图) - Process with decision points
- **Organization Chart** (组织架构图) - Hierarchical reporting
- **Before/After** (对比图) - Comparison of two states
- **Problem/Solution** (问题/解决方案) - Issue and resolution
- **Pros/Cons** (优缺点) - Two-sided comparison
- **Why/How/What** (黄金圈法则) - Purpose-driven communication
- **5W1H** (Five Ws One H) - Who, What, Where, When, Why, How
- **STAR** (Situation, Task, Action, Result) - Achievement framework

**Smart Chart Selection Logic (Enhanced v4 - Multi-Dimensional Analysis):**

The system now uses a sophisticated **3-layer detection algorithm** combining patterns from real-world implementations (Apache Superset, OpenObserve, variant-agents):

```
Layer 1: Semantic Analysis (Apache Superset)
├─ is_temporal: Detects date, time, year, month, q1-q4, etc.
├─ is_categorical: Detects category, type, department, region
├─ is_geographic: Detects map, location, country, city
├─ is_hierarchical: Detects hierarchy, level, tier, pyramid, tree
├─ is_financial: Detects revenue, profit, margin, budget
└─ is_performance: Detects kpi, score, rating, efficiency

Layer 2: Structure Inference (variant-agents)
├─ has_xy: 2D data (x, y) → scatter plot
├─ has_xyz: 3D data (x, y, z/size) → bubble chart
├─ has_ranges: Range data (min, max, quartile) → box plot
├─ has_matrix: Matrix structure → heatmap
├─ has_flow: Flow data (source, target) → sankey
├─ has_progress: Progress data (duration, start, end) → gantt/waterfall
└─ has_coordinates: Geographic data (lat, lng) → map

Layer 3: Rule-Based Decision Tree (OpenObserve)
├─ Priority 1: Matrix/Flow/3D → heatmap/sankey/bubble
├─ Priority 2: Strategy keywords + share/growth → BCG matrix
├─ Priority 3: Hierarchical → pyramid/treemap (≤5 vs >5 items)
├─ Priority 4: Temporal → step/polarArea/line
├─ Priority 5: Categorical (≤5 small %) → doughnut, (≤8 %) → pie, else → bar
├─ Priority 6: Multi-dim (3-8 items) → radar
└─ Priority 7: Geographic/Fallback → map/bar

New Detection Capabilities (Beyond Original 15 Patterns):
✓ Heatmap detection (matrix structure)
✓ Gantt chart detection (progress data)
✓ Waterfall chart detection (sequential changes)
✓ Sankey diagram detection (flow data)
✓ BCG Matrix detection (market share + growth)
✓ Box plot detection (range data)
✓ Treemap detection (large hierarchies)
✓ Violin plot detection (distribution density)
```

**Enhanced Visual Design (Phase 3):**
- **Animations**: Entry-up, entry-left, pulse effects on hover
- **Typography**: Improved line-height, letter-spacing, font hierarchy
- **Colorblind Palettes**: Viridis, Plasma, Cividis options
- **Tooltips**: Backdrop blur, custom shadows, better typography

**Responsive Design (Phase 6):**
- **4 Breakpoints**: Mobile (<480px), Tablet (768-1024px), Desktop (>1024px), Ultra-wide (>1600px)
- **Adaptive Layouts**: Horizontal bars on mobile, hidden legends on small screens
- **Chart Options**: Auto-scaling per screen width, adjusted fonts

**Accessibility (Phase 4):**
- **ARIA Labels**: Role="img", aria-describedby, aria-label on all canvas elements
- **Screen Reader Tables**: Fallback data tables for all charts
- **Keyboard Navigation**: Arrow keys, Home/End, Enter/Space for data point selection
- **Colorblind Support**: Redundant encoding (color + patterns)
- **WCAG 2.2 AA**: 4.5:1 contrast, 3:1 large text

**Performance (Phase 5):**
- **Lazy Loading**: Intersection Observer with 50px root margin
- **Debounced Resize**: 100ms delay for resize events
- **Data Aggregation**: Large datasets reduced to ~1K points
- **Animation Control**: Disabled for initial render

**Implementation**:
- `generator_v3.py`: Contains all enhanced detection and rendering methods
- Detection Method: `_determine_chart_type_v4()` (multi-dimensional analysis)
- Backward Compat: Original `_determine_chart_type()` preserved
- New Methods: `_render_bcg_matrix()`, `_render_gantt_chart()`, `_render_waterfall_chart()`, `_render_sankey_diagram()`, `_render_heatmap()`

---

## 📊 SUMMARY OF ENHANCEMENTS

**Completed Phases:**
1. ✅ **Phase 1**: Enhanced Chart Type Detection (3-layer analysis)
2. ✅ **Phase 2**: Advanced Business Charts (5 new types)
3. ✅ **Phase 3**: Visual Design Optimization (animations, typography, colorblind palettes)
4. ✅ **Phase 4**: Accessibility Features (ARIA, keyboard navigation)
5. ✅ **Phase 5**: Performance Optimizations (lazy loading, debouncing)
6. ✅ **Phase 6**: Responsive Design (4 breakpoints)
7. ✅ **Phase 7**: Testing Infrastructure (comprehensive test suite)

**Total Improvements:**
- Chart Types: 14 → 19 (+36% increase)
- Detection Dimensions: 1 → 3 (semantic + structural + rules, +200% improvement)
- New Chart Methods: 5 advanced business charts
- Enhanced CSS: +450 lines (animations, accessibility, performance, responsive)
- Test Suite: 8 test functions covering all detection layers
- Documentation: Updated SKILL.md with complete feature set

**Next Steps:**
- Generate comprehensive test presentations with all 19 chart types
- Visual verification of all new charts
- Final performance benchmarking

```
看"排名" → 玉玦图、金字塔图
  Use: Rankings, hierarchy levels, tiered data
  Examples: Market share ranking, performance tiers, priority levels

看"流向" → 桑基图、瀑布图
  Use: Flow between stages, sequential changes
  Examples: Customer journey, cash flow, conversion funnel

看"分布" → 箱型图、玫瑰图、气泡图
  Use: Distribution patterns, outliers, spread
  Examples: Test scores, customer age distribution, product categories

看"时间周期" → 极坐标弧长图、阶梯图
  Use: Cyclical patterns, discrete time changes
  Examples: Seasonal sales, quarterly results, year-over-year

看"KPI达标" → 子弹图、差异箭头图
  Use: Target vs actual, performance indicators
  Examples: Sales targets, budget variance, OKR progress

看"多维度比较" → 雷达图、矩阵气泡图
  Use: Multiple metrics comparison
  Examples: Product features, skill assessment, competitor analysis

看"占比关系" → 饼图、环形图、华夫图
  Use: Part-to-whole, composition
  Examples: Market share, budget breakdown, product mix (≤5 items)

看"趋势变化" → 折线图、面积图
  Use: Trends over time, continuous data
  Examples: Revenue growth, user acquisition, stock prices

看"横向对比" → 条形图、蝴蝶图
  Use: Category comparison with long labels
  Examples: Survey results, regional comparison, product features

看"战略分析" → BCG矩阵、GE-McKinsey九宫格、安索夫矩阵
  Use: Strategic positioning, portfolio analysis
  Examples: Product portfolio, market strategy, investment decisions

看"流程关系" → 泳道图、价值流程图、桑基图
  Use: Process flows, responsibilities, value-add
  Examples: Order processing, customer journey, manufacturing

看"概率/风险" → 蒙特卡洛云、箱型图
  Use: Uncertainty, risk analysis, probability
  Examples: Financial forecasting, project estimates, scenario analysis

看"层级" → 金字塔图、组织架构图
  Use: Hierarchical levels, top-down structure
  Examples: Organization structure, priority levels, Maslow's hierarchy

看"递进" → 递进图、流程图、时间轴
  Use: Sequential steps, phases, progression
  Examples: Project phases, journey maps, implementation steps

看"强调" → 强调框、对比图、问题/解决方案
  Use: Highlight key points, important messages
  Examples: Key takeaways, critical insights, call-to-action

看"循环" → 圆环/循环图、韦恩图
  Use: Cyclical process, continuous improvement
  Examples: Feedback loops, product lifecycle, PDCA

看"关系" → 关系图、韦恩图、思维导图
  Use: Connections between concepts, dependencies
  Examples: Stakeholder mapping, system relationships, concept links

看"对比" → 对比图、优缺点、Before/After
  Use: Two-sided comparison, before/after state
  Examples: Pros and cons, alternative comparison, improvement results

看"框架" → 黄金圈法则、5W1H、STAR
  Use: Structured communication frameworks
  Examples: Strategic messaging, project reporting, interview preparation
```

**Implementation:**
- Chart.js library (loaded from CDN: `https://cdn.jsdelivr.net/npm/chart.js`)
- Automatic chart type detection based on data characteristics
- Interactive tooltips on hover
- Responsive sizing with max-height constraints
- Fallback to bar chart for unsupported visualization types

## File Structure

The generator (`scripts/generator_v3.py`) creates:
```
presentation.html (single file)
├── CSS (inline, McKinsey-style, ~540 lines)
├── HTML (all slides)
└── JavaScript (inline)
    ├── Navigation logic
    ├── Keyboard handlers
    ├── Fullscreen toggle
    └── Chart.js configurations
```

## NEVER Do These

- **NEVER modify original content or conclusions**: The presentation must preserve all original meaning, data, and conclusions exactly
- **NEVER add fabricated data**: Only use data from the source document
- **NEVER use AI-generated placeholder text**: Use actual content from source
- **NEVER deviate from color scheme**: Strict adherence to the specified McKinsey-style palette
- **NEVER use inconsistent typography**: Maintain hierarchy and style across all slides
- **NEVER overcrowd slides**: Use generous white space and focus on key messages
- **NEVER use generic clipart or icons**: Maintain professional, business-appropriate visuals
- **NEVER sacrifice clarity for style**: Ensure data and conclusions are easily understood

## Resources

- **Phase details**: See [references/phases.md](references/phases.md)
- **Parsing guidelines**: See [references/parsing-guidelines.md](references/parsing-guidelines.md)
- **Best practices**: See [references/best-practices.md](references/best-practices.md)
- **Design templates**: See [assets/template.html](assets/template.html) and [assets/styles.css](assets/styles.css)
- **Chart examples**: See [assets/chart-examples.html](assets/chart-examples.html)
- **Example output**: See [presentation_demo/presentation_output.html](../../presentation_demo/presentation_output.html)

## Quick Start

This skill uses AI-powered subagents to generate presentations - no Python scripts required!

**Workflow**:

1. **Parse Document** (Phase 1)
   - Read and understand source document structure
   - Extract sections, data points, and conclusions
   - See [`references/parsing-guidelines.md`](references/parsing-guidelines.md)

2. **Plan Slides** (Phase 2) - Uses Subagent
   - Invoke `Task` tool with `general-purpose` subagent
   - Subagent analyzes content and creates structured slide plan
   - Assigns smart chart types and conceptual visualizations
   - Output: JSON slide plan with all slide specifications

3. **Apply Design** (Phase 3)
   - McKinsey-style design system applied automatically
   - Color palette, typography, layouts predefined
   - See Design System section above

4. **Generate HTML** (Phase 4) - Uses Subagent
   - Invoke `Task` tool with `general-purpose` subagent
   - Subagent generates complete HTML presentation
   - Includes inline CSS, JavaScript, and Chart.js integration
   - Output: Single-file, self-contained HTML presentation

**Example Usage**:
```
User: "Generate a McKinsey-style presentation from this document"

[Follow Phase 1-4 workflow using subagents]
→ Complete HTML presentation file
```

**Key Benefits**:
- ✅ No Python dependencies
- ✅ AI-powered slide planning
- ✅ Smart chart selection
- ✅ Flexible content handling
- ✅ Professional McKinsey-style design

## Complete Workflow Example

This example shows the complete end-to-end process using subagents.

### Step 1: Parse Source Document

Read the source document and extract structure:

```
Input: report.md, analysis.txt, or any structured document

Process:
1. Read document completely
2. Identify structure (headings, sections, lists)
3. Extract data points and numerical information
4. Identify conclusions and recommendations
5. Map content hierarchy

Output: Parsed content structure with:
- Document title
- Sections with content
- Data points (label, value, unit, category)
- Conclusions and recommendations
```

### Step 2: Plan Slides Using Subagent

Invoke the Task tool to create a structured slide plan:

```python
Task(
    subagent_type="general-purpose",
    description="Plan presentation slides from document",
    prompt="""You are a presentation planning specialist.

DOCUMENT CONTENT:
[Insert parsed document content here]

Create a slide plan following this structure:
1. Title slide (always first)
2. Executive summary (if conclusions exist)
3. Data visualization slides (for numerical data)
4. Conceptual slides (for frameworks/processes)
5. Content slides (for detailed information)
6. Conclusions slide (if recommendations exist)

For each slide, specify:
- slide_type: TITLE, EXECUTIVE_SUMMARY, DATA_VISUALIZATION, CONCEPTUAL, CONTENT, or CONCLUSIONS
- title: Clear heading
- content: Key points (preserve exact wording)
- key_points: Array of main points
- chart_type: (for DATA_VISUALIZATION) bar, line, pie, doughnut, radar, polarArea, bubble, scatter
- conceptual_type: (for CONCEPTUAL) pyramid, progression, emphasis, cycle, comparison, framework
- layout: title-center, bullet-points, two-column, full-width, conclusions-grid

SMART CHART SELECTION:
- Rankings/Hierarchy → polarArea, bar
- Flow/Journey → line
- Distribution → bubble, polarArea
- Time/Cyclical → line, polarArea
- KPI/Target → bar
- Multi-dimensional → radar
- Proportions (≤5 items) → doughnut, (≤8) → pie
- Trends → line
- Comparison → bar

Return JSON format:
{
  "title": "Presentation Title",
  "total_slides": N,
  "slides": [
    {
      "slide_number": 1,
      "slide_type": "TITLE",
      "title": "...",
      "content": "...",
      "key_points": ["..."],
      "layout": "title-center"
    }
  ]
}

CRITICAL: Preserve ALL original conclusions exactly. Do NOT fabricate data."""
)
```

**Expected Output from Subagent**:
```json
{
  "title": "Q4 2024 Financial Analysis",
  "total_slides": 7,
  "slides": [
    {
      "slide_number": 1,
      "slide_type": "TITLE",
      "title": "Q4 2024 Financial Analysis",
      "content": "Financial Performance Review",
      "layout": "title-center"
    },
    {
      "slide_number": 2,
      "slide_type": "EXECUTIVE_SUMMARY",
      "title": "Executive Summary",
      "content": "Key findings and insights",
      "key_points": [
        "Revenue increased by 23% YoY",
        "Operating margin improved to 18.5%",
        "New customer acquisition up 40%"
      ],
      "layout": "bullet-points"
    },
    {
      "slide_number": 3,
      "slide_type": "DATA_VISUALIZATION",
      "title": "Revenue Growth by Quarter",
      "content": "Quarterly revenue performance analysis",
      "key_points": [
        "Q4 showed strongest growth",
        "Enterprise segment led performance",
        "APAC region fastest growing"
      ],
      "chart_type": "line",
      "data_points": [
        {"label": "Q1", "value": 12.5, "unit": "M"},
        {"label": "Q2", "value": 14.2, "unit": "M"},
        {"label": "Q3", "value": 15.8, "unit": "M"},
        {"label": "Q4", "value": 18.3, "unit": "M"}
      ],
      "layout": "two-column"
    }
  ]
}
```

### Step 3: Generate HTML Using Subagent

Invoke the Task tool to generate the complete HTML presentation:

```python
Task(
    subagent_type="general-purpose",
    description="Generate McKinsey-style HTML presentation",
    prompt=f"""You are an expert HTML/CSS/JavaScript developer.

SLIDE PLAN:
[Insert JSON slide plan from Step 2 here]

DESIGN SYSTEM:
Colors:
- Background: #FFFFFF
- Header: #000000
- Primary Accent: #F85d42
- Secondary: #74788d
- Deep Blue: #556EE6
- Green: #34c38f
- Blue: #50a5f1
- Yellow: #f1b44c

Typography:
- Title: 64px bold black
- Subtitle: 36px bold accent
- Body: 18px regular dark gray

Generate a complete, single-file HTML presentation with:
1. DOCTYPE, html, head, body structure
2. Navigation bar (prev/next, slide counter)
3. All slides from the plan
4. Inline McKinsey-style CSS
5. JavaScript for navigation and Chart.js
6. Chart.js from CDN: https://cdn.jsdelivr.net/npm/chart.js
7. Fullscreen toggle button
8. Responsive design (breakpoints at 1200px, 768px)
9. Smooth transitions

CRITICAL:
- Render EXACT text from slide plan
- Preserve ALL conclusions word-for-word
- Use exact data points for charts
- Apply specified layouts

Return ONLY the complete HTML file content."""
)
```

**Expected Output from Subagent**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q4 2024 Financial Analysis</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* McKinsey-style CSS */
        :root {
            --primary-bg: #FFFFFF;
            --header-bg: #000000;
            --primary-accent: #F85d42;
            /* ... complete CSS ... */
        }
        /* ... rest of styling ... */
    </style>
</head>
<body>
    <nav class="navbar">
        <button class="nav-btn" id="prevBtn">← Previous</button>
        <span class="slide-counter">Slide <span id="currentSlide">1</span> of <span id="totalSlides">7</span></span>
        <button class="nav-btn" id="nextBtn">Next →</button>
    </nav>

    <div class="presentation-container">
        <div class="slide active" data-slide="1">
            <!-- Title slide content -->
        </div>
        <div class="slide" data-slide="2">
            <!-- Executive summary content -->
        </div>
        <!-- ... more slides ... -->
    </div>

    <button class="fullscreen-btn" onclick="toggleFullscreen()">⛶ Fullscreen</button>

    <script>
        // Navigation and Chart.js configurations
        // ... complete JavaScript ...
    </script>
</body>
</html>
```

### Step 4: Save and View

1. Save the HTML output to a file (e.g., `presentation.html`)
2. Open in any modern browser
3. Use arrow keys or buttons to navigate
4. Press fullscreen button for presentation mode

## Tips for Best Results

**When Planning Slides (Phase 2)**:
- Provide complete document context to subagent
- Specify if certain sections should be emphasized
- Mention if data has seasonal/cyclical patterns
- Note any specific visualizations requested

**When Generating HTML (Phase 4)**:
- Verify slide plan is complete and accurate
- Check that all conclusions are preserved
- Ensure data points are correctly formatted
- Test in browser before final delivery

**Common Adjustments**:
- Too many slides? Ask subagent to consolidate
- Wrong chart type? Specify data characteristics
- Missing insights? Ensure source document has clear conclusions
- Layout issues? Specify alternative layout in slide plan

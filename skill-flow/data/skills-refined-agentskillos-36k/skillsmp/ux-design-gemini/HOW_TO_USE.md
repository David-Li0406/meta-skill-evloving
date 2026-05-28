# How to Use ux-design-gemini Skill

This guide explains when and how to use the `ux-design-gemini` skill for UX design tasks using memex-cli with Google Gemini backend.

---

## When to Use This Skill

Use `ux-design-gemini` when you need to:

1. **Generate user flows and wireframes**
   - User journey maps
   - Task flow diagrams
   - Wireframe specifications

2. **Create UI component specifications**
   - Design system documentation
   - Component library specs
   - Style guides

3. **Design interaction patterns**
   - Micro-interactions
   - Animation specifications
   - Gesture-based interactions

4. **Build design system documentation**
   - Color palettes
   - Typography systems
   - Spacing and grid systems

5. **Produce responsive layout guides**
   - Mobile-first designs
   - Breakpoint strategies
   - Adaptive component behavior

6. **Analyze and critique designs**
   - Heuristic evaluations
   - Accessibility audits
   - Competitive analysis

---

## Gemini vs Other Backends

Understanding when to use Gemini versus other AI backends:

| Task Type | Best Backend | Reason |
|-----------|--------------|--------|
| **UX Design** | Gemini | Structured output, multimodal analysis |
| **Design Critique** | Gemini | Image analysis for visual feedback |
| **Code Generation** | Codex | Optimized for programming |
| **Complex Reasoning** | Claude | Architecture decisions, planning |

**Gemini's Strengths:**
- ✅ Excellent at structured output (Markdown tables, lists)
- ✅ Multimodal capabilities (analyze design screenshots)
- ✅ Fast generation for documentation
- ✅ Cost-effective for text-heavy tasks

**When to use other backends:**
- **Codex**: Frontend implementation (React, Vue components)
- **Claude**: Complex system architecture, strategic design decisions
- **Multi-backend workflows**: Design (Gemini) → Implementation (Codex)

---

## Quick Start for Designers

### Step 1: Install memex-cli

```bash
npm install -g memex-cli
```

### Step 2: Choose Your Design Stage

Refer to the [design workflow guide](references/design-workflow.md) or use this quick table:

| Stage | Task Type | Example |
|-------|-----------|---------|
| **Research** | User personas, journey maps | [User Research](examples/user-research.md) |
| **Define** | Information architecture, site maps | [Information Architecture](examples/information-architecture.md) |
| **Ideate** | User flows, concept sketches | See SKILL.md examples |
| **Prototype** | Wireframes, mockups, design systems | [Wireframes & Mockups](examples/wireframes-mockups.md) |
| **Test** | Design reviews, accessibility audits | [Design Review](examples/design-review.md) |

### Step 3: Run Design Task

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: my-design-task
backend: gemini
workdir: /path/to/project
---CONTENT---
[Your design task description in natural language]
---END---
EOF
```

**Example:**

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: user-flow
backend: gemini
workdir: ./design
---CONTENT---
为电商App设计用户购物流程，包含浏览、加购、结算、支付阶段
---END---
EOF
```

---

## Gemini Multimodal Capabilities

Gemini's unique strength is analyzing images for design critique.

### Upload Design Screenshots

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: design-review
backend: gemini
files: ./mockup.png
files-mode: embed        # Required for image analysis
workdir: ./project
---CONTENT---
审查这个设计稿：
1. 视觉层次是否清晰
2. 色彩对比度是否符合WCAG AA标准
3. 组件布局是否合理
---END---
EOF
```

**Supported formats:**
- PNG, JPG, WEBP (< 5MB recommended)
- Multiple images (comma-separated)

**Use cases:**
- Design critique and feedback
- Competitive analysis (screenshot comparison)
- Accessibility audit (color contrast check)
- Design system compliance verification

See [multimodal tips guide](references/multimodal-tips.md) for advanced techniques.

---

## Integration with Design Tools

### Figma Workflow

**Export from Figma:**
1. Select frames to review
2. Export as PNG (2x resolution)
3. Upload to Gemini for analysis

**Use Gemini for:**
- Generating component specifications from mockups
- Creating design system documentation
- Accessibility audit before development

### Sketch/Adobe XD Workflow

Similar to Figma:
- Export artboards as PNG
- Use Gemini to analyze layouts
- Generate handoff documentation

### Collaborative Design

```bash
# Step 1: Designer exports mockup
# Step 2: Use Gemini to generate specs
memex-cli run --stdin <<'EOF'
---TASK---
id: component-specs
backend: gemini
files: ./button-variants.png
files-mode: embed
---CONTENT---
生成按钮组件规格文档：
- 变体（主按钮、次要按钮、文字按钮）
- 状态（默认、悬停、按下、禁用）
- 尺寸（颜色HEX、字体大小、padding）
---END---
EOF
```

---

## Workflow Recommendations

### Pattern 1: Single Task Design

Quick, one-off design tasks.

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: wireframe
backend: gemini
---CONTENT---
创建登录页面线框图规格
---END---
EOF
```

**Duration:** 5-10 minutes
**Best for:** Individual page designs, component specs

---

### Pattern 2: Sequential Design Workflow

Multi-stage process with dependencies.

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: research
backend: gemini
---CONTENT---
用户研究：分析目标用户需求
---END---

---TASK---
id: architecture
backend: gemini
dependencies: research
---CONTENT---
基于用户研究，设计信息架构
---END---

---TASK---
id: wireframe
backend: gemini
dependencies: architecture
---CONTENT---
根据信息架构，创建关键页面线框图
---END---
EOF
```

**Duration:** 30-60 minutes
**Best for:** Complete feature design, new product workflows

See [design workflow guide](references/design-workflow.md) for detailed process.

---

### Pattern 3: Parallel Page Design

Design multiple pages simultaneously after IA is defined.

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: ia
backend: gemini
---CONTENT---
设计站点地图和导航结构
---END---

---TASK---
id: home-page
backend: gemini
dependencies: ia
---CONTENT---
首页设计规格
---END---

---TASK---
id: product-page
backend: gemini
dependencies: ia
---CONTENT---
商品详情页设计规格
---END---

---TASK---
id: checkout-page
backend: gemini
dependencies: ia
---CONTENT---
结算页设计规格
---END---
EOF
```

**Duration:** 20-40 minutes (parallel execution)
**Best for:** Multi-page design, design system creation

---

## Field Reference

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique task identifier | `wireframe-home`, `persona-creation` |
| `backend` | Always `gemini` for UX design | `gemini` |
| `workdir` | Working directory path | `./design-project`, `/home/user/designs` |

### Optional Fields

| Field | Default | Description |
|-------|---------|-------------|
| `dependencies` | - | Task IDs for sequential execution |
| `timeout` | 300 | Max execution time (seconds) |
| `files` | - | Design files to analyze (PNG, JPG) |
| `files-mode` | auto | `embed` (required for image analysis) |
| `stream-format` | text | `text` / `jsonl` |

---

## Common Design Tasks

### Create User Personas

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: personas
backend: gemini
---CONTENT---
基于访谈数据，创建3个用户画像（包含目标、痛点、使用场景）
---END---
EOF
```

### Design Information Architecture

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: sitemap
backend: gemini
---CONTENT---
为SaaS产品设计站点地图，包含3层结构
---END---
EOF
```

### Generate Wireframe Specs

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: wireframes
backend: gemini
---CONTENT---
创建移动端App首页线框图规格说明（文字描述布局和组件位置）
---END---
EOF
```

### Review Design with Image

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: design-critique
backend: gemini
files: ./mockup.png
files-mode: embed
---CONTENT---
审查设计稿的视觉层次、色彩使用、留白间距
---END---
EOF
```

### Create Design System

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: design-system
backend: gemini
---CONTENT---
创建设计系统文档：色彩、字体、间距、组件规范
---END---
EOF
```

---

## Advanced Workflows

For advanced multi-task workflows and resume functionality, refer to memex-cli documentation:

- **Sequential workflows:** [memex-cli/references/advanced-usage.md](../memex-cli/references/advanced-usage.md)
- **Parallel execution:** [memex-cli/examples/parallel-tasks.md](../memex-cli/examples/parallel-tasks.md)
- **Resume interrupted runs:** [memex-cli/examples/resume-workflow.md](../memex-cli/examples/resume-workflow.md)

These features work the same across all backends (Gemini, Claude, Codex).

---

## Tips for Effective Prompts

### 1. Be Specific

**Bad:**
```
设计一个App
```

**Good:**
```
为健身App设计用户流程：
1. 用户目标：记录每日运动
2. 包含阶段：注册、选择计划、记录运动、查看进度
3. 输出格式：Markdown流程图
```

### 2. Specify Output Format

```
要求：
- 使用Markdown表格格式
- 包含ASCII图示
- 提供具体数值（px, %, HEX颜色）
```

### 3. Provide Context

```
目标用户：25-35岁上班族
使用场景：移动端App
设计风格：现代极简
品牌色：蓝色 (#1E88E5)
```

### 4. Include Constraints

```
约束条件：
- 页面不超过3屏
- 遵循iOS Human Interface Guidelines
- 支持深色模式
```

---

## Troubleshooting

### Issue: Output too generic

**Solution:**
- Add more specific requirements
- Provide examples or reference designs
- Specify exact deliverables

### Issue: Image analysis not working

**Solution:**
- Ensure `files-mode: embed` is set
- Check file format (PNG, JPG only)
- Reduce file size (< 5MB)
- Verify file path is correct

### Issue: Output format not as expected

**Solution:**
- Explicitly request format: "使用Markdown表格"
- Provide example structure in prompt
- Request specific sections/headers

### Issue: Need multi-backend workflow

**Solution:**
Use memex-cli with multiple backends:
```bash
---TASK---
id: ux-design
backend: gemini    # Gemini for UX design
---CONTENT---
设计用户界面
---END---

---TASK---
id: implement
backend: codex     # Codex for implementation
dependencies: ux-design
---CONTENT---
实现React组件
---END---
```

---

## Further Reading

- **[SKILL.md](SKILL.md)** - Quick reference and examples
- **[references/design-principles.md](references/design-principles.md)** - UX design fundamentals
- **[references/design-workflow.md](references/design-workflow.md)** - Complete design process
- **[references/multimodal-tips.md](references/multimodal-tips.md)** - Image analysis techniques
- **[examples/](examples/)** - Detailed examples for each design stage
- **[skills/memex-cli/SKILL.md](../memex-cli/SKILL.md)** - Memex CLI full documentation

---

**Need help?** Check the examples directory for runnable design task samples matching your use case.

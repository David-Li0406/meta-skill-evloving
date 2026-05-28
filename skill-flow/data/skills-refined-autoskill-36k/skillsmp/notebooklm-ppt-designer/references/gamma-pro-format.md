# Gamma Pro 适配输出格式

当需要将设计方案转换为Gamma Pro可用的生成指令时，使用此格式。

## 输出结构

```markdown
---

## 🚀 Gamma Pro 生成指令

Create a [N]-slide presentation:

**Brand Style:**
- Background: Pure black #000000
- Primary accent: [强调色] 
- Text: White #FFFFFF, Gray #CCCCCC
- Style: Minimalist, 55-60% whitespace
- No gradients, pure flat colors only

**Slide Structure:**

Slide 1 - Title:
- Title: "[主标题]" (54pt bold white centered)
- Subtitle: "[副标题]" (24pt gray centered)
- Footer: "[左下标识]" (left) + "[右下标识]" (right accent color)

Slide 2 - "[标题]" Page "01":
- Large "01" top-left (96pt accent color with accent line above)
- Title: "[标题]" (42pt bold white)
- Content: [视觉形式英文描述]
- Key highlight in accent color

Slide 3 - "[标题]" Page "02":
[继续每一页...]

**Design Rules:**
- Page numbers: 01, 02, 03... in accent color
- One key point per slide
- Arrows (→) in accent color for transitions
- Key data highlighted in accent color
- Consistent 8px grid spacing
```

## 视觉形式英文描述模板

### 箭头流程 (Arrow Flow)
```
Three-stage horizontal flow with arrows:
[State A] → [State B] → [State C]
Progressive emphasis: gray → white → accent color
Arrow color: accent color
```

### 三列卡片 (Three-Column Cards)
```
Three equal-width cards side by side:
Card 1: [Emoji] + [Title] + [Data] + [Description]
Card 2: [Emoji] + [Title] + [Data] + [Description]
Card 3: [Emoji] + [Title] + [Data] + [Description]
Card background: dark gray, data in accent color
```

### 金字塔递进 (Pyramid)
```
Three-tier pyramid structure (bottom to top):
Base: [Level 1] - subtle border
Middle: [Level 2] - medium emphasis
Top: [Level 3] - accent color highlight
Overlapping layers, narrowing upward
```

### 竖线列表 (Vertical List)
```
Left accent line with diamond bullet points:
◆ [Point 1]: [Description]
◆ [Point 2]: [Description]
◆ [Point 3]: [Description]
Diamond bullets in accent color
```

### 居中引用 (Centered Quote)
```
Centered layout:
[Emoji]
[Small title in accent color]
────────
"[Quote text]"
Optional: accent color border box with subtle glow
```

### 大数字强调 (Data Highlight)
```
Large number centered:
[95%] in accent color (96pt)
[Description] in white (24pt)
Optional: three smaller data cards below
```

## 完整示例

```markdown
## 🚀 Gamma Pro 生成指令

Create a 9-slide presentation:

**Brand Style:**
- Background: Pure black #000000
- Primary accent: Neon green #00FF94
- Text: White #FFFFFF, Gray #CCCCCC
- Style: Minimalist, 55-60% whitespace
- No gradients, pure flat colors only

**Slide Structure:**

Slide 1 - Title:
- Title: "Vibe Coding 之道" (54pt bold white centered)
- Subtitle: "人机协作编程新范式" (24pt gray centered)
- Footer: "The Real AI Engineer" (left) + "trae.ai" (right green)

Slide 2 - "编程范式的转折" Page "01":
- Large "01" top-left (96pt green with green line above)
- Title: "编程范式的转折" (42pt bold white)
- Content: Three-stage horizontal flow with arrows showing evolution
- Key highlight: final stage in neon green

Slide 3 - "人机协作三形态" Page "02":
- Large "02" top-left (96pt green)
- Title: "人机协作的三种形态" (42pt bold white)
- Content: Three-tier pyramid (用 → 驭 → 合)
- Top tier highlighted in neon green

Slide 4 - "核心三项" Page "03":
- Large "03" top-left
- Content: Three equal-width cards with emojis
- Data numbers in neon green

[Continue for remaining slides...]

Slide 9 - "总结" Page "08":
- Centered quote layout
- Quote in white with green border box
- Call to action with green link

**Design Rules:**
- Page numbers: 01, 02, 03... in neon green
- One key point per slide
- Arrows (→) in green for transitions
- Key data highlighted in neon green
- Consistent 8px grid spacing
```

## 注意事项

1. **语言**：Gamma Pro指令使用英文
2. **简化**：相比完整设计方案，Gamma指令更简洁
3. **关键词**：使用Gamma能理解的描述词
4. **颜色**：始终指定具体的十六进制颜色值
5. **结构**：保持Slide + 描述的清晰格式

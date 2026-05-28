---
name: AI 无损 PPT 架构师
description: 接收多种格式素材，自动生成精美的可编辑 PPT，支持 WPS 完美编辑
---

# AI 无损 PPT 架构师

## 📝 Skill 概述

这是一个部署在 Antigravity 上的全自动 PPT 生成 Skill。你可以上传各种格式的素材（PDF、Word、Excel、图片等），我会：
1. 智能解析内容并生成专业的 PPT 大纲
2. 为每一页生成高质量的 AI 配图
3. 使用 Python 自动生成精美的 `.pptx` 文件
4. 确保所有元素在 WPS/PowerPoint 中完全可编辑

**关键特点**：
- ✅ 零外部依赖（无需 API Key）
- ✅ 半自动流程（大纲可用户确认修改）
- ✅ 2025 年顶级设计美学（多巴胺配色、极简排版）
- ✅ 图片生成失败自动重试
- ✅ 5 种预设精美风格

---

## 🎯 使用场景

- 快速生成产品发布会 PPT
- 将长篇报告转换为演示文稿
- 创建数据分析展示 PPT
- 生成培训/教育课件
- 制作年度总结/述职报告

---

## 📋 工作流程

### 阶段 1：接收用户需求
当用户触发此 Skill 时，我会收集以下信息：
- 上传的素材文件（PDF/Word/Excel/图片等）
- 目标页数（必须明确指定，无默认值）
- 风格选择（可选，不指定则我智能决策）：
  - 科技未来
  - 奢华商务
  - 活力创意
  - 专业沉稳
  - 自然清新
- 自定义要求（可选）

**示例触发命令**：
```
使用 AI PPT 架构师 Skill，生成 15 页的产品发布会 PPT。
风格：科技未来
素材：[用户上传的文件]
要求：重点突出 AI 技术创新
```

---

### 阶段 2：解析素材
我会使用 Python 脚本调用以下库解析文件：
- `pdfplumber`：解析 PDF
- `python-docx`：解析 Word
- `openpyxl`：解析 Excel
- `Pillow`：处理图片

**验证规则**：
- 单文件大小 ≤ 100MB
- 支持格式：`.pdf`, `.docx`, `.xlsx`, `.png`, `.jpg`, `.md`
- 如果文件不合法，我会明确提示错误来源

**输出**：统一的结构化数据
```python
{
  "text_blocks": ["段落1", "段落2", ...],
  "tables": [表格数据],
  "images": [图片路径],
  "metadata": {元信息}
}
```

---

### 阶段 3：生成 PPT 大纲
基于解析的内容和用户要求，我会生成详细的 Markdown 格式大纲。

**大纲结构**（每页包含）：
- 页面类型（封面/目录/内容页/图表页等）
- 标题
- 内容要点
- 配图 Prompt（用于后续图片生成）

**示例大纲**：
```markdown
## 第 1 页：封面（全屏图片 + 标题）
- **标题**：AI 驱动的未来
- **副标题**：2025 技术趋势报告
- **配图 Prompt**：A futuristic AI neural network visualization, electric blue and purple neon lights, dark cyberpunk style, 8k ultra detailed, cinematic lighting

## 第 2 页：目录（极简列表 + 装饰线）
- **标题**：核心议题
- **内容**：
  1. AI 发展历程 → 从图灵测试到 AGI
  2. 关键技术突破 → Transformer 与多模态
  3. 应用案例 → 医疗、金融、创意产业
  4. 未来展望 → 伦理与监管
- **配图 Prompt**：Abstract geometric shapes forming a pathway, minimalist design, gradient from deep blue to bright cyan

## 第 3 页：内容页（左侧图片 + 右侧文字）
- **标题**：Transformer 架构革命
- **内容**：
  • 2017 年 Google 提出"Attention is All You Need"
  • 自注意力机制突破性创新
  • 奠定 GPT/BERT 等模型基础
  • 推动 NLP 进入预训练时代
- **配图 Prompt**：A visualization of transformer architecture with attention mechanism, neural network nodes connected by glowing lines, dark blue background, high tech style
```

---

### 阶段 4：用户确认大纲
我会将生成的大纲展示给用户，并询问：

```
请审阅以上 PPT 大纲。如需修改，请告诉我：
- 哪一页需要调整内容？
- 需要添加或删除哪些信息？
- 是否需要调整页面顺序？

如果满意，请回复"确认"继续生成 PPT。
```

**用户可以**：
- 回复 `确认` → 我继续执行
- 回复 `修改第 3 页，增加 XXX 内容` → 我更新大纲并再次确认
- 回复 `删除第 5 页` → 我删除该页并调整页码

**循环直到用户满意**。

---

### 阶段 5：生成 AI 配图
确认大纲后，我会从每页的 `配图 Prompt` 中提取内容，并：

1. **优化 Prompt**：根据选定的风格，为每个 Prompt 添加风格关键词
   ```python
   原始 Prompt: "A data visualization background"
   
   优化后（科技未来风格）:
   "A modern abstract data visualization with flowing particles, 
    electric blue (#00E5FF) and bright red (#FF1744) color scheme, 
    dark space blue (#0A0E27) background, futuristic, neon lights, 
    cyberpunk, holographic, high contrast, 8k quality, professional"
   ```

2. **调用 `generate_image` 工具**：
   ```python
   for i, prompt in enumerate(optimized_prompts):
       print(f"[进度] 正在生成第 {i+1}/{total} 张图片...")
       image = generate_image(prompt, f"slide_{i+1}_visualization")
       # 自动保存到 ./assets/ 目录
   ```

3. **无限重试机制**：
   ```python
   while True:
       try:
           image = generate_image(prompt)
           break  # 成功则退出
       except Exception as e:
           print(f"[警告] 图片生成失败，2秒后重试: {e}")
           time.sleep(2)
   ```

4. **图片规格**：
   - 分辨率：1920x1080（16:9 标准）
   - 格式：PNG（支持透明）

---

### 阶段 6：编写 Python PPT 生成脚本
我会创建一个完整的 Python 脚本，使用 `python-pptx` 库生成 PPT。

**关键代码结构**：

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import json

# 1. 加载风格配置
with open('templates/tech_future.json', 'r', encoding='utf-8') as f:
    style = json.load(f)

# 2. 创建演示文稿
prs = Presentation()
prs.slide_width = Inches(16)   # 16:9 宽屏
prs.slide_height = Inches(9)

# 3. 生成封面页
def create_cover_slide(title, subtitle, image_path, style):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白布局
    
    # 全屏背景图
    slide.shapes.add_picture(image_path, 0, 0, 
        width=prs.slide_width, height=prs.slide_height)
    
    # 半透明遮罩
    overlay = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, 
        prs.slide_width, prs.slide_height)
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = RGBColor(0, 0, 0)
    overlay.fill.transparency = 0.4
    
    # 大标题（72pt）
    title_box = slide.shapes.add_textbox(
        Inches(1), Inches(3), Inches(14), Inches(2))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_run = title_frame.paragraphs[0].runs[0]
    title_run.font.size = Pt(72)
    title_run.font.bold = True
    title_run.font.name = style['fonts']['title_en']
    title_run.font.color.rgb = RGBColor(255, 255, 255)
    
    # （副标题代码省略...）

# 4. 生成内容页
def create_content_slide(title, points, image_path, style):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 顶部装饰线
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(0.5), Inches(0.3), Inches(3), Inches(0.05))
    line.fill.solid()
    line.fill.fore_color.rgb = hex_to_rgb(style['colors']['primary'])
    
    # 标题（48pt Bold）
    # （代码省略...）
    
    # 左侧图片 + 右侧文字布局
    if image_path:
        slide.shapes.add_picture(image_path, 
            Inches(0.5), Inches(2), Inches(6), Inches(6))
        content_left = Inches(7)
    else:
        content_left = Inches(2)
    
    # 要点内容（28pt）
    # （代码省略...）

# 5. 循环生成所有页面
for page in outline_pages:
    if page['type'] == '封面':
        create_cover_slide(page['title'], page['subtitle'], 
            page['image'], style)
    else:
        create_content_slide(page['title'], page['content'], 
            page['image'], style)

# 6. 保存文件
filename = f"{title}_{datetime.now().strftime('%Y%m%d')}.pptx"
prs.save(filename)
print(f"✅ PPT 生成完成：{filename}")
```

---

### 阶段 7：运行脚本生成 PPT
我会在终端执行脚本：

```bash
pip install python-pptx pdfplumber openpyxl python-docx Pillow tqdm
python scripts/generate_ppt.py
```

**实时进度反馈**：
```
[进度] 正在安装依赖库... (1/2)
[进度] 依赖安装完成
[进度] 正在生成第 1/15 页...
[进度] 正在生成第 2/15 页...
...
[进度] 正在生成第 15/15 页...
[进度] 正在优化文件大小...
✅ PPT 生成完成！
```

---

### 阶段 8：交付成果
我会告知用户：

```
✅ PPT 生成完成！

📄 文件名：AI驱动的未来_20260119.pptx
📏 页数：15 页
🎨 风格：科技未来
💾 大小：18.3 MB
📍 路径：[文件绝对路径]

请下载文件并在 WPS 或 PowerPoint 中打开进行二次编辑。
所有文字、图片、形状都是完全可编辑的。
```

---

## 🎨 设计标准（2025 年顶级审美）

### 1. 配色方案
我会根据风格应用以下配色：

| 风格 | 主色 | 辅助色 1 | 辅助色 2 | 背景色 |
|------|------|---------|---------|--------|
| 科技未来 | #00E5FF | #FF1744 | #FFFFFF | #0A0E27 |
| 奢华商务 | #FFD700 | #C0C0C0 | #FFFFFF | #1A1A1A |
| 活力创意 | #FF6F00 | #D500F9 | #FFEB3B | 渐变背景 |
| 专业沉稳 | #1565C0 | #FFA726 | #E0E0E0 | #FAFAFA |
| 自然清新 | #4CAF50 | #81C784 | #FFFFFF | #E8F5E9 |

### 2. 排版原则
- ✅ 极简主义：每页不超过 3 个核心信息点
- ✅ 大标题：≥ 44pt（封面 60-80pt）
- ✅ 留白率：≥ 30%
- ✅ 视觉跳跃率：标题/正文字号对比 ≥ 2:1

### 3. 字体标准
- 英文：Roboto / Montserrat / Inter
- 中文：思源黑体 / 微软雅黑 Bold
- 正文最小字号：24pt

### 4. 视觉元素
- AI 生成的抽象渐变背景
- 细线条分隔符（0.5pt）
- 圆角矩形容器
- 半透明遮罩（Alpha 0.85）

---

## ⚠️ 错误处理

### 文件解析失败
如果文件无法解析，我会明确提示：
```
❌ 文件解析失败：product.pdf
原因：PDF 已加密，请使用未加密的文件
建议：尝试在 Adobe Reader 中另存为新文件
```

### 图片生成失败
我会自动重试，直到成功：
```
[警告] 图片生成失败（尝试 1/∞）：API 超时
[警告] 2秒后重试...
[进度] 图片生成成功：slide_3.png
```

### 脚本执行错误
如果遇到代码错误，我会：
1. 显示详细错误堆栈
2. 分析原因
3. 修复代码并重新运行

---

## 📖 用户指南

### 如何触发此 Skill？
在 Antigravity 中发送类似命令：
```
使用 AI PPT 架构师 Skill，生成 [页数] 页 PPT
风格：[选择一个风格]
素材：[上传文件]
要求：[自定义说明]
```

### 选择哪个 AI 模型？
推荐使用 **Claude 4.5 Sonnet (Thinking)**：
- ✅ 编程能力最强
- ✅ 支持 `generate_image` 工具
- ✅ Thinking 模式可见规划过程

### 图片生成需要特殊设置吗？
不需要！`generate_image` 是 Antigravity 内置工具，会自动调用。

---

## 📦 依赖库

```txt
python-pptx==0.6.21
pdfplumber==0.10.3
openpyxl==3.1.2
python-docx==1.1.0
Pillow==10.1.0
tqdm==4.66.1
```

---

## 🔧 高级自定义

### 自定义配色
用户可以指定自己的配色方案：
```
主题色：#FF5722
辅助色：#673AB7
背景色：白色
```

### 混合素材输入
支持同时上传多个文件，我会自动合并内容。

### 跳过图片生成
用户可以要求"不生成图片"或"使用占位图"。

---

## ✅ 验证清单

生成 PPT 后，我会自动验证：
- [ ] 文件可以在 WPS/PowerPoint 中打开
- [ ] 所有文字可以编辑
- [ ] 所有图片可以移动/删除
- [ ] 字体、颜色符合风格配置
- [ ] 页数符合用户要求

---

## 🎯 期望值设定

**可以达到**：
- ✅ 8-9 分的专业 PPT
- ✅ 清晰、现代、视觉和谐
- ✅ 节省 80% 制作时间

**需要用户二次精修**：
- ⚠️ 微妙的间距调整
- ⚠️ 个别文字措辞优化
- ⚠️ 特殊创意图形组合

**定位**：80% AI 自动生成 + 20% 用户精修 = 完美成品

---

## 📞 支持

如遇问题，请在对话中告诉我：
- 文件解析失败 → 我会诊断文件问题
- 图片生成太慢 → 可以跳过图片
- PPT 在 WPS 中显示异常 → 我会检查兼容性

---

**准备好开始了吗？上传你的素材，告诉我页数和风格，让我为你生成惊艳的 PPT！** 🚀

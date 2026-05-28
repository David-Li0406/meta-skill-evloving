# HTML Presentation Beautifier - 快速使用指南

## 🚀 快速开始

### 推荐使用优化版本

我们提供两个版本的生成器：

1. **generator_optimized.py** ✨ **推荐**
   - 单文件输出（无需外部 CSS/JS）
   - 智能图表类型选择
   - 多彩图表配色
   - 更好的数据标签

2. **generator.py** (原版)
   - 需要外部 CSS 和 JS 文件
   - 基础图表功能

---

## 📖 使用方法

### 方式一：直接使用 Python 脚本

```bash
# 使用优化版生成器（推荐）
python3 skills/scripts/generator_optimized.py parsed_data.json output.html

# 使用原版生成器
python3 skills/scripts/generator.py parsed_data.json output.html
```

### 方式二：作为 Claude Code 技能使用

这个项目是一个 Claude Code 插件技能。当你说：
- "将这个文档转换为演示文稿"
- "美化这个 HTML 演示"
- "生成 McKinsey 风格的幻灯片"

Claude 会自动调用此技能。

---

## 📁 项目文件说明

### 核心文件

```
html-presentation-beautifier/
├── skills/
│   ├── SKILL.md                      # 技能定义文档
│   └── scripts/
│       ├── parser.py                 # 文档解析器
│       ├── generator.py              # 原版 HTML 生成器
│       └── generator_optimized.py    # ✨ 优化版 HTML 生成器（推荐）
│
├── presentation_demo/                # 原版演示（需要外部文件）
│   ├── styles.css
│   ├── script.js
│   └── presentation_output.html
│
├── parsed_data.json                  # 示例：解析后的数据
├── test_with_conclusions.md          # 示例：源文档
├── presentation_output.html          # 原版输出
└── presentation_output_optimized.html # ✨ 优化版输出（单文件）
```

---

## 🔄 完整工作流程

### 步骤 1: 准备源文档

支持的格式：
- Markdown (`.md`)
- 纯文本 (`.txt`)
- JSON (`.json`)

示例文档结构：
```markdown
# 文档标题

## 章节 1
- 数据点 1: 85%
- 数据点 2: 65元

## Conclusions
- 结论 1
- 结论 2
```

### 步骤 2: 解析文档（可选）

如果你想先查看解析结果：

```bash
python3 skills/scripts/parser.py test_with_conclusions.md
```

输出：
```
Document: 「学童优选」品牌分析报告
Type: markdown
Sections: 4
Data Points: 85
Conclusions: 24
```

### 步骤 3: 生成演示文稿

**使用优化版生成器（推荐）**：

```bash
python3 skills/scripts/generator_optimized.py \
    parsed_data.json \
    my_presentation.html
```

**使用原版生成器**：

```bash
# 需要先复制样式和脚本文件
cp presentation_demo/styles.css .
cp presentation_demo/script.js .

python3 skills/scripts/generator.py \
    parsed_data.json \
    my_presentation.html
```

### 步骤 4: 查看演示文稿

```bash
# macOS
open my_presentation.html

# Windows
start my_presentation.html

# Linux
xdg-open my_presentation.html
```

---

## 🎨 输出示例

### 优化版输出特性

**单文件结构**：
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        /* 所有 CSS 样式内联 */
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar">...</nav>

    <!-- 幻灯片内容 -->
    <div class="presentation-container">
        <div class="slide active">...</div>
        <div class="slide">...</div>
        <!-- 更多幻灯片 -->
    </div>

    <!-- 交互按钮 -->
    <button class="fullscreen-btn">...</button>

    <script>
        /* 所有 JavaScript 代码 */
        /* Chart.js 图表配置 */
    </script>
</body>
</html>
```

**生成的幻灯片类型**：
1. 标题页 - 显示文档标题和日期
2. 执行摘要 - 前 5 个关键结论
3. 数据可视化页 - 图表 + 洞察（最多 3 个）
4. 详细发现页 - 文本内容
5. 结论与建议页 - 卡片网格 + 建议列表

---

## 🎯 导航控制

### 演示文稿中的控制

**鼠标控制**：
- 点击 "← Previous" 按钮：返回上一页
- 点击 "Next →" 按钮：进入下一页
- 点击 "⛶ Fullscreen" 按钮：切换全屏模式

**键盘快捷键**：
- `→` 或 `空格键`：下一页
- `←`：上一页
- `ESC`：退出全屏

**图表交互**：
- 鼠标悬停在柱状图上查看详细数值
- 点击图例隐藏/显示数据系列

---

## 📊 支持的图表类型

优化版生成器支持三种图表类型：

| 图表类型 | 使用场景 | 自动触发条件 |
|---------|---------|-------------|
| **柱状图** (Bar) | 数据比较 | 默认使用 |
| **饼图** (Pie) | 占比分布 | ≤5 个数据点且全部为百分比 |
| **折线图** (Line) | 时间趋势 | 预留接口（待完善） |

---

## 🎨 配色方案

McKinsey/BCG 风格配色：

```
主背景:     #FFFFFF (白色)
标题栏:     #000000 (黑色)
主强调色:   #F85d42 (橙红色)
次要强调色: #74788d (灰色)
深蓝色:     #556EE6 (用于图表)
绿色:       #34c38f (成功指标)
蓝色:       #50a5f1 (中性强调)
黄色:       #f1b44c (警告/注意)
```

---

## 🔧 自定义和扩展

### 修改配色方案

编辑 `generator_optimized.py` 中的 `colors` 字典：

```python
self.colors = {
    'primary': '#F85d42',      # 主强调色
    'secondary': '#74788d',    # 次要强调色
    'deep_blue': '#556EE6',    # 深蓝色
    'green': '#34c38f',        # 绿色
    'blue': '#50a5f1',         # 蓝色
    'yellow': '#f1b44c'        # 黄色
}
```

### 修改 CSS 样式

编辑 `_get_css()` 方法中的样式定义。

### 添加新的图表类型

1. 在 `_determine_chart_type()` 中添加选择逻辑
2. 在 `_generate_chart_script()` 中添加图表配置

---

## 📚 更多文档

- **优化报告**: `OPTIMIZATION_REPORT.md` - 详细的优化说明
- **测试报告**: `TEST_REPORT.md` - 功能测试结果
- **验证报告**: `VALIDATION_REPORT.md` - 项目验证文档
- **技能文档**: `skills/SKILL.md` - 完整的技能定义

---

## ⚡ 性能指标

**优化版生成器**：
- 文件大小：约 24 KB（单文件）
- 生成时间：< 1 秒
- 内存占用：< 50 MB
- 幻灯片数量：自动生成（通常 5-10 张）
- 图表数量：最多 3 个交互式图表

---

## 🐛 故障排除

### 问题：图表不显示

**原因**：需要网络连接以加载 Chart.js CDN

**解决方案**：
- 确保设备已连接互联网
- 或者下载 Chart.js 到本地并修改 `<script src="...">`

### 问题：中文显示乱码

**原因**：文件编码问题

**解决方案**：
- 确保源文档使用 UTF-8 编码
- 生成器默认使用 UTF-8 输出

### 问题：幻灯片太多或太少

**原因**：章节和数据点数量

**解决方案**：
- 调整源文档的章节划分
- 修改生成器中的幻灯片生成逻辑

---

## 💡 最佳实践

1. **源文档准备**
   - 使用清晰的章节标题（#, ##, ###）
   - 将结论放在 "Conclusions" 或 "Recommendations" 章节
   - 数据点使用明确的单位（%, $, k, m, b）

2. **内容组织**
   - 每个章节不超过 5 个关键点
   - 数据点最好是数值型
   - 结论要简洁明确

3. **演示技巧**
   - 使用全屏模式（F11 或点击全屏按钮）
   - 利用键盘快捷键快速导航
   - 鼠标悬停图表查看详细数据

---

## 📞 支持

如有问题或建议，请参考：
- 完整文档：`skills/SKILL.md`
- 优化详情：`OPTIMIZATION_REPORT.md`
- 测试结果：`TEST_REPORT.md`

---

**最后更新**: 2026-01-20
**推荐版本**: generator_optimized.py v2.0

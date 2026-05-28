# AI 无损 PPT 架构师 Skill

## 📦 文件结构

```
.agent/skills/ai-ppt-architect/
├── SKILL.md                          # Skill 主文档（详细工作流程）
├── requirements.txt                  # Python 依赖
├── README.md                         # 本文件
├── scripts/
│   └── ppt_builder.py                # PPT 生成引擎示例脚本
├── templates/
│   ├── tech_future.json              # 科技未来风格
│   ├── luxury_business.json          # 奢华商务风格
│   ├── vibrant_creative.json         # 活力创意风格
│   ├── professional_stable.json      # 专业沉稳风格
│   └── nature_fresh.json             # 自然清新风格
└── examples/
    └── (示例输入文件和输出 PPT)
```

## 🚀 快速开始

### 1. 触发 Skill

在 Antigravity 中发送：

```
使用 AI PPT 架构师 Skill，生成 15 页的产品发布会 PPT。
风格：科技未来
素材：[上传你的文件]
要求：重点突出 AI 功能创新
```

### 2. 选择 AI 模型

推荐使用 **Claude 4.5 Sonnet (Thinking)**：
- ✅ 最强编程能力
- ✅ 支持 `generate_image` 工具
- ✅ 可见规划过程

### 3. 等待生成

AI 会自动执行以下流程：
1. 解析你的素材文件
2. 生成 PPT 大纲并请你确认
3. 生成 AI 配图（自动重试直到成功）
4. 编写并运行 Python 脚本
5. 生成 `.pptx` 文件供下载

## 🎨 风格预览

### 科技未来
- **配色**：荧光青 + 亮红 + 深空蓝背景
- **适用**：科技产品发布、技术报告
- **特点**：未来感、霓虹灯效果

### 奢华商务
- **配色**：金色 + 银色 + 纯黑背景
- **适用**：高端品牌展示、投资路演
- **特点**：高端质感、优雅大气

### 活力创意
- **配色**：鲜橙 + 荧光紫 + 渐变背景
- **适用**：创意提案、品牌活动
- **特点**：大胆鲜艳、充满活力

### 专业沉稳
- **配色**：深蓝 + 暖橙 + 白色背景
- **适用**：企业汇报、商务演示
- **特点**：简洁专业、可信赖

### 自然清新
- **配色**：草绿 + 浅绿 + 淡绿背景
- **适用**：环保主题、医疗健康
- **特点**：清新自然、舒适安心

## 📖 使用文档

详细使用说明请参阅：
- **[SKILL.md](SKILL.md)** - 完整的工作流程和技术细节
- **[usage_guide.md](../../../brain/5b8c28af-1e78-4916-969f-1fceea8b51ff/usage_guide.md)** - 使用指南（模型选择、常见问题）
- **[implementation_plan.md](../../../brain/5b8c28af-1e78-4916-969f-1fceea8b51ff/implementation_plan.md)** - 技术实现计划

## 💡 常见问题

### Q: 需要自己提供 API Key 吗？
A: **不需要**！所有功能都由 Antigravity 内置工具完成。

### Q: 图片生成需要特殊设置吗？
A: **不需要**！`generate_image` 是 Antigravity 工具，会自动调用。

### Q: 生成的 PPT 能在 WPS 中编辑吗？
A: **可以**！所有元素（文字、图片、形状）都是完全可编辑的。

### Q: 可以自定义配色吗？
A: **可以**！在触发 Skill 时指定你的主题色和辅助色即可。

### Q: 图片生成失败怎么办？
A: AI 会自动重试直到成功，无需担心。

## 🛠️ 技术栈

- **python-pptx**: PPT 文件生成
- **pdfplumber**: PDF 解析
- **openpyxl**: Excel 解析
- **python-docx**: Word 解析
- **Pillow**: 图片处理

## ⚡ 性能参考

- **15 页 PPT**：约 3-5 分钟
- **文件解析**：约 30 秒
- **大纲生成**：约 1 分钟
- **图片生成**：约 2-4 分钟（15 张）
- **PPT 生成**：约 1 分钟

## 📝 示例命令

### 基础使用
```
使用 AI PPT Skill，生成 10 页 PPT，风格：专业沉稳
```

### 自定义配色
```
使用 AI PPT Skill，生成 20 页 PPT
主题色：#FF5722
辅助色：#673AB7
要求：现代简约风格
```

### 混合素材
```
使用 AI PPT Skill，素材：
- 产品白皮书.pdf
- 数据报告.xlsx
- 品牌logo.png

生成 18 页年度总结 PPT
```

## 📞 支持

如遇问题，请在 Antigravity 对话中告诉  AI，我会：
- 诊断文件解析问题
- 调整设计方案
- 修复代码错误
- 优化生成流程

---

**准备好生成你的第一个 AI PPT 了吗？** 🚀

上传素材，选择风格，让 AI 为你完成剩下的工作！

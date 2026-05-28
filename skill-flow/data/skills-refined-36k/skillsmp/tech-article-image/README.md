# Tech Article Image 技术文章配图生成器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**一个为技术媒体人设计的 Claude Skill，让 AI 配图告别"塑料感"。**

---

## 解决什么问题？

你一定见过这种 AI 配图：发光的大脑、霓虹色的电路、悬浮的全息界面、油腻的光污染……

它们"很AI"，但不专业，更不高级。

这个 Skill 提供 **25种经过设计验证的视觉风格**，每一种都来自真实的艺术流派或设计传统——瑞士国际主义、专利说明书、华尔街日报点画、蓝晒印相、绘图仪生成艺术……

**不是随机生成，而是有章法的视觉匹配。**
<div align="center">
<img src="https://github.com/ZD-AI-Lab/Tech-Article-Illustration-Master/blob/main/assets/styles-01-rational.png" width=600 />   
<img src="https://github.com/ZD-AI-Lab/Tech-Article-Illustration-Master/blob/main/assets/styles-02-narrative.png" width=600 />
<img src="https://github.com/ZD-AI-Lab/Tech-Article-Illustration-Master/blob/main/assets/styles-03-industrial.png" width=600 />
<img src="https://github.com/ZD-AI-Lab/Tech-Article-Illustration-Master/blob/main/assets/styles-04-digital.png" width=600 />
<img src="https://github.com/ZD-AI-Lab/Tech-Article-Illustration-Master/blob/main/assets/styles-05-aesthetic.png" width=600 />
</div>
---

## 核心亮点

### 🎯 情绪-风格匹配系统

不靠猜，靠逻辑。Skill 会分析你的文章：

| 文章情绪 | 推荐风格 | 视觉效果 |
|----------|----------|----------|
| 理性分析 | 瑞士设计、等轴测蓝图 | 几何、极简、网格 |
| 硬核拆解 | 专利说明书、X光透视 | 墨线、结构、内部视图 |
| 人文叙事 | 孔版印刷、拼贴 | 颗粒感、温度、冲突 |
| 数字原生 | 故障艺术、激光雷达 | 像素、点云、虚拟空间 |
| 美学愿景 | 包豪斯、现代水墨 | 哲学、平衡、意境 |

### 🚫 内置"反AI病"机制

每个提示词自动附加负向约束：
```
No text, no watermark, no plastic texture, no lens flare, no glowing brains
```

告别塑料感、光污染、假文字、发光大脑。

### 📖 提示词透明可解释

不是黑盒输出。每次生成都附带结构解析：

| 组成部分 | 作用 |
|----------|------|
| 风格声明 | 锁定艺术流派，避免"通用科技风" |
| 核心意象 | 文章概念的视觉转译 |
| 材质/纹理 | 赋予物理质感 |
| 氛围词 | 微调情绪 |
| 负向约束 | 排除常见问题 |

你能看懂、能修改、能学会。

### 🔌 MCP 生图无缝集成

- 有 MCP 生图工具 → 自动调用 Gemini 3.0 生成
- 无 MCP → 输出中英双语提示词，可用于任意生图工具

无论什么环境都能用。

---

## 25种风格速览

**理性与精确**
瑞士设计 · 等轴测蓝图 · 专利说明书 · 绘图仪艺术 · ASCII字符画

**人文与叙事**
孔版印刷 · 科技黑色漫画 · 达芬奇手稿 · 混合媒介拼贴 · 版画

**工业力量**
粗野主义 · 华尔街日报点画 · X光透视 · 零件平铺 · 蓝晒印相

**数字原生**
1-Bit像素 · 故障艺术 · 低多边形 · 合成波 · 激光雷达点云

**美学与愿景**
热成像 · 多层纸雕 · 太阳朋克 · 包豪斯 · 现代水墨

---

## 适合谁？

- 📰 **科技媒体编辑**：快速为深度文章配专业题图
- ✍️ **技术博主**：让博客视觉风格有辨识度
- 📱 **内容运营**：公众号/社交媒体配图不再千篇一律
- 🎨 **对AI配图有追求的人**：受够了"塑料感"，想要真正的设计感

---

## 安装使用

### 方法一：直接下载（推荐）

1. 下载 [`dist/tech-article-image.zip`](dist/tech-article-image.zip)
2. 上传到 Claude Skills
3. 开始使用

### 方法二：Clone 仓库

```bash
git clone https://github.com/ZD-AI-Lab/Tech-Article-Illustration-Master.git
```

然后上传 `dist/tech-article-image.zip` 到 Claude Skills。

### 使用方式

1. 发送文章或文章摘要给 Claude
2. 说"帮我配个图"或"生成一张题图"
3. 确认风格和提示词
4. 生成图像（或复制提示词到其他生图工具）

---

## 示例输出

**输入：** 一篇关于大模型推理优化的技术文章

**Skill 输出：**

> **推荐风格：绘图仪生成艺术 (Algorithmic Plotter Art)**
> 
> **风格简介：** 模拟机械绘图仪用数学公式驱动笔尖绘制的艺术。特点是精密的细线交织、摩尔纹干涉、纯粹的黑白墨线在纸上的物理质感。常见于数学可视化和生成艺术领域。
> 
> **为什么选它：** 推理优化的本质是数学与算法的极致追求，摩尔纹的视觉张力完美契合"优化收敛"的概念。

**英文提示词：**
```
Algorithmic plotter art. Dense intersecting fine black ink lines 
forming neural network topology with flowing optimization gradients, 
creating geometric moiré patterns on textured white paper. 
Mathematical precision. No text, no plastic texture.
```

**中文提示词：**
```
算法绘图仪艺术。密集交叉的精细黑色墨线构成神经网络拓扑结构，
流动的优化梯度形成几何摩尔纹图案，绘于有纹理的白纸上。
数学的精确。无文字，无塑料质感。
```

---

## 进阶：配置直接生图

本 Skill 支持在 Claude 中直接生成图像，无需手动复制提示词。

**只需3步：**

### 1. 申请 Gemini API Key

访问 [Google AI Studio](https://aistudio.google.com/apikey)，免费申请 API Key。

### 2. 编辑 Claude 配置文件

找到配置文件位置：
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

添加以下内容（如果文件不存在就新建）：

```json
{
  "mcpServers": {
    "mcp-image": {
      "command": "npx",
      "args": ["-y", "mcp-image"],
      "env": {
        "GEMINI_API_KEY": "你的API Key",
        "IMAGE_OUTPUT_DIR": "图片保存路径，如 /Users/你的用户名/Pictures/AI-Images"
      }
    }
  }
}
```

### 3. 重启 Claude

完全退出 Claude 后重新打开，在 Connectors 里看到 `mcp-image` 已启用即配置成功。

---

**说明：**
- `mcp-image` 是一个开源 npm 包，基于 Gemini 3.0 生图
- 首次使用会自动下载，无需手动安装
- 生成的图片保存在 `IMAGE_OUTPUT_DIR` 指定的目录

---

## 仓库结构

```
tech-article-image/
├── README.md                   # 本说明文档
├── LICENSE                     # MIT 开源协议
├── SKILL.md                    # Skill 主文件
├── references/
│   └── styles.md               # 25种风格详细参考
├── assets/
│   └── styles-*.png            # 5组风格示例图
└── dist/
    └── tech-article-image.zip  # 👈 直接下载上传到Claude即可
```

---

## 开源协议

MIT License. 

欢迎 Fork、修改、商用。

如果觉得有用，欢迎 Star ⭐

---

## 致谢

本项目推荐使用的图像生成工具 [mcp-image](https://github.com/shinpr/mcp-image) 由 **shinpr** 开发，基于 MIT 协议开源。感谢作者的贡献！

---

**作者：** 高飞 / Gao Fei（至顶科技 / Tech Walker）  
**微博：** https://weibo.com/gaofei

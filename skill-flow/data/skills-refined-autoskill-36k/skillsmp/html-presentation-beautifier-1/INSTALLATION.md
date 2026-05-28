# HTML Presentation Beautifier - 安装指南

本文档说明如何将 `html-presentation-beautifier` 插件安装为 Claude Code 的 command 命令。

---

## 📦 插件信息

- **名称**: html-presentation-beautifier
- **版本**: 1.0.0
- **命令**: `/beauty`
- **功能**: 将文档转换为 McKinsey 风格的 HTML 演示文稿

---

## 🚀 安装方法

### 方法 1: 当前目录使用（推荐用于测试）

如果插件已经在当前目录，无需额外安装，直接使用：

```bash
# 确保在插件目录中
cd /path/to/html-presentation-beautifier

# 直接使用 /beauty 命令
/beauty your_document.md
```

### 方法 2: 在其他项目中使用（符号链接）

在你的项目目录中创建符号链接：

```bash
# 进入你的项目目录
cd /path/to/your-project

# 运行安装脚本（从插件目录）
/path/to/html-presentation-beautifier/install.sh link
```

或者手动创建符号链接：

```bash
# 创建符号链接
ln -s /path/to/html-presentation-beautifier/.claude-plugin .claude-plugin
ln -s /path/to/html-presentation-beautifier/commands commands
ln -s /path/to/html-presentation-beautifier/skills skills
```

### 方法 3: 全局安装（推荐用于多个项目）

```bash
# 进入插件目录
cd /path/to/html-presentation-beautifier

# 运行全局安装
./install.sh global

# 在需要使用的项目中创建符号链接
cd /path/to/your-project
ln -s ~/.claude-code-plugins/html-presentation-beautifier/.claude-plugin .claude-plugin
ln -s ~/.claude-code-plugins/html-presentation-beautifier/commands commands
ln -s ~/.claude-code-plugins/html-presentation-beautifier/skills skills
```

---

## 📋 安装脚本使用说明

安装脚本 `install.sh` 支持三种模式：

### 1. 本地模式（默认）

```bash
./install.sh
# 或
./install.sh local
```

显示插件信息，无需安装。

### 2. 链接模式

```bash
./install.sh link
# 或
./install.sh -l
# 或
./install.sh --link
```

在当前目录创建符号链接到插件。

**使用场景**: 在特定项目中使用插件

**示例**:
```bash
cd ~/my-project
~/plugins/html-presentation-beautifier/install.sh link
```

### 3. 全局模式

```bash
./install.sh global
# 或
./install.sh -g
# 或
./install.sh --global
```

将插件复制到全局插件目录 `~/.claude-code-plugins/`。

**使用场景**: 在多个项目中共享插件

**后续步骤**:
```bash
# 在需要使用的项目中
cd ~/another-project
ln -s ~/.claude-code-plugins/html-presentation-beautifier/.claude-plugin .claude-plugin
ln -s ~/.claude-code-plugins/html-presentation-beautifier/commands commands
ln -s ~/.claude-code-plugins/html-presentation-beautifier/skills skills
```

---

## ✅ 验证安装

安装完成后，验证插件是否正确配置：

```bash
# 检查符号链接
ls -la .claude-plugin commands skills

# 检查配置文件
cat .claude-plugin/plugin.json

# 检查命令文件
ls commands/
# 应该看到: beauty.md

# 检查技能文件
ls skills/
# 应该看到: SKILL.md, scripts/, assets/, references/
```

---

## 🎯 使用方法

安装完成后，可以在 Claude Code 中使用 `/beauty` 命令：

### 基本用法

```
/beauty document.md
```

### 多个文件

```
/beauty report.md analysis.md summary.md
```

### 不同格式

```
/beauty data.json
/beauty document.txt
/beauty presentation.md
```

---

## 📂 插件目录结构

安装后的目录结构：

```
your-project/
├── .claude-plugin/          # 插件配置（符号链接）
│   └── plugin.json
├── commands/                # 命令定义（符号链接）
│   └── beauty.md
├── skills/                  # 技能定义（符号链接）
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── parser.py
│   │   ├── generator_v3.py
│   │   └── generator_optimized.py
│   ├── assets/
│   │   ├── styles.css
│   │   └── template.html
│   └── references/
│       ├── parsing-guidelines.md
│       └── best-practices.md
└── your files...
```

---

## 🔧 故障排除

### 问题 1: 命令无法识别

**症状**: 输入 `/beauty` 提示命令不存在

**解决方案**:
1. 确认符号链接已正确创建
2. 检查 `.claude-plugin/plugin.json` 文件存在
3. 重启 Claude Code

### 问题 2: 符号链接失效

**症状**: 符号链接指向错误的路径

**解决方案**:
```bash
# 删除旧的符号链接
rm .claude-plugin commands skills

# 重新创建
/path/to/plugin/install.sh link
```

### 问题 3: 权限问题

**症状**: 无法读取脚本文件

**解决方案**:
```bash
# 添加执行权限
chmod +x skills/scripts/*.py

# 或使用绝对路径
python3 /path/to/plugin/skills/scripts/parser.py
```

---

## 📚 更多文档

- [快速使用指南](QUICK_START.md)
- [技能定义](skills/SKILL.md)
- [测试报告](PLUGIN_TEST_REPORT.md)
- [命令文档](commands/beauty.md)

---

## 💡 提示

1. **推荐使用符号链接**: 避免复制多个副本，便于维护更新
2. **全局安装适合多项目**: 如果需要在多个项目中使用，建议全局安装
3. **版本控制**: 不要将符号链接提交到 Git，可以在 `.gitignore` 中添加：
   ```
   .claude-plugin
   commands
   skills
   ```

---

## 🎉 安装完成

现在你可以使用 `/beauty` 命令来美化你的文档了！

示例：
```
/beauty my_report.md
```

这将生成一个 McKinsey 风格的 HTML 演示文稿。

---

**最后更新**: 2026-01-21
**版本**: 1.0.0

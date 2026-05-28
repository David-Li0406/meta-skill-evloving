# 中文接口文档生成器技能

**自动分析代码中的接口定义，提取中文注释和文档字符串，生成简洁清晰的中文接口文档。**

## 概述

此技能为中文开发者自动分析代码中的接口定义（函数、类、模块、API端点等），提取中文注释和文档字符串，生成简洁清晰的中文接口文档。专注于内部文档、快速原型和团队协作场景，支持交互式选项选择。

**区别于OpenAPI生成器**：通用接口支持（非仅API）、中文优先、简单交互、无复杂规范验证。

## 主要功能

- **接口分析**：识别Python/JS/TS代码中的函数、类方法、API端点等接口定义
- **中文文档提取**：优先提取中文注释、docstring，支持简繁体中文
- **多格式输出**：Markdown、HTML、JSON，支持REST/GraphQL/函数接口
- **交互选项**：选择详细程度（简要/详细）、格式、包含示例
- **报告生成**：一键生成完整中文接口报告，保存为时间戳文件
- **团队友好**：简洁输出，便于中文团队审阅和协作

## 技术架构

```
interface_analyzer.py    # 接口定义分析器（AST解析）
chinese_doc_extractor.py # 中文注释和docstring提取器
doc_formatter.py         # 文档格式化器（Markdown/HTML/JSON）
report_generator.py      # 完整报告生成器
```

## 使用方法

### 基本调用

1. 提供代码片段、文件路径或目录
2. 指定语言类型（python/javascript/typescript）
3. 选择详细程度（简要/详细）
4. 选择输出格式（markdown/html/json）

### 示例调用

**示例1：Python函数分析**
```
使用chinese-interface-doc-generator技能分析这个Python函数并生成详细中文文档：
def 用户登录(user: str, pwd: str) -> bool:
    '''用户登录接口...'''
```

**示例2：JS模块文档提取**
```
使用chinese-interface-doc-generator技能，从这个JS文件提取所有方法的中文文档，用简要Markdown格式。
```

**示例3：HTML格式输出**
```
为这个类生成HTML接口文档，包括参数说明和示例。
```

## 输入要求

- **代码内容**：代码字符串、文件路径或目录（支持.py, .js, .ts）
- **语言类型**：python（默认）、javascript、typescript
- **可选参数**：
  - `detail_level`: 简要/详细 (default: 详细)
  - `output_format`: markdown/html/json (default: markdown)
  - `include_examples`: true/false (default: true)

## 输出格式

- **主要输出**：中文Markdown报告，格式：`接口文档_YYYY-MM-DD_HH-MM-SS.md`
- **保存位置**：`~/.claude/interface_docs/`
- **内容包括**：
  - 接口列表与签名
  - 中文描述/参数/返回值
  - 示例调用（若有）
  - 错误码/异常处理
  - 生成元数据

## 安装

### 安装到Claude Code

1. **复制技能文件夹**：
   ```bash
   # 个人安装
   cp -r generated-skills/chinese-interface-doc-generator ~/.claude/skills/

   # 项目安装
   cp -r generated-skills/chinese-interface-doc-generator .claude/skills/
   ```

2. **重启Claude Code**或重新加载技能

3. **验证安装**：
   - 技能将自动加载
   - 当用户请求接口文档分析时自动触发

### 文件结构

```
chinese-interface-doc-generator/
├── SKILL.md                    # 技能定义文件
├── README.md                   # 本文件
├── HOW_TO_USE.md               # 使用示例
├── interface_analyzer.py       # 接口分析器
├── chinese_doc_extractor.py    # 中文文档提取器
├── doc_formatter.py           # 文档格式化器
├── report_generator.py        # 报告生成器
├── sample_input.json          # 示例输入数据
├── expected_output.json       # 预期输出验证
└── test_basic.py              # 基础功能测试
```

## 最佳实践

1. **代码规范**：使用中文docstring，便于自动提取
2. **结构清晰**：接口定义使用标准语法，避免嵌套过深
3. **提供示例**：代码中包含调用示例，提高文档质量
4. **分模块分析**：大型项目分目录处理，避免单次过载
5. **审阅输出**：自动生成后手动补充业务上下文

## 限制

- 主要支持Python/JS/TS，复杂语言需手动调整
- 依赖代码注释质量，无注释时仅提取签名
- 非动态语言的二进制接口不支持
- 大型代码库建议分批处理

## 测试验证

运行基础测试：
```bash
cd chinese-interface-doc-generator
python test_basic.py
```

测试将验证：
1. 接口分析功能
2. 中文文档提取
3. 文档格式化
4. 报告生成

## 故障排除

### 常见问题

1. **中文显示乱码**：
   - 确保系统支持UTF-8编码
   - 检查输出文件编码（应为UTF-8）
   - 在Windows系统上可能需要设置控制台编码

2. **无法识别接口**：
   - 检查代码语法是否正确
   - 确认语言类型选择正确
   - 尝试简化代码结构

3. **输出文件未生成**：
   - 检查目录权限：`~/.claude/interface_docs/`
   - 确认磁盘空间充足
   - 查看是否有文件系统错误

### 调试模式

如需详细调试信息，可修改`report_generator.py`中的日志输出级别。

## 版本历史

- **v1.0.0** (2025-12-26): 初始版本发布
  - 基础接口分析功能
  - 中文文档提取
  - 多格式输出支持
  - 报告自动生成

## 相关资源

- [Claude Skills官方文档](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Skills Marketplace](https://github.com/anthropics/skills)
- [Claude Code文档](https://docs.claude.com/en/docs/claude-code)

---

**注意**：此技能为中文开发团队设计，专注于中文代码注释和文档生成，提升团队协作效率。
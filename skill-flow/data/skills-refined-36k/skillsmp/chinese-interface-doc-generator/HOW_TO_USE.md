# 如何使用此技能

嘿 Claude—我刚刚添加了 \"chinese-interface-doc-generator\" 技能。你能分析这段代码并生成中文接口文档吗？

## 示例调用

**示例1：**
嘿 Claude—我刚刚添加了 \"chinese-interface-doc-generator\" 技能。请分析这个Python函数并生成详细的中文文档：
```
def 用户注册(name, email): \"\"\"用户注册接口...\"\"\"
```

**示例2：**
使用chinese-interface-doc-generator技能，从这个JS文件提取所有方法的中文学文档，用简要Markdown格式。

**示例3：**
为这个类生成HTML接口文档，包括参数说明和示例。

## 需要提供什么

- 代码片段、文件路径或目录
- 语言（python/js/ts，可选）
- 详细程度（简要/详细，可选）
- 输出格式（markdown/html/json，可选）

## 你将得到什么

- 完整中文接口列表
- 提取的注释和docstring
- 参数/返回值说明
- 保存的报告文件（时间戳命名）
- 预览和安装路径
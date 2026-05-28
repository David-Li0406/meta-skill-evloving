#!/usr/bin/env python3
"""
技能初始化工具 - 从模板创建新技能

用法:
    init_skill.py <skill-name> --path <path>

示例:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private
    init_skill.py custom-skill --path /custom/location
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: 完成并提供关于该技能的功能以及何时使用它的说明。包括何时使用此技能 —— 触发它的特定场景、文件类型或任务。]
---

# {skill_title}

## 概览 (Overview)

[TODO: 用 1-2 句话解释这个技能的作用]

## 技能结构说明 (Structuring This Skill)

[TODO: 方案最适合该技能目的的结构。常见模式：

**1. 基于工作流 (Workflow-Based)** (最适合顺序流程)
- 当有明确的逐步操作流程时效果很好
- 示例：具有“工作流决策树” → “读取” → “创建” → “编辑”的 DOCX 技能
- 结构：## 概览 → ## 工作流决策树 → ## 步骤 1 → ## 步骤 2...

**2. 基于任务 (Task-Based)** (最适合工具集合)
- 当技能提供不同的操作/能力时效果很好
- 示例：具有“快速开始” → “合并 PDF” → “拆分 PDF” → “提取文本”的 PDF 技能
- 结构：## 概览 → ## 快速开始 → ## 任务类别 1 → ## 任务类别 2...

**3. 参考/指南 (Reference/Guidelines)** (最适合标准或规范)
- 适用于品牌指南、编码标准或要求
- 示例：具有“品牌指南” → “颜色” → “排版” → “特性”的品牌样式
- 结构：## 概览 → ## 指南 → ## 规范 → ## 使用...

**4. 基于能力 (Capabilities-Based)** (最适合集成系统)
- 当技能提供多个相互关联的功能时效果很好
- 示例：具有“核心能力” → 编号能力列表的产品管理
- 结构：## 概览 → ## 核心能力 → ### 1. 功能 → ### 2. 功能...

模式可以根据需要混合使用。大多数技能会结合多种模式（例如，从基于任务开始，为复杂操作添加工作流）。

完成后删除整个“技能结构说明”部分 —— 这只是指导建议。]

## [TODO: 根据选择的结构替换为第一个主要部分]

[TODO: 在此处添加内容。参考现有技能中的示例：
- 技术性技能的代码示例
- 复杂工作流的决策树
- 具有真实用户请求的具体示例
- 根据需要引用 scripts/templates/references]

## 资源 (Resources)

此技能包含示例资源目录，演示如何组织不同类型的捆绑资源：

### scripts/
可以直接运行以执行特定操作的可执行代码（Python/Bash 等）。

**其他技能的示例：**
- PDF 技能：`fill_fillable_fields.py`, `extract_form_field_info.py` - 用于 PDF 处理的工具
- DOCX 技能：`document.py`, `utilities.py` - 用于文档处理的 Python 模块

**适用场景：** 执行自动化、数据处理或特定操作的 Python 脚本、shell 脚本或任何可执行代码。

**注意：** 脚本可以在不加载到上下文的情况下执行，但仍可以由 Agent 读取以进行补丁修复或环境调整。

### references/
旨在加载到上下文中以辅助 Agent 处理和思考的文档和参考资料。

**其他技能的示例：**
- 产品管理：`communication.md`, `context_building.md` - 详细的工作流指南
- BigQuery：API 参考文档和查询示例
- 财务：模式文档、公司政策

**适用场景：** 深入的文档、API 参考、数据库模式、综合指南或 Agent 在工作时应参考的任何详细信息。

### assets/
不打算加载到上下文中，而是用于 Agent 产生的输出中的文件。

**其他技能的示例：**
- 品牌样式：PowerPoint 模板文件 (.pptx)，徽标文件
- 前端构建器：HTML/React 样板项目目录
- 排版：字体文件 (.ttf, .woff2)

**适用场景：** 模板、样板代码、文档模板、图像、图标、字体或任何打算在最终输出中复制或使用的文件。

---

**任何不需要的目录都可以删除。** 并非每个技能都需要所有三种类型的资源。
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} 的示例辅助脚本

这是一个可以直接运行的占位脚本。
请替换为实际实现，或在不需要时删除。

其他技能的真实脚本示例：
- pdf/scripts/fill_fillable_fields.py - 填充 PDF 表单字段
- pdf/scripts/convert_pdf_to_images.py - 将 PDF 页面转换为图像
"""

def main():
    print("这是 {skill_name} 的示例脚本")
    # TODO: 在此处添加实际脚本逻辑
    # 可以是数据处理、文件转换、API 调用等。

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} 的参考文档

这是一个详细参考文档的占位符。
请替换为实际参考内容，或在不需要时删除。

其他技能的真实参考文档示例：
- product-management/references/communication.md - 状态更新的综合指南
- product-management/references/context_building.md - 收集背景信息的深入探讨
- bigquery/references/ - API 参考和查询示例

## 何时使用参考文档

参考文档非常适用于：
- 详尽的 API 文档
- 详细的工作流指南
- 复杂的多步骤流程
- 对于主 SKILL.md 而言过长信息
- 仅针对特定用例需要的内容

## 结构建议

### API 参考示例
- 概览 (Overview)
- 身份验证 (Authentication)
- 端点与示例 (Endpoints with examples)
- 错误代码 (Error codes)
- 速率限制 (Rate limits)

### 工作流指南示例
- 前提条件 (Prerequisites)
- 分步说明 (Step-by-step instructions)
- 常见模式 (Common patterns)
- 故障排查 (Troubleshooting)
- 最佳实践 (Best practices)
"""

EXAMPLE_ASSET = """# 示例资产 (Asset) 文件

这个占位符表示存储资产文件的位置。
请替换为实际资产文件（模板、图像、字体等），或在不需要时删除。

资产文件并不打算加载到上下文中，而是用于 Agent 产生的输出中。

其他技能的示例资产文件：
- 品牌指南：logo.png, slides_template.pptx
- 前端构建器：带有 HTML/React 样板的 hello-world/ 目录
- 排版：custom-font.ttf, font-family.woff2
- 数据：sample_data.csv, test_dataset.json

## 常见资产类型

- 模板：.pptx, .docx, 样板目录
- 图像：.png, .jpg, .svg, .gif
- 字体：.ttf, .otf, .woff, .woff2
- 样板代码：项目目录、启动文件
- 图标：.ico, .svg
- 数据文件：.csv, .json, .xml, .yaml

注意：这只是一个文本占位符。实际资产可以是任何文件类型。
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created

    Returns:
        Path to created skill directory, or None if error
    """
    # Determine skill directory path
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"❌ 错误: 技能目录已存在: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ 已创建技能目录: {skill_dir}")
    except Exception as e:
        print(f"❌ 创建目录时出错: {e}")
        return None

    # Create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("✅ 已创建 SKILL.md")
    except Exception as e:
        print(f"❌ 创建 SKILL.md 时出错: {e}")
        return None

    # Create resource directories with example files
    try:
        # 创建 scripts/ 目录及示例脚本
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ 已创建 scripts/example.py")

        # 创建 references/ 目录及示例参考文档
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ 已创建 references/api_reference.md")

        # 创建 assets/ 目录及示例资产占位符
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("✅ 已创建 assets/example_asset.txt")
    except Exception as e:
        print(f"❌ 创建资源目录时出错: {e}")
        return None

    # 打印后续步骤
    print(f"\n✅ 技能 '{skill_name}' 已成功在 {skill_dir} 初始化")
    print("\n后续步骤:")
    print("1. 编辑 SKILL.md 以完成 TODO 项目并更新描述")
    print("2. 自定义或删除 scripts/、references/ 和 assets/ 中的示例文件")
    print("3. 准备就绪后运行验证器以检查技能结构")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("用法: init_skill.py <skill-name> --path <path>")
        print("\n技能名称要求:")
        print("  - 使用连字符分隔的标识符 (例如 'data-analyzer')")
        print("  - 仅限小写字母、数字和连字符")
        print("  - 最大 40 个字符")
        print("  - 必须与目录名完全匹配")
        print("\n示例:")
        print("  init_skill.py my-new-skill --path skills/public")
        print("  init_skill.py my-api-helper --path skills/private")
        print("  init_skill.py custom-skill --path /custom/location")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 正在初始化技能: {skill_name}")
    print(f"   位置: {path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
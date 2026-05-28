#!/usr/bin/env node

/**
 * Skill 初始化器 - 从模板创建新的 skill
 *
 * 使用方法：
 *    init_skill.ts <skill-name> --path <path>
 *
 * 示例：
 *    init_skill.ts my-new-skill --path skills/public
 *    init_skill.ts my-api-helper --path skills/private
 *    init_skill.ts custom-skill --path /custom/location
 */

import * as fs from 'fs/promises';
import * as path from 'path';

const SKILL_TEMPLATE = `---
name: {skill_name}
description: [TODO: 完整且信息丰富的说明，解释该 skill 的功能和使用时机。包括何时使用该 skill - 触发它的具体场景、文件类型或任务。]
---

# {skill_title}

## 概述

[TODO: 1-2 句话说明该 skill 能够实现什么]

## Skill 结构组织

[TODO: 根据该 skill 的目的选择最适合的结构。常见模式：

**1. 基于工作流**（最适合顺序过程）
- 当有清晰的步骤程序时效果很好
- 示例：DOCX skill 包含"工作流决策树" → "读取" → "创建" → "编辑"
- 结构：## 概述 → ## 工作流决策树 → ## 步骤 1 → ## 步骤 2...

**2. 基于任务**（最适合工具集合）
- 当 skill 提供不同的操作/能力时效果很好
- 示例：PDF skill 包含"快速开始" → "合并 PDF" → "拆分 PDF" → "提取文本"
- 结构：## 概述 → ## 快速开始 → ## 任务类别 1 → ## 任务类别 2...

**3. 参考/指南**（最适合标准或规范）
- 适用于品牌指南、编码标准或要求
- 示例：品牌样式包含"品牌指南" → "颜色" → "字体" → "特性"
- 结构：## 概述 → ## 指南 → ## 规范 → ## 使用...

**4. 基于能力**（最适合集成系统）
- 当 skill 提供多个相互关联的功能时效果很好
- 示例：产品管理包含"核心能力" → 编号能力列表
- 结构：## 概述 → ## 核心能力 → ### 1. 功能 → ### 2. 功能...

可以根据需要混合和匹配模式。大多数 skill 会组合模式（例如，从基于任务开始，为复杂操作添加工作流）。

完成后删除整个"Skill 结构组织"部分 - 这只是指导。]

## [TODO: 根据所选结构替换为第一个主要部分]

[TODO: 在此添加内容。查看现有 skill 中的示例：
- 技术 skill 的代码示例
- 复杂工作流的决策树
- 包含真实用户请求的具体示例
- 根据需要引用 scripts/templates/references]

## 资源

该 skill 包含示例资源目录，展示如何组织不同类型的references：

### scripts/
可执行代码（TypeScript/JavaScript/Bash 等），可以直接运行以执行特定操作。

**其他 skill 的示例：**
- PDF skill: fill_fillable_fields.ts, extract_form_field_info.ts - PDF 操作工具
- DOCX skill: document.ts, utilities.ts - 文档处理的 TypeScript 模块

**适用于：**TypeScript 脚本、shell 脚本，或任何执行自动化、数据处理或特定操作的可执行代码。

**注意：**脚本可以在不加载到上下文的情况下执行，但仍可以被 Claude 读取以进行补丁或环境调整。

### references/
旨在加载到上下文中的文档和参考资料，用于为 Claude 的过程和思考提供信息。

**其他 skill 的示例：**
- 产品管理：communication.md, context_building.md - 详细的工作流指南
- BigQuery：API 参考文档和查询示例
- 财务：架构文档、公司政策

**适用于：**深度文档、API 参考、数据库架构、综合指南，或 Claude 在工作时应该引用的任何详细信息。

### assets/
不打算加载到上下文中的文件，而是在 Claude 产生的输出中使用。

**其他 skill 的示例：**
- 品牌样式：PowerPoint 模板文件（.pptx）、logo 文件
- 前端构建器：HTML/React 样板项目目录
- 字体设计：字体文件（.ttf, .woff2）

**适用于：**模板、样板代码、文档模板、图像、图标、字体，或任何要复制或用于最终输出的文件。

---

**任何不需要的目录都可以删除。**并非每个 skill 都需要所有三种类型的资源。
`;

const EXAMPLE_SCRIPT = `#!/usr/bin/env node

/**
 * {skill_name} 的示例辅助脚本
 *
 * 这是一个可以直接执行的占位符脚本。
 * 用实际实现替换或不需要时删除。
 *
 * 其他 skill 的真实脚本示例：
 * - pdf/scripts/fill_fillable_fields.ts - 填充 PDF 表单字段
 * - pdf/scripts/convert_pdf_to_images.ts - 将 PDF 页面转换为图像
 */

import * as fs from 'fs';
import * as path from 'path';

function main(): void {
    console.log("这是 {skill_name} 的示例脚本");
    // TODO: 在此添加实际的脚本逻辑
    // 这可能是数据处理、文件转换、API 调用等。
}

if (require.main === module) {
    main();
}
`;

const EXAMPLE_REFERENCE = `# {skill_title} 的参考文档

这是详细参考文档的占位符。
用实际参考内容替换或不需要时删除。

其他 skill 的真实参考文档示例：
- product-management/references/communication.md - 状态更新的综合指南
- product-management/references/context_building.md - 收集上下文的深度分析
- bigquery/references/ - API 参考和查询示例

## 何时使用参考文档

参考文档适用于：
- 全面的 API 文档
- 详细的工作流指南
- 复杂的多步骤过程
- 对于主 SKILL.md 来说过长的信息
- 仅特定用例需要的内容

## 结构建议

### API 参考示例
- 概述
- 身份验证
- 带示例的端点
- 错误代码
- 速率限制

### 工作流指南示例
- 先决条件
- 分步说明
- 常见模式
- 故障排除
- 最佳实践
`;

const EXAMPLE_ASSET = `# 示例资源文件

此占位符表示资源文件的存储位置。
用实际资源文件（模板、图像、字体等）替换或不需要时删除。

资源文件不打算加载到上下文中，而是在 Claude 产生的输出中使用。

其他 skill 的资源文件示例：
- 品牌指南：logo.png, slides_template.pptx
- 前端构建器：包含 HTML/React 样板的 hello-world/ 目录
- 字体设计：custom-font.ttf, font-family.woff2
- 数据：sample_data.csv, test_dataset.json

## 常见资源类型

- 模板：.pptx, .docx, 样板目录
- 图像：.png, .jpg, .svg, .gif
- 字体：.ttf, .otf, .woff, .woff2
- 样板代码：项目目录、启动文件
- 图标：.ico, .svg
- 数据文件：.csv, .json, .xml, .yaml

注意：这是一个文本占位符。实际资源可以是任何文件类型。
`;

/**
 * 将连字符分隔的 skill 名称转换为标题格式用于显示
 */
function titleCaseSkillName(skillName: string): string {
    return skillName
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

/**
 * 使用模板 SKILL.md 初始化新的 skill 目录
 */
async function initSkill(skillName: string, targetPath: string): Promise<string | null> {
    try {
        // 确定 skill 目录路径
        const skillDir = path.resolve(targetPath, skillName);

        // 检查目录是否已存在
        try {
            await fs.access(skillDir);
            console.log(`❌ 错误：Skill 目录已存在：${skillDir}`);
            return null;
        } catch {
            // 目录不存在，这正是我们想要的
        }

        // 创建 skill 目录
        await fs.mkdir(skillDir, { recursive: true });
        console.log(`✅ 已创建 skill 目录：${skillDir}`);

        // 从模板创建 SKILL.md
        const skillTitle = titleCaseSkillName(skillName);
        const skillContent = SKILL_TEMPLATE
            .replace(/{skill_name}/g, skillName)
            .replace(/{skill_title}/g, skillTitle);

        const skillMdPath = path.join(skillDir, 'SKILL.md');
        await fs.writeFile(skillMdPath, skillContent, 'utf8');
        console.log("✅ 已创建 SKILL.md");

        // 创建包含示例文件的资源目录
        try {
            // 创建包含示例脚本的 scripts/ 目录
            const scriptsDir = path.join(skillDir, 'scripts');
            await fs.mkdir(scriptsDir, { recursive: true });

            const exampleScriptPath = path.join(scriptsDir, 'example.ts');
            const exampleScriptContent = EXAMPLE_SCRIPT.replace(/{skill_name}/g, skillName);
            await fs.writeFile(exampleScriptPath, exampleScriptContent, 'utf8');

            // 使脚本可执行（在 Unix 系统上）
            try {
                await fs.chmod(exampleScriptPath, 0o755);
            } catch {
                // 在 Windows 上忽略 chmod 错误
            }
            console.log("✅ 已创建 scripts/example.ts");

            // 创建包含示例参考文档的 references/ 目录
            const referencesDir = path.join(skillDir, 'references');
            await fs.mkdir(referencesDir, { recursive: true });

            const exampleReferencePath = path.join(referencesDir, 'api_reference.md');
            const exampleReferenceContent = EXAMPLE_REFERENCE.replace(/{skill_title}/g, skillTitle);
            await fs.writeFile(exampleReferencePath, exampleReferenceContent, 'utf8');
            console.log("✅ 已创建 references/api_reference.md");

            // 创建包含示例资源占位符的 assets/ 目录
            const assetsDir = path.join(skillDir, 'assets');
            await fs.mkdir(assetsDir, { recursive: true });

            const exampleAssetPath = path.join(assetsDir, 'example_asset.txt');
            await fs.writeFile(exampleAssetPath, EXAMPLE_ASSET, 'utf8');
            console.log("✅ 已创建 assets/example_asset.txt");
        } catch (error) {
            console.log(`❌ 创建资源目录时出错：${error}`);
            return null;
        }

        // 打印后续步骤
        console.log(`\n✅ Skill '${skillName}' 已在 ${skillDir} 成功初始化`);
        console.log("\n后续步骤：");
        console.log("1. 编辑 SKILL.md 完成 TODO 项目并更新描述");
        console.log("2. 自定义或删除 scripts/、references/ 和 assets/ 中的示例文件");
        console.log("3. 准备好后运行验证器检查 skill 结构");

        return skillDir;
    } catch (error) {
        console.log(`❌ 错误：${error}`);
        return null;
    }
}

/**
 * 主函数
 */
async function main(): Promise<void> {
    const args = process.argv.slice(2);

    // 查找 --path 标志并提取 skill 名称
    const pathIndex = args.indexOf('--path');
    if (pathIndex === -1 || pathIndex !== 1 || args.length !== 3) {
        console.log("使用方法：init_skill.ts <skill-name> --path <path>");
        console.log("\nSkill 名称要求：");
        console.log("  - 连字符分隔标识符（例如：'data-analyzer'）");
        console.log("  - 仅小写字母、数字和连字符");
        console.log("  - 最多 40 个字符");
        console.log("  - 必须与目录名称完全匹配");
        console.log("\n示例：");
        console.log("  init_skill.ts my-new-skill --path skills/public");
        console.log("  init_skill.ts my-api-helper --path skills/private");
        console.log("  init_skill.ts custom-skill --path /custom/location");
        process.exit(1);
    }

    const skillName = args[0];
    const targetPath = args[2];

    console.log(`🚀 正在初始化 skill：${skillName}`);
    console.log(`   位置：${targetPath}`);
    console.log();

    const result = await initSkill(skillName, targetPath);

    if (result) {
        process.exit(0);
    } else {
        process.exit(1);
    }
}

if (require.main === module) {
    main().catch(error => {
        console.error('❌ 意外错误：', error);
        process.exit(1);
    });
}
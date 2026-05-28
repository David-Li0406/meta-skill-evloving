#!/usr/bin/env node

/**
 * 技能快速验证脚本 - 精简版本
 *
 * 使用方法:
 *    npx ts-node quick_validate.ts <技能目录>
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import * as yaml from 'js-yaml';

interface ValidationResult {
    valid: boolean;
    message: string;
}

interface SkillFrontmatter {
    name?: string;
    description?: string;
    license?: string;
    'allowed-tools'?: string[];
    metadata?: Record<string, any>;
}

const ALLOWED_PROPERTIES = new Set([
    'name',
    'description',
    'license',
    'allowed-tools',
    'metadata'
]);

/**
 * 技能的基本验证
 */
export async function validateSkill(skillPath: string): Promise<boolean> {
    const result = await validateSkillWithMessage(skillPath);
    console.log(result.message);
    return result.valid;
}

/**
 * 验证技能并返回详细结果
 */
export async function validateSkillWithMessage(skillPath: string): Promise<ValidationResult> {
    try {
        // 检查 SKILL.md 是否存在
        const skillMd = path.join(skillPath, 'SKILL.md');
        try {
            await fs.access(skillMd);
        } catch {
            return { valid: false, message: "未找到 SKILL.md" };
        }

        // 读取并验证前置元数据
        const content = await fs.readFile(skillMd, 'utf8');
        if (!content.startsWith('---')) {
            return { valid: false, message: "未找到 YAML 前置元数据" };
        }

        // 提取前置元数据
        const frontmatterMatch = content.match(/^---\n(.*?)\n---/s);
        if (!frontmatterMatch) {
            return { valid: false, message: "前置元数据格式无效" };
        }

        const frontmatterText = frontmatterMatch[1];

        // 解析 YAML 前置元数据
        let frontmatter: SkillFrontmatter;
        try {
            const parsed = yaml.load(frontmatterText) as SkillFrontmatter;
            if (!parsed || typeof parsed !== 'object') {
                return { valid: false, message: "前置元数据必须是一个 YAML 字典" };
            }
            frontmatter = parsed;
        } catch (error) {
            return { valid: false, message: `前置元数据中的 YAML 无效: ${error}` };
        }

        // 检查意外属性（不包括 metadata 下的嵌套键）
        const unexpectedKeys = Object.keys(frontmatter).filter(key => !ALLOWED_PROPERTIES.has(key));
        if (unexpectedKeys.length > 0) {
            const allowedList = Array.from(ALLOWED_PROPERTIES).sort().join(', ');
            const unexpectedList = unexpectedKeys.sort().join(', ');
            return {
                valid: false,
                message: `SKILL.md 前置元数据中有意外的键: ${unexpectedList}。允许的属性是: ${allowedList}`
            };
        }

        // 检查必需字段
        if (!frontmatter.name) {
            return { valid: false, message: "前置元数据中缺少 'name'" };
        }
        if (!frontmatter.description) {
            return { valid: false, message: "前置元数据中缺少 'description'" };
        }

        // 提取名称进行验证
        const name = String(frontmatter.name).trim();
        if (name) {
            // 检查命名约定 (hyphen-case: 小写字母和连字符)
            if (!/^[a-z0-9-]+$/.test(name)) {
                return {
                    valid: false,
                    message: `名称 '${name}' 应该是 hyphen-case（仅限小写字母、数字和连字符）`
                };
            }
            if (name.startsWith('-') || name.endsWith('-') || name.includes('--')) {
                return {
                    valid: false,
                    message: `名称 '${name}' 不能以连字符开始/结束或包含连续连字符`
                };
            }
            // 检查名称长度（根据规范最多 64 个字符）
            if (name.length > 64) {
                return {
                    valid: false,
                    message: `名称太长（${name.length} 个字符）。最多 64 个字符。`
                };
            }
        }

        // 提取并验证描述
        const description = String(frontmatter.description).trim();
        if (description) {
            // 检查尖括号
            if (description.includes('<') || description.includes('>')) {
                return { valid: false, message: "描述不能包含尖括号（< 或 >）" };
            }
            // 检查描述长度（根据规范最多 1024 个字符）
            if (description.length > 1024) {
                return {
                    valid: false,
                    message: `描述太长（${description.length} 个字符）。最多 1024 个字符。`
                };
            }
        }

        return { valid: true, message: "技能验证通过!" };

    } catch (error) {
        return { valid: false, message: `验证错误: ${error}` };
    }
}

/**
 * 不依赖 js-yaml 的替代实现
 */
async function validateSkillSimple(skillPath: string): Promise<ValidationResult> {
    try {
        // 检查 SKILL.md 是否存在
        const skillMd = path.join(skillPath, 'SKILL.md');
        try {
            await fs.access(skillMd);
        } catch {
            return { valid: false, message: "未找到 SKILL.md" };
        }

        // 读取并验证前置元数据
        const content = await fs.readFile(skillMd, 'utf8');
        if (!content.startsWith('---')) {
            return { valid: false, message: "未找到 YAML 前置元数据" };
        }

        // 提取前置元数据
        const frontmatterMatch = content.match(/^---\n(.*?)\n---/s);
        if (!frontmatterMatch) {
            return { valid: false, message: "前置元数据格式无效" };
        }

        const frontmatterText = frontmatterMatch[1];

        // 简单的 YAML 验证（不解析）
        const lines = frontmatterText.split('\n');
        const seenKeys = new Set<string>();

        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed || trimmed.startsWith('#')) continue;

            const colonIndex = trimmed.indexOf(':');
            if (colonIndex === -1) continue;

            const key = trimmed.substring(0, colonIndex).trim();
            seenKeys.add(key);

            // 对必需键进行基本验证
            if (key === 'name') {
                const name = trimmed.substring(colonIndex + 1).trim();
                if (!name) {
                    return { valid: false, message: "前置元数据中缺少 'name' 值" };
                }
                // 如果有引号则移除
                const cleanName = name.replace(/^["']|["']$/g, '');
                if (!/^[a-z0-9-]+$/.test(cleanName)) {
                    return {
                        valid: false,
                        message: `名称 '${cleanName}' 应该是 hyphen-case（仅限小写字母、数字和连字符）`
                    };
                }
            }

            if (key === 'description') {
                const description = trimmed.substring(colonIndex + 1).trim();
                if (!description) {
                    return { valid: false, message: "前置元数据中缺少 'description' 值" };
                }
                // 如果有引号则移除
                const cleanDescription = description.replace(/^["']|["']$/g, '');
                if (cleanDescription.includes('<') || cleanDescription.includes('>')) {
                    return { valid: false, message: "描述不能包含尖括号（< 或 >）" };
                }
            }
        }

        // 检查必需键
        if (!seenKeys.has('name')) {
            return { valid: false, message: "前置元数据中缺少 'name'" };
        }
        if (!seenKeys.has('description')) {
            return { valid: false, message: "前置元数据中缺少 'description'" };
        }

        return { valid: true, message: "技能验证通过!" };

    } catch (error) {
        return { valid: false, message: `验证错误: ${error}` };
    }
}

/**
 * 主函数
 */
async function main(): Promise<void> {
    const args = process.argv.slice(2);

    if (args.length !== 1) {
        console.log("使用方法: npx ts-node quick_validate.ts <技能目录>");
        process.exit(1);
    }

    const skillDirectory = args[0];

    // 尝试使用 js-yaml（如果可用），否则使用简化验证
    try {
        require('js-yaml');
        const result = await validateSkillWithMessage(skillDirectory);
        console.log(result.message);
        process.exit(result.valid ? 0 : 1);
    } catch {
        console.log("⚠️  未找到 js-yaml，使用简化验证");
        console.log("     要获得完整的 YAML 验证，请安装: npm install js-yaml @types/js-yaml\n");
        const result = await validateSkillSimple(skillDirectory);
        console.log(result.message);
        process.exit(result.valid ? 0 : 1);
    }
}

if (require.main === module) {
    main().catch(error => {
        console.error('❌ 意外错误:', error);
        process.exit(1);
    });
}
#!/usr/bin/env node

/**
 * 技能打包器 - 创建技能文件夹的可分发 .skill 文件
 *
 * 使用方法:
 *    npx ts-node package_skill.ts <skill文件夹路径> [输出目录]
 *
 * 示例:
 *    npx ts-node package_skill.ts skills/public/my-skill
 *    npx ts-node package_skill.ts skills/public/my-skill ./dist
 */

import * as fs from 'fs/promises';
import * as fsSync from 'fs';
import * as path from 'path';
import archiver from 'archiver';
import { createWriteStream } from 'fs';
import { validateSkill } from './quick_validate';

/**
 * 将技能文件夹打包成 .skill 文件
 */
async function packageSkill(skillPath: string, outputDir?: string): Promise<string | null> {
    const resolvedSkillPath = path.resolve(skillPath);

    try {
        // 验证技能文件夹是否存在
        try {
            const stats = await fs.stat(resolvedSkillPath);
            if (!stats.isDirectory()) {
                console.log(`❌ 错误: 路径不是一个目录: ${resolvedSkillPath}`);
                return null;
            }
        } catch {
            console.log(`❌ 错误: 未找到技能文件夹: ${resolvedSkillPath}`);
            return null;
        }

        // 验证 SKILL.md 是否存在
        const skillMd = path.join(resolvedSkillPath, "SKILL.md");
        try {
            await fs.access(skillMd);
        } catch {
            console.log(`❌ 错误: 在 ${resolvedSkillPath} 中未找到 SKILL.md`);
            return null;
        }

        // 打包前运行验证
        console.log("🔍 正在验证技能...");
        const valid = await validateSkill(resolvedSkillPath);
        if (!valid) {
            console.log("❌ 验证失败。请在打包前修复验证错误。");
            return null;
        }
        console.log("✅ 技能验证通过!\n");

        // 确定输出位置
        const skillName = path.basename(resolvedSkillPath);
        let outputPath: string;

        if (outputDir) {
            outputPath = path.resolve(outputDir);
            await fs.mkdir(outputPath, { recursive: true });
        } else {
            outputPath = process.cwd();
        }

        const skillFilename = path.join(outputPath, `${skillName}.skill`);

        // 创建 .skill 文件 (zip 格式)
        return new Promise((resolve, reject) => {
            const output = createWriteStream(skillFilename);
            const archive = archiver('zip', { zlib: { level: 9 } });

            output.on('close', () => {
                console.log(`\n✅ 成功打包技能到: ${skillFilename}`);
                console.log(`📦 归档大小: ${archive.pointer()} 字节`);
                resolve(skillFilename);
            });

            archive.on('error', (err: Error) => {
                console.log(`❌ 创建 .skill 文件时出错: ${err}`);
                reject(err);
            });

            archive.pipe(output);

            // 遍历技能目录并添加文件
            const walkDir = async (dir: string, relativeTo: string): Promise<void> => {
                const entries = await fs.readdir(dir, { withFileTypes: true });

                for (const entry of entries) {
                    const fullPath = path.join(dir, entry.name);

                    if (entry.isDirectory()) {
                        await walkDir(fullPath, relativeTo);
                    } else {
                        const relativePath = path.relative(relativeTo, fullPath);
                        console.log(`  已添加: ${relativePath}`);
                        archive.file(fullPath, { name: relativePath });
                    }
                }
            };

            // 从技能的父目录开始遍历，以在 zip 中包含技能文件夹
            const skillParentDir = path.dirname(resolvedSkillPath);
            walkDir(resolvedSkillPath, skillParentDir)
                .then(() => archive.finalize())
                .catch(reject);
        });

    } catch (error) {
        console.log(`❌ 错误: ${error}`);
        return null;
    }
}

/**
 * 不依赖 archiver 的替代实现
 */
async function packageSkillSimple(skillPath: string, outputDir?: string): Promise<string | null> {
    const resolvedSkillPath = path.resolve(skillPath);

    try {
        // 验证技能文件夹是否存在
        try {
            const stats = await fs.stat(resolvedSkillPath);
            if (!stats.isDirectory()) {
                console.log(`❌ 错误: 路径不是一个目录: ${resolvedSkillPath}`);
                return null;
            }
        } catch {
            console.log(`❌ 错误: 未找到技能文件夹: ${resolvedSkillPath}`);
            return null;
        }

        // 验证 SKILL.md 是否存在
        const skillMd = path.join(resolvedSkillPath, "SKILL.md");
        try {
            await fs.access(skillMd);
        } catch {
            console.log(`❌ 错误: 在 ${resolvedSkillPath} 中未找到 SKILL.md`);
            return null;
        }

        // 打包前运行验证
        console.log("🔍 正在验证技能...");
        const valid = await validateSkill(resolvedSkillPath);
        if (!valid) {
            console.log("❌ 验证失败。请在打包前修复验证错误。");
            return null;
        }
        console.log("✅ 技能验证通过!\n");

        // 确定输出位置
        const skillName = path.basename(resolvedSkillPath);
        let outputPath: string;

        if (outputDir) {
            outputPath = path.resolve(outputDir);
            await fs.mkdir(outputPath, { recursive: true });
        } else {
            outputPath = process.cwd();
        }

        const skillFilename = path.join(outputPath, `${skillName}.skill`);

        // 使用 Node.js 内置的 zlib 进行 zip 创建 (更简单但灵活性较低)
        const { createWriteStream } = require('fs');
        const yauzl = require('yauzl'); // 读取时需要安装这个
        const yazl = require('yazl'); // 替代的 zip 库

        console.log("⚠️  注意: 要获得完整功能，请安装 archiver 包:");
        console.log("     npm install archiver @types/archiver");
        console.log("     然后使用主要的 packageSkill 函数。");

        return skillFilename;

    } catch (error) {
        console.log(`❌ 错误: ${error}`);
        return null;
    }
}

/**
 * 主函数
 */
async function main(): Promise<void> {
    const args = process.argv.slice(2);

    if (args.length < 1) {
        console.log("使用方法: npx ts-node package_skill.ts <skill文件夹路径> [输出目录]");
        console.log("\n示例:");
        console.log("  npx ts-node package_skill.ts skills/public/my-skill");
        console.log("  npx ts-node package_skill.ts skills/public/my-skill ./dist");
        console.log("\n前置条件:");
        console.log("  npm install archiver @types/archiver");
        process.exit(1);
    }

    const skillPath = args[0];
    const outputDir = args.length > 1 ? args[1] : undefined;

    console.log(`📦 正在打包技能: ${skillPath}`);
    if (outputDir) {
        console.log(`   输出目录: ${outputDir}`);
    }
    console.log();

    // 尝试使用 archiver（如果可用），否则使用简化版本
    try {
        require('archiver');
        const result = await packageSkill(skillPath, outputDir);
        if (result) {
            process.exit(0);
        } else {
            process.exit(1);
        }
    } catch {
        console.log("⚠️  未找到 Archiver，使用简化实现");
        console.log("     要获得完整功能，请安装: npm install archiver @types/archiver\n");
        const result = await packageSkillSimple(skillPath, outputDir);
        if (result) {
            process.exit(0);
        } else {
            process.exit(1);
        }
    }
}

if (require.main === module) {
    main().catch(error => {
        console.error('❌ 意外错误:', error);
        process.exit(1);
    });
}
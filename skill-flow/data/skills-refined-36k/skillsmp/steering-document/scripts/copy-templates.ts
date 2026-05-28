#!/usr/bin/env bun
/**
 * ステアリングドキュメントのテンプレートを指定ディレクトリにコピーするスクリプト
 *
 * Usage:
 *   bun run copy-templates.ts <targetDir>
 *
 * Examples:
 *   bun run copy-templates.ts .claude/skills/sdd-steering
 *   bun run copy-templates.ts specs/_steering
 */

import { dirname, join } from "node:path";

const SCRIPT_DIR = dirname(Bun.main);
const TEMPLATES_DIR = join(SCRIPT_DIR, "..", "templates");

async function main() {
	const targetDir = Bun.argv[2];

	if (!targetDir) {
		console.error("Error: Target directory is required");
		console.error("Usage: bun run copy-templates.ts <targetDir>");
		console.error("");
		console.error("Examples:");
		console.error("  bun run copy-templates.ts .claude/skills/sdd-steering");
		console.error("  bun run copy-templates.ts specs/_steering");
		process.exit(1);
	}

	// テンプレートディレクトリの存在確認
	const templatesGlob = new Bun.Glob("*-template.md");
	const templateFiles = Array.from(templatesGlob.scanSync(TEMPLATES_DIR));

	if (templateFiles.length === 0) {
		console.error("Error: No template files found in:", TEMPLATES_DIR);
		process.exit(1);
	}

	// ターゲットディレクトリの作成
	const targetFile = Bun.file(join(targetDir, ".keep"));
	if (!(await targetFile.exists())) {
		await Bun.write(targetFile, "");
		console.log(`Created directory: ${targetDir}`);
	}

	let copied = 0;
	let skipped = 0;

	for (const template of templateFiles) {
		const sourcePath = join(TEMPLATES_DIR, template);
		// product-template.md -> product.md
		const targetName = template.replace("-template", "");
		const targetPath = join(targetDir, targetName);

		const targetFileObj = Bun.file(targetPath);
		if (await targetFileObj.exists()) {
			console.log(`Skipped (already exists): ${targetName}`);
			skipped++;
			continue;
		}

		const sourceFile = Bun.file(sourcePath);
		await Bun.write(targetPath, sourceFile);
		console.log(`Copied: ${template} -> ${targetName}`);
		copied++;
	}

	// .keep ファイルを削除
	const keepFile = Bun.file(join(targetDir, ".keep"));
	if (await keepFile.exists()) {
		await Bun.write(keepFile, ""); // Bun doesn't have unlink, leave empty
	}

	console.log("");
	console.log(`✅ Done: ${copied} copied, ${skipped} skipped`);
	console.log(`📍 Target: ${targetDir}`);
	console.log("");
	console.log("Edit these files to define your project's steering documents.");
}

main();

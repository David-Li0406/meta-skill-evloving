#!/usr/bin/env bun

/**
 * Image Optimization Script
 *
 * Compresses PNG and JPEG images using sharp with optimal settings.
 * Only overwrites files if the optimized version is smaller.
 *
 * Usage:
 *   bun run scripts/optimize-images.ts              # Optimize all images
 *   bun run scripts/optimize-images.ts --dry-run    # Preview without changes
 *   bun run scripts/optimize-images.ts --file=path  # Test single file
 *
 * Settings can be customized via environment variables:
 *   PNG_QUALITY=80 JPEG_QUALITY=80 bun run scripts/optimize-images.ts
 */

import sharp from "sharp";
import { readdir, stat } from "fs/promises";
import { join, extname } from "path";

// Configuration (can be overridden via env vars)
const IMAGES_DIR = process.env.IMAGES_DIR || "./public/images";
const PNG_QUALITY = Number(process.env.PNG_QUALITY) || 80;
const JPEG_QUALITY = Number(process.env.JPEG_QUALITY) || 80;
const PNG_COMPRESSION = Number(process.env.PNG_COMPRESSION) || 9;

// CLI flags
const DRY_RUN = process.argv.includes("--dry-run");
const VERBOSE = process.argv.includes("--verbose") || process.argv.includes("-v");
const SINGLE_FILE = process.argv.find((arg) => arg.startsWith("--file="))?.split("=")[1];

interface OptimizationResult {
	file: string;
	originalSize: number;
	newSize: number;
	savings: number;
	savingsPercent: number;
	skipped: boolean;
}

/**
 * Recursively find all image files in a directory
 */
async function getAllImageFiles(dir: string): Promise<string[]> {
	const files: string[] = [];

	async function walk(currentDir: string) {
		const entries = await readdir(currentDir, { withFileTypes: true });
		for (const entry of entries) {
			const fullPath = join(currentDir, entry.name);
			if (entry.isDirectory()) {
				await walk(fullPath);
			} else {
				const ext = extname(entry.name).toLowerCase();
				if ([".png", ".jpg", ".jpeg"].includes(ext)) {
					files.push(fullPath);
				}
			}
		}
	}

	await walk(dir);
	return files.sort();
}

/**
 * Optimize a single image file
 */
async function optimizeImage(filePath: string): Promise<OptimizationResult> {
	const ext = extname(filePath).toLowerCase();
	const originalStat = await stat(filePath);
	const originalSize = originalStat.size;

	try {
		let outputBuffer: Buffer;

		if (ext === ".png") {
			outputBuffer = await sharp(filePath)
				.png({
					quality: PNG_QUALITY,
					compressionLevel: PNG_COMPRESSION,
					adaptiveFiltering: true,
					palette: true,
				})
				.toBuffer();
		} else {
			outputBuffer = await sharp(filePath)
				.jpeg({
					quality: JPEG_QUALITY,
					mozjpeg: true,
				})
				.toBuffer();
		}

		const newSize = outputBuffer.length;
		const savings = originalSize - newSize;
		const savingsPercent = (savings / originalSize) * 100;

		// Only write if we actually saved space and not dry run
		if (savings > 0 && !DRY_RUN) {
			await Bun.write(filePath, outputBuffer);
		}

		return {
			file: filePath,
			originalSize,
			newSize: savings > 0 ? newSize : originalSize,
			savings: Math.max(0, savings),
			savingsPercent: Math.max(0, savingsPercent),
			skipped: savings <= 0,
		};
	} catch (error) {
		console.error(`  ✗ Error optimizing ${filePath}:`, error instanceof Error ? error.message : error);
		return {
			file: filePath,
			originalSize,
			newSize: originalSize,
			savings: 0,
			savingsPercent: 0,
			skipped: true,
		};
	}
}

/**
 * Format bytes to human-readable string
 */
function formatBytes(bytes: number): string {
	if (bytes < 1024) return `${bytes}B`;
	if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
	return `${(bytes / (1024 * 1024)).toFixed(2)}MB`;
}

/**
 * Main execution
 */
async function main() {
	console.log("┌─────────────────────────────────────────────────────────────┐");
	console.log("│                    Image Optimization                        │");
	console.log("└─────────────────────────────────────────────────────────────┘");
	console.log("");
	console.log(`  Settings:`);
	console.log(`    PNG Quality: ${PNG_QUALITY}/100, Compression: ${PNG_COMPRESSION}/9`);
	console.log(`    JPEG Quality: ${JPEG_QUALITY}/100 (mozjpeg)`);
	console.log(`    Directory: ${IMAGES_DIR}`);
	if (DRY_RUN) console.log(`    Mode: DRY RUN (no files modified)`);
	console.log("");

	// Get files to process
	let files: string[];
	if (SINGLE_FILE) {
		files = [SINGLE_FILE];
		console.log(`  Testing single file: ${SINGLE_FILE}`);
	} else {
		files = await getAllImageFiles(IMAGES_DIR);
		console.log(`  Found ${files.length} images to process`);
	}
	console.log("");

	// Process files
	const results: OptimizationResult[] = [];
	let processed = 0;

	for (const file of files) {
		const result = await optimizeImage(file);
		results.push(result);

		const shortPath = file.replace(IMAGES_DIR + "/", "").replace("./public/images/", "");

		if (result.skipped) {
			if (VERBOSE) {
				console.log(`  - ${shortPath}: already optimal`);
			}
		} else {
			console.log(
				`  ✓ ${shortPath}: ${formatBytes(result.originalSize)} → ${formatBytes(result.newSize)} (${result.savingsPercent.toFixed(1)}%)`
			);
		}

		processed++;
		if (!SINGLE_FILE && !VERBOSE && processed % 25 === 0) {
			console.log(`    ... ${processed}/${files.length} processed`);
		}
	}

	// Summary
	console.log("");
	console.log("┌─────────────────────────────────────────────────────────────┐");
	console.log("│                         Summary                              │");
	console.log("└─────────────────────────────────────────────────────────────┘");

	const totalOriginal = results.reduce((sum, r) => sum + r.originalSize, 0);
	const totalNew = results.reduce((sum, r) => sum + r.newSize, 0);
	const totalSavings = totalOriginal - totalNew;
	const filesOptimized = results.filter((r) => !r.skipped).length;
	const filesSkipped = results.filter((r) => r.skipped).length;

	console.log(`  Files processed:  ${results.length}`);
	console.log(`  Files optimized:  ${filesOptimized}`);
	console.log(`  Files skipped:    ${filesSkipped} (already optimal)`);
	console.log("");
	console.log(`  Original size:    ${formatBytes(totalOriginal)}`);
	console.log(`  New size:         ${formatBytes(totalNew)}`);
	console.log(`  Total savings:    ${formatBytes(totalSavings)} (${((totalSavings / totalOriginal) * 100).toFixed(1)}%)`);

	if (DRY_RUN) {
		console.log("");
		console.log("  ℹ️  Run without --dry-run to apply optimizations");
	}

	console.log("");
}

main().catch(console.error);

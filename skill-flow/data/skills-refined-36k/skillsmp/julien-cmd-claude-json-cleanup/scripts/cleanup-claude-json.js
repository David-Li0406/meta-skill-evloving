#!/usr/bin/env node
/**
 * Claude JSON Cleanup - Clean oversized ~/.claude.json
 *
 * Removes stale project entries and compacts the file.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const CLAUDE_JSON = path.join(os.homedir(), '.claude.json');
const BACKUP_PATH = path.join(os.homedir(), '.claude.json.backup');

function fileExists(p) {
    try {
        fs.accessSync(p);
        return true;
    } catch {
        return false;
    }
}

function formatBytes(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function main() {
    console.log('🔧 Claude JSON Cleanup\n');

    // Check file exists
    if (!fileExists(CLAUDE_JSON)) {
        console.log('❌ ~/.claude.json not found');
        process.exit(1);
    }

    // Read current file
    const originalContent = fs.readFileSync(CLAUDE_JSON, 'utf-8');
    const originalSize = Buffer.byteLength(originalContent, 'utf-8');
    const config = JSON.parse(originalContent);

    console.log(`📊 Original size: ${formatBytes(originalSize)}`);
    console.log(`   Estimated tokens: ~${Math.round(originalSize / 4)}`);

    // Create backup
    fs.writeFileSync(BACKUP_PATH, originalContent);
    console.log(`\n💾 Backup created: ${BACKUP_PATH}`);

    // Stats
    let removedProjects = 0;
    let removedGithubPaths = 0;

    // 1. Clean stale projects
    if (config.projects && typeof config.projects === 'object') {
        const originalCount = Object.keys(config.projects).length;
        const validProjects = {};

        for (const [projectPath, data] of Object.entries(config.projects)) {
            // Normalize path for Windows
            const normalizedPath = projectPath.replace(/\//g, path.sep);

            if (fileExists(normalizedPath)) {
                validProjects[projectPath] = data;
            } else {
                removedProjects++;
            }
        }

        config.projects = validProjects;
        console.log(`\n🗂️  Projects: ${originalCount} → ${Object.keys(validProjects).length} (removed ${removedProjects} stale)`);
    }

    // 2. Clean stale github repo paths
    if (config.githubRepoPaths && Array.isArray(config.githubRepoPaths)) {
        const originalCount = config.githubRepoPaths.length;
        config.githubRepoPaths = config.githubRepoPaths.filter(p => {
            const normalizedPath = p.replace(/\//g, path.sep);
            const exists = fileExists(normalizedPath);
            if (!exists) removedGithubPaths++;
            return exists;
        });
        console.log(`📁 GitHub paths: ${originalCount} → ${config.githubRepoPaths.length} (removed ${removedGithubPaths} stale)`);
    }

    // 3. Write compacted JSON
    const compactedContent = JSON.stringify(config, null, 2);
    const compactedSize = Buffer.byteLength(compactedContent, 'utf-8');

    fs.writeFileSync(CLAUDE_JSON, compactedContent);

    // Summary
    const savedBytes = originalSize - compactedSize;
    const savedPercent = ((savedBytes / originalSize) * 100).toFixed(1);

    console.log(`\n✅ Cleanup complete!`);
    console.log(`   New size: ${formatBytes(compactedSize)} (saved ${formatBytes(savedBytes)}, ${savedPercent}%)`);
    console.log(`   Estimated tokens: ~${Math.round(compactedSize / 4)}`);

    if (Math.round(compactedSize / 4) > 25000) {
        console.log(`\n⚠️  Still above 25,000 token limit. Consider manual cleanup.`);
    } else {
        console.log(`\n🎉 File is now within safe token limits.`);
    }
}

// Run
try {
    main();
} catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
}

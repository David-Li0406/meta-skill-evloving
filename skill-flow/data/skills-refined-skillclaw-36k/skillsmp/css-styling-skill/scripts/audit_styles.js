#!/usr/bin/env node

/**
 * Style Auditor
 * Scans project for hardcoded hex colors and potential style violations.
 */

const fs = require('fs');
const path = require('path');

// Configuration
const IGNORE_DIRS = ['node_modules', '.next', 'dist', 'build', '.git', 'coverage'];
const EXTENSIONS = ['.tsx', '.ts', '.jsx', '.js', '.css', '.scss'];

// "Allowed" hex codes (The Palette) - to filter out false positives if strict checking
// zinc-950: #09090b
// zinc-900: #18181b
// zinc-800: #27272a
// emerald-500: #10b981
// white: #ffffff, #fff
// black: #000000, #000
const ALLOWED_HEX = new Set([
    '#09090b', '#18181b', '#27272a', '#10b981', '#ffffff', '#fff', '#000000', '#000',
    '#fafafa', '#a1a1aa' // from SKILL.md mobile palette
]);

function getAllFiles(dirPath, arrayOfFiles) {
    const files = fs.readdirSync(dirPath);

    arrayOfFiles = arrayOfFiles || [];

    files.forEach(function(file) {
        const fullPath = path.join(dirPath, file);
        if (fs.statSync(fullPath).isDirectory()) {
            if (!IGNORE_DIRS.includes(file)) {
                arrayOfFiles = getAllFiles(fullPath, arrayOfFiles);
            }
        } else {
            if (EXTENSIONS.includes(path.extname(file))) {
                arrayOfFiles.push(fullPath);
            }
        }
    });

    return arrayOfFiles;
}

function scanFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    let issues = [];

    lines.forEach((line, index) => {
        // Check for Hex Codes
        const hexMatches = line.match(/#[0-9a-fA-F]{3,6}/g);
        if (hexMatches) {
            hexMatches.forEach(hex => {
                if (!ALLOWED_HEX.has(hex.toLowerCase())) {
                    issues.push({
                        line: index + 1,
                        type: 'Hardcoded Hex',
                        value: hex,
                        context: line.trim()
                    });
                }
            });
        }

        // Check for specific "bad" class names (Generic examples)
        // e.g. using 'bg-red-500' when we only use emerald might be a warning, but maybe too noisy.
        // Let's stick to inline styles for React
        if (line.includes('style={{') && (line.includes('color:') || line.includes('background'))) {
             issues.push({
                line: index + 1,
                type: 'Inline Style',
                value: 'style={{...}}',
                context: line.trim()
            });
        }
    });

    return issues;
}

function main() {
    const targetDir = process.argv[2] || '.';
    console.log(`🔍 Scanning styles in standards...`);
    
    // We strictly want to scan 'src' and 'mobile' usually
    const srcFiles = fs.existsSync('src') ? getAllFiles('src') : [];
    const mobileFiles = fs.existsSync('mobile') ? getAllFiles('mobile') : [];
    const allFiles = [...srcFiles, ...mobileFiles];

    let totalIssues = 0;

    allFiles.forEach(file => {
        const issues = scanFile(file);
        if (issues.length > 0) {
            console.log(`\n📄 ${file}`);
            issues.forEach(issue => {
                console.log(`  L${issue.line}: [${issue.type}] ${issue.value}`);
                // console.log(`      ${issue.context.substring(0, 60)}...`);
            });
            totalIssues += issues.length;
        }
    });

    console.log(`\nFound ${totalIssues} potential style issues.`);
}

main();

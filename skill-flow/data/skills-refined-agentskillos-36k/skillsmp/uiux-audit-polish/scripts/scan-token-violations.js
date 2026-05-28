const fs = require('fs');
const path = require('path');

const DIRECTORIES_TO_SCAN = ['src'];
const EXTENSIONS = ['.tsx', '.ts', '.css', '.scss'];

// Regex patterns for violations
const PATTERNS = [
    {
        name: 'Hardcoded Hex Color',
        regex: /#[0-9a-fA-F]{3,6}\b/g,
        suggestion: 'Use a design token (e.g., text-primary, bg-surface)',
        severity: 'High'
    },
    {
        name: 'Non-Zero Radius (Tailwind)',
        regex: /rounded-(sm|md|lg|xl|2xl|3xl)/g,
        suggestion: 'Calm Luxury requires zero-radius (rounded-none). Only pills (rounded-full) are allowed for specific buttons.',
        severity: 'Medium'
    },
    {
        name: 'Hardcoded Pixel Value (>1px)',
        regex: /\b(?!0px|1px)\d+px\b/g,
        suggestion: 'Use spacing tokens (e.g., p-4, h-12) or fluid variables.',
        severity: 'Medium'
    },
    {
        name: 'Legacy Brand Token',
        regex: /\b(text|bg|border|ring|fill|stroke|shadow)-brand-\w+\b/g,
        suggestion: 'Legacy token detected. Use semantic tokens (e.g. action-primary, text-primary).',
        severity: 'High'
    }
];

function getAllFiles(dirPath, arrayOfFiles) {
    const files = fs.readdirSync(dirPath);

    arrayOfFiles = arrayOfFiles || [];

    files.forEach(function (file) {
        if (fs.statSync(dirPath + "/" + file).isDirectory()) {
            arrayOfFiles = getAllFiles(dirPath + "/" + file, arrayOfFiles);
        } else {
            if (EXTENSIONS.includes(path.extname(file))) {
                arrayOfFiles.push(path.join(dirPath, "/", file));
            }
        }
    });

    return arrayOfFiles;
}

function scanFiles() {
    console.log('🔍 Starting Design System Audit...\n');
    let issuesFound = 0;

    try {
        const files = [];
        DIRECTORIES_TO_SCAN.forEach(dir => {
            if (fs.existsSync(dir)) {
                getAllFiles(dir, files);
            }
        });

        files.forEach(file => {
            const content = fs.readFileSync(file, 'utf8');
            const fileIssues = [];

            PATTERNS.forEach(pattern => {
                let match;
                // Reset lastIndex for strict global regex if needed, but simple match is okay here
                // We use string match or exec. 
                // For distinct matches:
                const matches = content.match(pattern.regex);
                if (matches) {
                    // Dedup matches
                    const uniqueMatches = [...new Set(matches)];
                    uniqueMatches.forEach(m => {
                        fileIssues.push({
                            type: pattern.name,
                            value: m,
                            suggestion: pattern.suggestion
                        });
                    });
                }
            });

            if (fileIssues.length > 0) {
                issuesFound += fileIssues.length;
                console.log(`\n📄 ${file}`);
                fileIssues.forEach(issue => {
                    console.log(`   ❌ [${issue.type}] "${issue.value}" -> ${issue.suggestion}`);
                });
            }
        });

        console.log(`\n-----------------------------------`);
        if (issuesFound > 0) {
            console.log(`⚠️  Audit Complete: ${issuesFound} potential violations found.`);
        } else {
            console.log(`✅  Audit Complete: No obvious violations found. Calm Luxury achieved!`);
        }

    } catch (e) {
        console.error("Error scanning files:", e);
    }
}

scanFiles();

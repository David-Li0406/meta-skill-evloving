const fs = require('fs');
const path = require('path');

const DIRECTORIES_TO_SCAN = ['src'];
const EXTENSIONS = ['.tsx', '.ts', '.js'];
const EXCLUDES = ['src/components/ui/shadcn', 'node_modules', '.next']; // Example excludes

const METRICS = {
    MAX_LINES: 300,
    FORBIDDEN_PATTERNS: [
        { name: 'Usage of "any"', regex: /: any/g, severity: 'High' },
        { name: 'Console Log', regex: /console\.log\(/g, severity: 'Low' },
        { name: 'TODO Comment', regex: /\/\/ TODO/g, severity: 'Medium' }
    ]
};

function getAllFiles(dirPath, arrayOfFiles) {
    const files = fs.readdirSync(dirPath);
    arrayOfFiles = arrayOfFiles || [];

    files.forEach(function (file) {
        const fullPath = path.join(dirPath, file);
        if (fs.statSync(fullPath).isDirectory()) {
            if (!EXCLUDES.some(ex => fullPath.includes(ex))) {
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

function scanQuality() {
    console.log('🔍 Starting Code Quality Audit...\n');
    const files = [];
    DIRECTORIES_TO_SCAN.forEach(dir => {
        if (fs.existsSync(dir)) getAllFiles(dir, files);
    });

    let fileIssues = 0;
    let highSeverityFound = false;

    files.forEach(file => {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        const issues = [];

        // Check File Size
        if (lines.length > METRICS.MAX_LINES) {
            issues.push(`⚠️  File too large (${lines.length} lines). Consider splitting.`);
        }

        // Check Patterns
        METRICS.FORBIDDEN_PATTERNS.forEach(pattern => {
            const matches = content.match(pattern.regex);
            if (matches) {
                issues.push(`❌ [${pattern.severity}] Found ${matches.length} "${pattern.name}"`);
                if (pattern.severity === 'High') {
                    highSeverityFound = true;
                }
            }
        });

        if (issues.length > 0) {
            fileIssues++;
            console.log(`\n📄 ${file}`);
            issues.forEach(i => console.log(`   ${i}`));
        }
    });

    console.log(`\n-----------------------------------`);
    console.log(`📊 Audit Complete. Issues found in ${fileIssues} files.`);

    if (highSeverityFound) {
        console.error('\n❌ [Critical] High severity issues detected. Build blocked.');
        process.exit(1);
    }
}

scanQuality();

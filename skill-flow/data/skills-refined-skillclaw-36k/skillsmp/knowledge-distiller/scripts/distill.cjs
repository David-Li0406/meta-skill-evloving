const fs = require('fs');
const path = require('path');

const inputFile = process.argv[2];
if (!inputFile) {
    console.error("Usage: node distill.cjs <path/to/summary.md>");
    process.exit(1);
}

const kbRoot = path.join(__dirname, '../../../../KB');

// 1. Scan KB Structure (Helper to find existing links)
function scanKB(dir, prefix = '') {
    let structure = [];
    const items = fs.readdirSync(dir, { withFileTypes: true });

    for (const item of items) {
        if (item.isDirectory() && !item.name.startsWith('.')) {
            structure.push(`${prefix}${item.name}/`);
            structure.push(...scanKB(path.join(dir, item.name), `${prefix}  `));
        } else if (item.isFile() && item.name.endsWith('.md')) {
            structure.push(`${prefix}${item.name}`);
        }
    }
    return structure;
}

let kbStructure = [];
try {
    kbStructure = scanKB(kbRoot);
} catch (e) {
    kbStructure = ["Error scanning KB: " + e.message];
}

// 2. Read Source
const sourceContent = fs.readFileSync(inputFile, 'utf-8');

// 3. Generate Architect Template
const template = `---
tags: #knowledge/topic #status/incubating
created: ${new Date().toISOString().split('T')[0]}
intention: "..." 
related_projects: [Project A](../path/to/A.md), [Project B](../path/to/B.md)
---

# [Topic Name]

## 1. Executive Summary (ELI5)
...
`;

// 4. Output
console.log(JSON.stringify({
    role: "Senior Knowledge Architect & Technical Writer",
    objective: "Transform raw research into a 'Source of Truth' PKB note.",
    strategy: "Intention-Based Distillation",
    rules: [
        "1. DEDUCE INTENTION: Ask 'What is this?'. (e.g. Identity/Bio -> TELOS.md; Role -> Personas/; Tool -> Tools/; Guide -> Guides/).",
        "2. SORT ACCORDINGLY: Use Intention to pick folder OR specific file (like TELOS.md) to update.",
        "3. COMPLETENESS: Ensure all quadrants covered.",
        "4. LINKING: Use standard Markdown links `[label](path)`."
    ],
    kb_map: kbStructure,
    template: template,
    source_preview: sourceContent.substring(0, 500) + "..."
}, null, 2));

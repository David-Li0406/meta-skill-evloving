const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const dotenvx = require('@dotenvx/dotenvx');

// Load env quietly
const envPath = path.join(__dirname, '../../../../.env');
dotenvx.config({ path: envPath, quiet: true });

const topic = process.argv[2];
// depth now controls how many references we verify/summarize
const depth = parseInt(process.argv[4] || 3);

if (!topic) {
    console.error("Usage: node research.cjs \"Topic\" --depth <number>");
    process.exit(1);
}

const FASTGPT_SCRIPT = path.join(__dirname, 'fastgpt.cjs');
const SUMMARIZE_SCRIPT = path.join(__dirname, 'summarize.cjs');
const OUTPUT_DIR = path.join(__dirname, '../../../../KB/Summaries');

if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Cost Safeguard
if (!process.argv.includes('--confirm')) {
    console.warn("⚠️  KAGI DEEP RESEARCH COST WARNING ⚠️");
    console.warn(`   This operation will perform:`);
    console.warn(`   - 1 FastGPT Query`);
    console.warn(`   - Up to ${depth} Summarization calls`);
    console.warn(`   Estimated Cost: High (Credits)`);
    console.warn("");
    console.warn("   To proceed, please re-run the command with the '--confirm' flag.");
    process.exit(0);
}

// 1. FastGPT "Deep Search"
console.error(`[1/2] Researching "${topic}" with FastGPT...`);
let fastGptResult = {};

try {
    const output = execSync(`node "${FASTGPT_SCRIPT}" "${topic}"`, { encoding: 'utf-8' });
    // robustness: extract JSON
    const jsonStart = output.indexOf('{');
    const jsonEnd = output.lastIndexOf('}') + 1;
    if (jsonStart === -1) {
        throw new Error("Invalid Output from FastGPT");
    }
    fastGptResult = JSON.parse(output.substring(jsonStart, jsonEnd));
} catch (e) {
    console.error("Research failed:", e.message);
    process.exit(1);
}

// 2. Generate Report
console.error(`[2/2] Generating Report...`);

let reportContent = `# Research Report: ${topic}\n\n`;
reportContent += `**Date:** ${new Date().toISOString().split('T')[0]}\n`;
reportContent += `**Method:** Kagi FastGPT + Recursive Summarization\n\n`;

reportContent += `## Executive Summary\n\n${fastGptResult.output || 'No summary available.'}\n\n`;

if (fastGptResult.references && fastGptResult.references.length > 0) {
    reportContent += `## Key Sources & Details\n\n`;

    // Process top references based on depth
    const refsToProcess = fastGptResult.references.slice(0, depth);

    for (const [i, ref] of refsToProcess.entries()) {
        console.error(`  - Verifying Source (${i + 1}/${refsToProcess.length}): ${ref.title}`);
        reportContent += `### ${i + 1}. [${ref.title}](${ref.url})\n\n`;
        reportContent += `> ${ref.snippet || 'No snippet provided.'}\n\n`;

        // Optional: Run full summarizer on the reference URL for "verification"
        try {
            const extraSummary = execSync(`node "${SUMMARIZE_SCRIPT}" --url "${ref.url}"`, { encoding: 'utf-8', stdio: ['ignore', 'pipe', 'ignore'] });
            if (extraSummary && extraSummary.length > 20) {
                reportContent += `**Deep Dive:**\n${extraSummary.trim()}\n\n`;
            }
        } catch (e) {
            reportContent += `*(Deep summary unavailable)*\n\n`;
        }
        reportContent += `---\n\n`;
    }
}

// 3. Save
const filename = `${topic.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_research.md`;
const outputPath = path.join(OUTPUT_DIR, filename);

fs.writeFileSync(outputPath, reportContent);
console.error(`Research Complete. Report saved to:`);
console.log(outputPath);

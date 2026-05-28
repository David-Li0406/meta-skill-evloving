#!/usr/bin/env node
/**
 * Skill Validation Script
 * Validates the structure and consistency of the WordPress Gutenberg Expert skill
 */

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(__dirname, '..');
const AGENTS_DIR = path.join(SKILL_DIR, 'agents');

let errors = [];
let warnings = [];

/**
 * Check if a file exists
 */
function fileExists(filePath) {
    return fs.existsSync(filePath);
}

/**
 * Read file content
 */
function readFile(filePath) {
    return fs.readFileSync(filePath, 'utf-8');
}

/**
 * Validate SKILL.md frontmatter
 */
function validateSkillMd() {
    const skillPath = path.join(SKILL_DIR, 'SKILL.md');

    if (!fileExists(skillPath)) {
        errors.push('SKILL.md not found');
        return;
    }

    const content = readFile(skillPath);

    // Check frontmatter
    if (!content.startsWith('---')) {
        errors.push('SKILL.md: Missing YAML frontmatter');
        return;
    }

    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (!frontmatterMatch) {
        errors.push('SKILL.md: Invalid frontmatter format');
        return;
    }

    const frontmatter = frontmatterMatch[1];

    // Check required fields
    if (!frontmatter.includes('name:')) {
        errors.push('SKILL.md: Missing "name" in frontmatter');
    }
    if (!frontmatter.includes('description:')) {
        errors.push('SKILL.md: Missing "description" in frontmatter');
    }

    console.log('✓ SKILL.md frontmatter validated');
}

/**
 * Validate all agent files exist
 */
function validateAgentStructure() {
    const expectedDomains = [
        'wp-core',
        'gutenberg-blocks',
        'tooling',
        'design',
        'theme',
        'testing'
    ];

    for (const domain of expectedDomains) {
        const domainPath = path.join(AGENTS_DIR, domain);

        if (!fileExists(domainPath)) {
            errors.push(`Missing domain directory: agents/${domain}`);
            continue;
        }

        // Check for orchestrator
        const orchestratorPath = path.join(domainPath, 'orchestrator.md');
        if (!fileExists(orchestratorPath)) {
            warnings.push(`Missing orchestrator: agents/${domain}/orchestrator.md`);
        }
    }

    console.log('✓ Agent structure validated');
}

/**
 * Validate agent file format
 */
function validateAgentFiles() {
    function walkDir(dir) {
        const files = fs.readdirSync(dir);

        for (const file of files) {
            const filePath = path.join(dir, file);
            const stat = fs.statSync(filePath);

            if (stat.isDirectory()) {
                walkDir(filePath);
            } else if (file.endsWith('.md')) {
                validateAgentFile(filePath);
            }
        }
    }

    walkDir(AGENTS_DIR);
    console.log('✓ Agent files validated');
}

/**
 * Validate individual agent file
 */
function validateAgentFile(filePath) {
    const relativePath = path.relative(SKILL_DIR, filePath);
    const content = readFile(filePath);

    // Check for title (H1)
    if (!content.match(/^# .+/m)) {
        warnings.push(`${relativePath}: Missing H1 title`);
    }

    // Check for "Ton Domaine" or "Domaine" section
    if (!content.includes('## Ton Domaine') &&
        !content.includes('## Domaine') &&
        !content.includes('## Agents Disponibles')) {
        warnings.push(`${relativePath}: Missing domain/agents section`);
    }

    // Check for "Sources" section in non-orchestrator files
    if (!filePath.includes('orchestrator') && !content.includes('## Sources')) {
        // Just a note, not required
    }

    // Check for code examples in non-orchestrator files
    if (!filePath.includes('orchestrator') && !content.includes('```')) {
        warnings.push(`${relativePath}: No code examples found`);
    }
}

/**
 * Validate documentation files
 */
function validateDocs() {
    const docsDir = path.join(SKILL_DIR, 'docs');

    if (!fileExists(docsDir)) {
        warnings.push('docs/ directory not found');
        return;
    }

    const expectedDocs = [
        'getting-started.md',
        'troubleshooting.md',
        'migration-guide.md'
    ];

    for (const doc of expectedDocs) {
        const docPath = path.join(docsDir, doc);
        if (!fileExists(docPath)) {
            warnings.push(`Missing documentation: docs/${doc}`);
        }
    }

    console.log('✓ Documentation validated');
}

/**
 * Validate CHANGELOG
 */
function validateChangelog() {
    const changelogPath = path.join(SKILL_DIR, 'CHANGELOG.md');

    if (!fileExists(changelogPath)) {
        warnings.push('CHANGELOG.md not found');
        return;
    }

    const content = readFile(changelogPath);

    // Check for version entries
    if (!content.match(/## \[\d+\.\d+\.\d+\]/)) {
        warnings.push('CHANGELOG.md: No version entries found');
    }

    console.log('✓ CHANGELOG validated');
}

/**
 * Count agents
 */
function countAgents() {
    let count = 0;

    function walkDir(dir) {
        const files = fs.readdirSync(dir);

        for (const file of files) {
            const filePath = path.join(dir, file);
            const stat = fs.statSync(filePath);

            if (stat.isDirectory()) {
                walkDir(filePath);
            } else if (file.endsWith('.md') && !file.includes('orchestrator')) {
                count++;
            }
        }
    }

    walkDir(AGENTS_DIR);

    // Add direct agents
    const directAgents = [
        'wp-rest-api-expert.md',
        'gdpr-consent-api.md',
        'i18n-localization.md',
        'seo-expert.md',
        'accessibility-expert.md'
    ];

    for (const agent of directAgents) {
        if (fileExists(path.join(AGENTS_DIR, agent))) {
            count++;
        }
    }

    return count;
}

/**
 * Main validation
 */
function main() {
    console.log('🔍 Validating WordPress Gutenberg Expert skill...\n');

    validateSkillMd();
    validateAgentStructure();
    validateAgentFiles();
    validateDocs();
    validateChangelog();

    const agentCount = countAgents();
    console.log(`\n📊 Total agents: ${agentCount}`);

    console.log('\n' + '='.repeat(50));

    if (errors.length > 0) {
        console.log('\n❌ ERRORS:');
        errors.forEach(e => console.log(`   - ${e}`));
    }

    if (warnings.length > 0) {
        console.log('\n⚠️  WARNINGS:');
        warnings.forEach(w => console.log(`   - ${w}`));
    }

    if (errors.length === 0 && warnings.length === 0) {
        console.log('\n✅ All validations passed!');
    }

    console.log('\n' + '='.repeat(50));

    // Exit with error if there are errors
    if (errors.length > 0) {
        process.exit(1);
    }
}

main();

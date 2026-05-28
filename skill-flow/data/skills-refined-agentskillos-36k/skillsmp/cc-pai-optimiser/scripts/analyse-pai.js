#!/usr/bin/env node
/**
 * analyze-pai.js
 * Comprehensive PAI repository analysis against 12-factor principles
 *
 * Usage: bun run scripts/analyze-pai.js [pai-path]
 */

import { execSync } from 'child_process';
import { existsSync, readFileSync, readdirSync, statSync } from 'fs';
import { join, relative } from 'path';

// Analysis categories (updated for PAI v2.1.x)
const ANALYSIS_MODULES = {
    structure: analyzeStructure,
    contextManagement: analyzeContextManagement,
    skillsSystem: analyzeSkillsSystem,
    hooksConfiguration: analyzeHooksConfiguration,
    agentConfiguration: analyzeAgentConfiguration,
    toolIntegration: analyzeToolIntegration,
    workflowPatterns: analyzeWorkflowPatterns,
    delegationPatterns: analyzeDelegationPatterns
};

// Analyze PAI directory structure
function analyzeStructure(paiPath) {
    const results = {
        score: 0,
        maxScore: 10,
        findings: [],
        recommendations: []
    };

    const expectedDirs = [
        { path: '.claude', required: true, weight: 2 },
        { path: '.claude/context', required: true, weight: 2 },
        { path: '.claude/skills', required: false, weight: 2 },  // PAI v2.x skills (replaces .claude/rules)
        { path: '.claude/agents', required: false, weight: 1 },
        { path: '.claude/commands', required: false, weight: 1 },
        { path: '.claude/hooks', required: false, weight: 1 },
        { path: '.claude/state', required: false, weight: 1 }    // State persistence
    ];

    for (const dir of expectedDirs) {
        const fullPath = join(paiPath, dir.path);
        if (existsSync(fullPath)) {
            results.score += dir.weight;
            results.findings.push(`✅ ${dir.path} exists`);
        } else if (dir.required) {
            results.findings.push(`❌ ${dir.path} MISSING (required)`);
            results.recommendations.push(`Create ${dir.path} directory for proper PAI structure`);
        } else {
            results.findings.push(`⚪ ${dir.path} not present (optional)`);
        }
    }

    // Check for CLAUDE.md files
    const claudeFiles = findFiles(paiPath, 'CLAUDE.md');
    results.findings.push(`📄 Found ${claudeFiles.length} CLAUDE.md files`);
    if (claudeFiles.length === 0) {
        results.recommendations.push('Create at least one CLAUDE.md file for context configuration');
    }

    return results;
}

// Analyze context management patterns
function analyzeContextManagement(paiPath) {
    const results = {
        score: 0,
        maxScore: 20,
        findings: [],
        recommendations: []
    };

    const contextPath = join(paiPath, '.claude', 'context');

    if (!existsSync(contextPath)) {
        results.findings.push('❌ No context directory found');
        results.recommendations.push('Implement UFC (Universal File-based Context) system');
        return results;
    }

    results.score += 5;

    // Analyze context file sizes
    const contextFiles = findFiles(contextPath, '*.md');
    let oversizedFiles = 0;
    let totalLines = 0;

    for (const file of contextFiles) {
        const content = readFileSync(file, 'utf-8');
        const lines = content.split('\n').length;
        totalLines += lines;

        if (lines > 500) {
            oversizedFiles++;
            results.findings.push(`⚠️  ${relative(paiPath, file)}: ${lines} lines (exceeds 500 limit)`);
        }
    }

    if (oversizedFiles === 0 && contextFiles.length > 0) {
        results.score += 5;
        results.findings.push(`✅ All context files under 500 lines`);
    } else if (oversizedFiles > 0) {
        results.recommendations.push(`Split ${oversizedFiles} oversized context files using progressive disclosure pattern`);
    }

    // Check for progressive disclosure patterns
    const hasReferences = existsSync(join(contextPath, 'references')) ||
        contextFiles.some(f => readFileSync(f, 'utf-8').includes('See '));
    if (hasReferences) {
        results.score += 5;
        results.findings.push('✅ Progressive disclosure pattern detected');
    } else {
        results.recommendations.push('Implement progressive disclosure with references/ directory');
    }

    // Check for context loading enforcement (context files + SKILL.md files)
    const skillsPath = join(paiPath, '.claude', 'skills');
    const skillFiles = existsSync(skillsPath) ? findFiles(skillsPath, 'SKILL.md') : [];
    const allContextFiles = [...contextFiles, ...skillFiles];

    const hasEnforcement = allContextFiles.some(f => {
        const content = readFileSync(f, 'utf-8');
        return content.includes('MANDATORY') ||
               content.includes('MUST') ||
               content.includes('READ THESE FILES') ||
               content.includes('→ READ:') ||  // PAI routing pattern
               content.includes('READ:');      // Alternate routing pattern
    });

    if (hasEnforcement) {
        results.score += 5;
        results.findings.push('✅ Context loading enforcement detected');
    } else {
        results.recommendations.push('Add context loading enforcement (e.g., "→ READ:" routing, "MUST", or "MANDATORY" directives)');
    }

    return results;
}

// Analyze skills system (PAI v2.x)
function analyzeSkillsSystem(paiPath) {
    const results = {
        score: 0,
        maxScore: 25,
        findings: [],
        recommendations: []
    };

    const skillsPath = join(paiPath, '.claude', 'skills');
    const rulesPath = join(paiPath, '.claude', 'rules'); // Legacy

    // Check for legacy rules vs modern skills
    if (existsSync(rulesPath) && !existsSync(skillsPath)) {
        results.findings.push('⚠️  Using legacy .claude/rules/ - consider migrating to .claude/skills/');
        results.recommendations.push('Migrate from .claude/rules/ to .claude/skills/ for PAI v2.x compatibility');
    }

    if (!existsSync(skillsPath)) {
        results.findings.push('⚪ No skills directory (skills are optional but powerful)');
        results.recommendations.push('Create .claude/skills/ to define reusable, invocable capabilities');
        return results;
    }

    results.score += 5;
    results.findings.push('✅ Skills directory exists');

    // Analyze each skill
    const skillDirs = readdirSync(skillsPath, { withFileTypes: true })
        .filter(d => d.isDirectory())
        .map(d => d.name);

    results.findings.push(`📦 Found ${skillDirs.length} skill(s)`);

    let wellFormedSkills = 0;
    let hasInvocableSkill = false;
    let hasForkContextSkill = false;

    for (const skillDir of skillDirs) {
        const skillMdPath = join(skillsPath, skillDir, 'SKILL.md');

        if (!existsSync(skillMdPath)) {
            results.findings.push(`⚠️  ${skillDir}/ missing SKILL.md`);
            results.recommendations.push(`Add SKILL.md to ${skillDir}/ with proper frontmatter`);
            continue;
        }

        const content = readFileSync(skillMdPath, 'utf-8');

        // Check for proper frontmatter
        const hasFrontmatter = content.startsWith('---');
        const hasName = /^name:\s*.+/m.test(content);
        const hasDescription = /^description:\s*.+/m.test(content);
        const hasContext = /^context:\s*(fork|same)/m.test(content);

        if (hasFrontmatter && hasName) {
            wellFormedSkills++;

            // Check context type
            if (/context:\s*fork/m.test(content)) {
                hasForkContextSkill = true;
                results.findings.push(`✅ ${skillDir}: fork context (subagent)`);
            } else {
                results.findings.push(`✅ ${skillDir}: same context`);
            }

            // Check for invocability (user-invocable commands)
            if (/invocable|user-invocable|slash command/i.test(content)) {
                hasInvocableSkill = true;
            }
        } else {
            const issues = [];
            if (!hasFrontmatter) issues.push('missing frontmatter');
            if (!hasName) issues.push('missing name');
            results.findings.push(`⚠️  ${skillDir}: ${issues.join(', ')}`);
        }

        // Check for proper skill structure
        const hasReferences = existsSync(join(skillsPath, skillDir, 'references'));
        const hasScripts = existsSync(join(skillsPath, skillDir, 'scripts'));
        const hasWorkflows = existsSync(join(skillsPath, skillDir, 'workflows'));

        if (hasReferences || hasScripts || hasWorkflows) {
            results.findings.push(`  └─ Has: ${[hasReferences && 'references', hasScripts && 'scripts', hasWorkflows && 'workflows'].filter(Boolean).join(', ')}`);
        }
    }

    // Score based on skill quality
    if (wellFormedSkills === skillDirs.length && skillDirs.length > 0) {
        results.score += 10;
        results.findings.push('✅ All skills have proper SKILL.md format');
    } else if (wellFormedSkills > 0) {
        results.score += 5;
    }

    if (hasForkContextSkill) {
        results.score += 5;
        results.findings.push('✅ Has fork-context skills (isolated execution)');
    }

    if (hasInvocableSkill) {
        results.score += 5;
        results.findings.push('✅ Has user-invocable skills');
    } else {
        results.recommendations.push('Consider making skills user-invocable with Skill tool');
    }

    return results;
}

// Analyze hooks configuration
function analyzeHooksConfiguration(paiPath) {
    const results = {
        score: 0,
        maxScore: 20,
        findings: [],
        recommendations: []
    };

    const hooksDir = join(paiPath, '.claude', 'hooks');
    const settingsPath = join(paiPath, '.claude', 'settings.json');

    // Check for hooks directory (scripts)
    let hasHooksDir = false;
    let hookScripts = [];
    if (existsSync(hooksDir)) {
        hasHooksDir = true;
        hookScripts = readdirSync(hooksDir).filter(f => f.endsWith('.ts') || f.endsWith('.js') || f.endsWith('.sh'));
        results.findings.push(`📁 Hooks directory: ${hookScripts.length} script(s)`);
    }

    // Check settings.json for hooks configuration (CC 2.1.x)
    if (existsSync(settingsPath)) {
        try {
            const settings = JSON.parse(readFileSync(settingsPath, 'utf-8'));

            if (settings.hooks && typeof settings.hooks === 'object') {
                const hookEvents = Object.keys(settings.hooks);
                results.score += 10;
                results.findings.push(`✅ Hooks configured in settings.json: ${hookEvents.join(', ')}`);

                // Analyze hook event coverage
                const recommendedEvents = ['PreToolUse', 'PostToolUse', 'SessionStart', 'SessionEnd', 'UserPromptSubmit'];
                const missingEvents = recommendedEvents.filter(e => !hookEvents.includes(e));

                if (missingEvents.length === 0) {
                    results.score += 5;
                    results.findings.push('✅ All recommended hook events configured');
                } else if (missingEvents.length < 3) {
                    results.score += 2;
                    results.findings.push(`⚪ Optional hook events not configured: ${missingEvents.join(', ')}`);
                }

                // Check for specific patterns
                const hasPreToolHooks = hookEvents.includes('PreToolUse');
                const hasSessionHooks = hookEvents.includes('SessionStart') || hookEvents.includes('SessionEnd');

                if (hasPreToolHooks) {
                    results.findings.push('✅ PreToolUse hooks enabled (event capture/validation)');
                }
                if (hasSessionHooks) {
                    results.findings.push('✅ Session lifecycle hooks enabled');
                }

            } else {
                results.findings.push('⚪ No hooks configured in settings.json');
                results.recommendations.push('Configure hooks in settings.json for CC 2.1.x automation');
            }

            // Check for statusLine (related to hooks/automation)
            if (settings.statusLine) {
                results.score += 5;
                results.findings.push('✅ Status line configured');
            }

        } catch (e) {
            results.findings.push('⚠️  Could not parse settings.json');
        }
    } else {
        results.findings.push('❌ No settings.json found');
        results.recommendations.push('Create settings.json with hooks configuration');
    }

    // Check for legacy hooks.json (deprecated)
    const legacyHooksJson = join(paiPath, '.claude', 'hooks.json');
    if (existsSync(legacyHooksJson)) {
        results.findings.push('⚠️  Legacy hooks.json detected - migrate to settings.json');
        results.recommendations.push('Migrate hooks.json to settings.json hooks section');
    }

    return results;
}

// Analyze delegation patterns (multi-agent)
function analyzeDelegationPatterns(paiPath) {
    const results = {
        score: 0,
        maxScore: 15,
        findings: [],
        recommendations: []
    };

    // Search for delegation patterns in CLAUDE.md files and context
    const allMdFiles = findFiles(paiPath, '*.md');

    let hasDelegationGuide = false;
    let hasParallelPatterns = false;
    let hasAgentHierarchy = false;

    for (const file of allMdFiles) {
        const content = readFileSync(file, 'utf-8').toLowerCase();
        const relativePath = relative(paiPath, file);

        // Check for delegation guide
        if (relativePath.includes('delegation') || content.includes('delegation-guide')) {
            hasDelegationGuide = true;
            results.findings.push(`✅ Delegation guide: ${relativePath}`);
        }

        // Check for parallel agent patterns
        if (content.includes('parallel') && (content.includes('agent') || content.includes('task tool'))) {
            hasParallelPatterns = true;
        }

        // Check for agent hierarchy documentation
        if (content.includes('agent-guide') || content.includes('agent hierarchy') || content.includes('orchestrator')) {
            hasAgentHierarchy = true;
        }
    }

    if (hasDelegationGuide) {
        results.score += 5;
    } else {
        results.recommendations.push('Create delegation guide for multi-agent workflows');
    }

    if (hasParallelPatterns) {
        results.score += 5;
        results.findings.push('✅ Parallel agent patterns documented');
    } else {
        results.recommendations.push('Document parallel agent execution patterns');
    }

    if (hasAgentHierarchy) {
        results.score += 5;
        results.findings.push('✅ Agent hierarchy/roles documented');
    } else {
        results.recommendations.push('Define agent hierarchy and escalation paths');
    }

    // Check for Task tool patterns in commands
    const commandsDir = join(paiPath, '.claude', 'commands');
    if (existsSync(commandsDir)) {
        const commands = readdirSync(commandsDir).filter(f => f.endsWith('.md'));
        let commandsWithDelegation = 0;

        for (const cmd of commands) {
            const content = readFileSync(join(commandsDir, cmd), 'utf-8');
            if (content.includes('Task tool') || content.includes('subagent') || content.includes('parallel')) {
                commandsWithDelegation++;
            }
        }

        if (commandsWithDelegation > 0) {
            results.findings.push(`✅ ${commandsWithDelegation} command(s) use delegation patterns`);
        }
    }

    return results;
}

// Analyze agent configuration
function analyzeAgentConfiguration(paiPath) {
    const results = {
        score: 0,
        maxScore: 15,
        findings: [],
        recommendations: []
    };

    const agentsPath = join(paiPath, '.claude', 'agents');

    if (!existsSync(agentsPath)) {
        results.findings.push('⚪ No agents directory (agents are optional)');
        return results;
    }

    const agentFiles = readdirSync(agentsPath).filter(f => f.endsWith('.md'));
    results.findings.push(`📄 Found ${agentFiles.length} agent definitions`);

    if (agentFiles.length > 0) {
        results.score += 5;
    }

    // Check agent specialization (Factor 10)
    const generalPurposeIndicators = ['general', 'main', 'default', 'master'];
    let specializedCount = 0;

    for (const file of agentFiles) {
        const name = file.toLowerCase();
        const isSpecialized = !generalPurposeIndicators.some(ind => name.includes(ind));
        if (isSpecialized) {
            specializedCount++;
            results.findings.push(`✅ Specialized agent: ${file}`);
        } else {
            results.findings.push(`⚠️  General-purpose agent: ${file}`);
        }
    }

    if (specializedCount === agentFiles.length && agentFiles.length > 0) {
        results.score += 5;
        results.findings.push('✅ All agents are specialized (Factor 10 compliant)');
    } else if (agentFiles.length > 0) {
        results.recommendations.push('Split general-purpose agents into specialized, single-purpose agents');
    }

    // Check agent file sizes
    let oversizedAgents = 0;
    for (const file of agentFiles) {
        const content = readFileSync(join(agentsPath, file), 'utf-8');
        if (content.split('\n').length > 500) {
            oversizedAgents++;
        }
    }

    if (oversizedAgents === 0 && agentFiles.length > 0) {
        results.score += 5;
        results.findings.push('✅ All agent configs under 500 lines');
    } else if (oversizedAgents > 0) {
        results.recommendations.push(`Refactor ${oversizedAgents} oversized agent configurations`);
    }

    return results;
}

// Analyze tool integration
function analyzeToolIntegration(paiPath) {
    const results = {
        score: 0,
        maxScore: 10,
        findings: [],
        recommendations: []
    };

    // Check for MCP tools documentation
    const toolsContext = join(paiPath, '.claude', 'context', 'tools');
    if (existsSync(toolsContext)) {
        results.score += 5;
        results.findings.push('✅ Tools context documentation exists');
    } else {
        results.findings.push('⚪ No tools context directory (optional)');
    }

    // Check for MCP server configurations
    const settingsPath = join(paiPath, '.claude', 'settings.json');
    if (existsSync(settingsPath)) {
        try {
            const settings = JSON.parse(readFileSync(settingsPath, 'utf-8'));
            if (settings.enabledMcpjsonServers || settings.enableAllProjectMcpServers) {
                results.score += 5;
                results.findings.push('✅ MCP server configuration present');
            }
        } catch { /* ignore */ }
    }

    return results;
}

// Analyze workflow patterns
function analyzeWorkflowPatterns(paiPath) {
    const results = {
        score: 0,
        maxScore: 20,
        findings: [],
        recommendations: []
    };

    // Check for commands
    const commandsPath = join(paiPath, '.claude', 'commands');
    if (existsSync(commandsPath)) {
        const commands = readdirSync(commandsPath).filter(f => f.endsWith('.md'));
        results.score += 5;
        results.findings.push(`✅ Found ${commands.length} command workflows`);

        // Analyze command structure
        for (const cmd of commands.slice(0, 5)) { // Check first 5
            const content = readFileSync(join(commandsPath, cmd), 'utf-8');
            const hasSteps = content.includes('##') || content.includes('1.') || content.includes('Step');
            if (!hasSteps) {
                results.findings.push(`⚠️  Command '${cmd}' lacks step structure`);
            }
        }
    } else {
        results.findings.push('⚪ No commands directory');
        results.recommendations.push('Create reusable workflows in .claude/commands/');
    }

    // Check for hooks (Factor 6 - Launch/Pause/Resume)
    const hooksPath = join(paiPath, '.claude', 'hooks');
    if (existsSync(hooksPath)) {
        const hooks = readdirSync(hooksPath);
        results.score += 5;
        results.findings.push(`✅ Found ${hooks.length} automation hooks`);
    } else {
        results.recommendations.push('Add hooks for event-based automation');
    }

    // Check for working directory (Factor 5 - Unified State)
    const workingPath = join(paiPath, '.claude', 'context', 'working');
    if (existsSync(workingPath)) {
        results.score += 5;
        results.findings.push('✅ Working directory for active state exists');
    } else {
        results.recommendations.push('Create .claude/context/working/ for unified execution state');
    }

    // Check for control flow patterns (Factor 8)
    const allFiles = findFiles(paiPath, '*.md');
    const hasControlFlow = allFiles.some(f => {
        const content = readFileSync(f, 'utf-8');
        return content.includes('workflow') || content.includes('pipeline') || content.includes('if ') || content.includes('loop');
    });

    if (hasControlFlow) {
        results.score += 5;
        results.findings.push('✅ Custom control flow patterns detected');
    } else {
        results.recommendations.push('Define explicit control flow in command files');
    }

    return results;
}

// Helper: Find files matching pattern
function findFiles(dir, pattern, results = []) {
    if (!existsSync(dir)) return results;

    const files = readdirSync(dir);
    for (const file of files) {
        const fullPath = join(dir, file);
        const stat = statSync(fullPath);

        if (stat.isDirectory()) {
            findFiles(fullPath, pattern, results);
        } else if (pattern === '*' || file.endsWith(pattern.replace('*', '')) || file === pattern) {
            results.push(fullPath);
        }
    }

    return results;
}

// Generate full report
function generateReport(paiPath) {
    const report = {
        timestamp: new Date().toISOString(),
        paiPath: paiPath,
        modules: {},
        totalScore: 0,
        maxScore: 0,
        recommendations: []
    };

    for (const [name, analyzer] of Object.entries(ANALYSIS_MODULES)) {
        const result = analyzer(paiPath);
        report.modules[name] = result;
        report.totalScore += result.score;
        report.maxScore += result.maxScore;
        report.recommendations.push(...result.recommendations.map(r => ({ module: name, recommendation: r })));
    }

    report.compliancePercentage = Math.round((report.totalScore / report.maxScore) * 100);

    return report;
}

// Format report for console
function formatReport(report) {
    const lines = [];

    lines.push('\n╔══════════════════════════════════════════════════════════════╗');
    lines.push('║              PAI OPTIMIZATION ANALYSIS                       ║');
    lines.push('╚══════════════════════════════════════════════════════════════╝\n');

    lines.push(`📅 Generated: ${report.timestamp}`);
    lines.push(`📁 PAI Path: ${report.paiPath}`);
    lines.push(`📊 Overall Score: ${report.totalScore}/${report.maxScore} (${report.compliancePercentage}%)\n`);

    // Score bar
    const filled = Math.round(report.compliancePercentage / 5);
    const bar = '█'.repeat(filled) + '░'.repeat(20 - filled);
    lines.push(`Progress: [${bar}] ${report.compliancePercentage}%\n`);

    // Module details
    for (const [name, result] of Object.entries(report.modules)) {
        lines.push(`─── ${name.toUpperCase()} (${result.score}/${result.maxScore}) ───`);
        for (const finding of result.findings) {
            lines.push(`  ${finding}`);
        }
        lines.push('');
    }

    // Recommendations
    if (report.recommendations.length > 0) {
        lines.push('─── RECOMMENDATIONS ──────────────────────────────────────────\n');
        const grouped = {};
        for (const rec of report.recommendations) {
            if (!grouped[rec.module]) grouped[rec.module] = [];
            grouped[rec.module].push(rec.recommendation);
        }

        for (const [module, recs] of Object.entries(grouped)) {
            lines.push(`📌 ${module}:`);
            for (const rec of recs) {
                lines.push(`   • ${rec}`);
            }
            lines.push('');
        }
    }

    return lines.join('\n');
}

// Main execution
async function main() {
    const paiPath = process.argv[2] || process.cwd();

    console.log('Analyzing PAI repository...\n');

    const report = generateReport(paiPath);
    console.log(formatReport(report));

    // Output JSON for programmatic use
    if (process.argv.includes('--json')) {
        console.log('\n─── JSON OUTPUT ──────────────────────────────────────────────\n');
        console.log(JSON.stringify(report, null, 2));
    }
}

main().catch(console.error);
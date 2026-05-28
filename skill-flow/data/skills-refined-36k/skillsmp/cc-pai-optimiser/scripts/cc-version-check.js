#!/usr/bin/env node
/**
 * cc-version-check.js
 * Check Claude Code version compatibility with PAI features
 *
 * Usage: bun run scripts/cc-version-check.js [pai-path]
 */

import { execSync } from 'child_process';
import { existsSync, readFileSync, readdirSync } from 'fs';
import { join } from 'path';

// Feature requirements by CC version (updated 2026-01)
const FEATURE_REQUIREMENTS = {
    // Core features (foundational)
    subagents: { minVersion: '1.0.80', description: 'Parallel task delegation via Task tool' },
    checkpoints: { minVersion: '2.0.0', description: 'Code state snapshots with /rewind' },
    hooks: { minVersion: '1.0.85', description: 'Event-based automation (settings.json hooks config)' },
    skills: { minVersion: '2.0.40', description: 'Reusable skill definitions in .claude/skills/' },
    planMode: { minVersion: '2.0.50', description: 'Structured planning with EnterPlanMode/ExitPlanMode' },

    // CC 2.0.x features
    lsp: { minVersion: '2.0.74', description: 'Language Server Protocol for code intelligence' },
    chromeIntegration: { minVersion: '2.0.72', description: 'Browser control via Chrome extension' },
    desktopApp: { minVersion: '2.0.51', description: 'Native desktop application' },
    vscodeExtension: { minVersion: '2.0.0', description: 'Native VS Code extension' },
    enterpriseSettings: { minVersion: '2.0.53', description: 'Managed enterprise configurations' },

    // CC 2.1.0 features
    modelRouting: { minVersion: '2.1.0', description: 'Per-task model selection (haiku/sonnet/opus)' },
    skillInvocation: { minVersion: '2.1.0', description: 'Skill tool for invoking user-defined skills' },
    backgroundTasks: { minVersion: '2.1.0', description: 'run_in_background parameter for Task tool' },
    taskResume: { minVersion: '2.1.0', description: 'Resume agents via agent ID' },
    statusLine: { minVersion: '2.1.0', description: 'Custom status line via settings.json' },
    settingsJsonHooks: { minVersion: '2.1.0', description: 'Hooks configuration in settings.json (replaces hooks.json)' },
    enhancedSubagents: { minVersion: '2.1.0', description: 'Specialized agent types (Explore, Plan, etc.)' },
    webSearch: { minVersion: '2.1.0', description: 'Built-in WebSearch tool' },
    askUserQuestion: { minVersion: '2.1.0', description: 'Interactive user questions with options' },

    // CC 2.1.3 features
    mergedSkillsCommands: { minVersion: '2.1.3', description: 'Unified slash commands and skills (simplified mental model)' },
    releaseChannelToggle: { minVersion: '2.1.3', description: 'Release channel toggle (stable/latest) in /config' },
    enhancedDoctor: { minVersion: '2.1.3', description: '/doctor detects unreachable permission rules' },
    extendedHookTimeout: { minVersion: '2.1.3', description: 'Hook execution timeout increased to 10 minutes' },

    // CC 2.1.4 features
    disableBackgroundTasks: { minVersion: '2.1.4', description: 'CLAUDE_CODE_DISABLE_BACKGROUND_TASKS env var to disable background tasks' },

    // Provider integrations
    bedrockSupport: { minVersion: '0.2.0', description: 'AWS Bedrock integration' },
    vertexSupport: { minVersion: '0.2.0', description: 'Google Vertex AI integration' }
};

// Parse semver string to comparable array
function parseVersion(version) {
    const clean = version.replace(/^v/, '').split('-')[0];
    return clean.split('.').map(n => parseInt(n, 10) || 0);
}

// Compare two version arrays
function compareVersions(a, b) {
    for (let i = 0; i < Math.max(a.length, b.length); i++) {
        const av = a[i] || 0;
        const bv = b[i] || 0;
        if (av > bv) return 1;
        if (av < bv) return -1;
    }
    return 0;
}

// Get current Claude Code version
function getCurrentCCVersion() {
    try {
        const output = execSync('claude --version', { encoding: 'utf-8', timeout: 5000 });
        const match = output.match(/(\d+\.\d+\.\d+)/);
        const version = match ? match[1] : null;
        const location = execSync('which claude', { encoding: 'utf-8', timeout: 5000 });
        return { version, location };
    } catch {
        return { version: null, location: null };
    }
}

// Check PAI structure for feature usage
function checkPAIFeatureUsage(paiPath) {
    const usage = {};
    const claudeDir = join(paiPath, '.claude');

    // Check for subagent patterns
    usage.subagents = existsSync(join(claudeDir, 'agents'));

    // Check for hooks (directory or settings.json config)
    usage.hooks = existsSync(join(claudeDir, 'hooks'));

    // Check for skills (new path: .claude/skills/, legacy: .claude/rules/)
    usage.skills = existsSync(join(claudeDir, 'skills')) || existsSync(join(claudeDir, 'rules'));

    // Check for commands (implies planning/workflow)
    usage.planMode = existsSync(join(claudeDir, 'commands'));

    // Check for context system
    usage.contextSystem = existsSync(join(claudeDir, 'context'));

    // Check settings.json for advanced features
    const settingsPath = join(claudeDir, 'settings.json');
    if (existsSync(settingsPath)) {
        try {
            const settings = JSON.parse(readFileSync(settingsPath, 'utf-8'));

            // CC 2.1.x features detection
            usage.settingsJsonHooks = Boolean(settings.hooks && Object.keys(settings.hooks).length > 0);
            usage.statusLine = Boolean(settings.statusLine);
            usage.modelRouting = Boolean(settings.model); // Default model set

            // Enhanced subagents detection (check for skill definitions with context: fork)
            const skillsDir = join(claudeDir, 'skills');
            if (existsSync(skillsDir)) {
                usage.enhancedSubagents = checkForForkContextSkills(skillsDir);
                usage.skillInvocation = true;
            }
        } catch {
            // Settings parse error, skip
        }
    }

    return usage;
}

// Check if skills directory contains fork context skills
function checkForForkContextSkills(skillsDir) {
    try {
        const entries = readdirSync(skillsDir, { withFileTypes: true });
        for (const entry of entries) {
            if (entry.isDirectory()) {
                const skillMd = join(skillsDir, entry.name, 'SKILL.md');
                if (existsSync(skillMd)) {
                    const content = readFileSync(skillMd, 'utf-8');
                    if (content.includes('context: fork')) {
                        return true;
                    }
                }
            }
        }
    } catch {
        // Error reading skills dir
    }
    return false;
}

// Generate compatibility report
function generateReport(currentVersion, currentLocation, paiPath) {
    const report = {
        timestamp: new Date().toISOString(),
        ccVersion: currentVersion || 'Not detected',
        ccLocation: currentLocation || 'Not detected',
        paiPath: paiPath,
        featureStatus: {},
        recommendations: []
    };

    if (!currentVersion) {
        report.recommendations.push({
            priority: 'HIGH',
            message: 'Claude Code not detected. Install with: bun install -g @anthropic-ai/claude-code'
        });
        return report;
    }

    const currentParsed = parseVersion(currentVersion);
    const paiUsage = checkPAIFeatureUsage(paiPath);

    for (const [feature, config] of Object.entries(FEATURE_REQUIREMENTS)) {
        const requiredParsed = parseVersion(config.minVersion);
        const isSupported = compareVersions(currentParsed, requiredParsed) >= 0;
        const isUsed = paiUsage[feature] || false;

        report.featureStatus[feature] = {
            description: config.description,
            minVersion: config.minVersion,
            supported: isSupported,
            inUse: isUsed
        };

        if (isSupported && !isUsed) {
            report.recommendations.push({
                priority: 'MEDIUM',
                feature: feature,
                message: `Feature "${feature}" is available but not utilized in PAI. ${config.description}`
            });
        }

        if (!isSupported && isUsed) {
            report.recommendations.push({
                priority: 'HIGH',
                feature: feature,
                message: `Feature "${feature}" requires CC v${config.minVersion}+. Current: v${currentVersion}. Update recommended.`
            });
        }
    }

    // Add version-specific recommendations
    if (compareVersions(currentParsed, parseVersion('2.0.0')) < 0) {
        report.recommendations.push({
            priority: 'HIGH',
            message: 'Major version 2.0+ recommended for checkpoints, VS Code extension, and improved stability.'
        });
    }

    return report;
}

// Format report for console output
function formatReport(report) {
    const lines = [];

    lines.push('\n╔══════════════════════════════════════════════════════════════╗');
    lines.push('║           CC-PAI COMPATIBILITY REPORT                        ║');
    lines.push('╚══════════════════════════════════════════════════════════════╝\n');

    lines.push(`📅 Generated: ${report.timestamp}`);
    lines.push(`🔧 Claude Code Version: ${report.ccVersion}`);
    lines.push(`📍 Claude Code Location: ${report.ccLocation?.trim() || 'Not detected'}`);
    lines.push(`📁 PAI Path: ${report.paiPath}\n`);

    lines.push('─── FEATURE STATUS ───────────────────────────────────────────\n');

    for (const [feature, status] of Object.entries(report.featureStatus)) {
        const supportIcon = status.supported ? '✅' : '❌';
        const useIcon = status.inUse ? '🟢' : '⚪';
        lines.push(`${supportIcon} ${useIcon} ${feature.padEnd(20)} v${status.minVersion}+ | ${status.description}`);
    }

    if (report.recommendations.length > 0) {
        lines.push('\n─── RECOMMENDATIONS ──────────────────────────────────────────\n');

        const sorted = [...report.recommendations].sort((a, b) => {
            const priority = { HIGH: 0, MEDIUM: 1, LOW: 2 };
            return priority[a.priority] - priority[b.priority];
        });

        for (const rec of sorted) {
            const icon = rec.priority === 'HIGH' ? '🔴' : rec.priority === 'MEDIUM' ? '🟡' : '🟢';
            lines.push(`${icon} [${rec.priority}] ${rec.message}`);
        }
    }

    lines.push('\n─── LEGEND ───────────────────────────────────────────────────');
    lines.push('✅ Supported  ❌ Not Supported  🟢 In Use  ⚪ Not Used\n');

    return lines.join('\n');
}

// Main execution
async function main() {
    const paiPath = process.argv[2] || process.cwd();

    console.log('Checking Claude Code compatibility...\n');

    const { version: currentVersion, location: currentLocation } = getCurrentCCVersion();
    const report = generateReport(currentVersion, currentLocation, paiPath);

    console.log(formatReport(report));

    // Output JSON for programmatic use
    if (process.argv.includes('--json')) {
        console.log('\n─── JSON OUTPUT ──────────────────────────────────────────────\n');
        console.log(JSON.stringify(report, null, 2));
    }
}

main().catch(console.error);
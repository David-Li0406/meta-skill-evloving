const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const SKILLS_ROOT = '.agent/skills';
const GATES = [
    {
        name: 'UI/UX Audit',
        command: `node ${SKILLS_ROOT}/ui-ux-audit/scripts/scan-token-violations.js`,
        files: ['src/components'], // Only run if valid files changed? (Simplification: run always for now)
        blocking: false // Audit warnings shouldn't strictly block dev commits, but nice to know
    },
    {
        name: 'Code Quality',
        command: `node ${SKILLS_ROOT}/code-quality/scripts/scan-quality-metrics.js`,
        blocking: true // Metrics are strictly enforced
    },
    {
        name: 'Database Health',
        command: `node ${SKILLS_ROOT}/db-optimizer/scripts/audit-prisma-schema.js`,
        blocking: true // Missing indexes are critical
    },
    {
        name: 'Smoke Tests',
        command: `node ${SKILLS_ROOT}/test-automation/scripts/run-smoke-tests.js`,
        blocking: true // Broken critical path = No commit
    }
];

function runCommand(cmd) {
    try {
        execSync(cmd, { stdio: 'inherit' });
        return true;
    } catch (e) {
        return false;
    }
}

function main() {
    const args = process.argv.slice(2);
    const bypass = args.includes('--bypass');
    const commitMsg = args.find(a => !a.startsWith('--'));

    if (!commitMsg) {
        console.error('❌ Error: Commit message required.');
        console.error('   Usage: node gated-commit.js "feat: message"');
        process.exit(1);
    }

    console.log('🛡️  Starting Gated Commit Protocol...\n');

    let allPassed = true;

    for (const gate of GATES) {
        console.log(`\n🔍 Gate: ${gate.name}...`);
        const passed = runCommand(gate.command);

        if (!passed) {
            if (gate.blocking && !bypass) {
                console.error(`\n❌ Gate Failed: ${gate.name}`);
                console.error('   Blocking commit. Fix the error or use --bypass (use responsibly).');
                process.exit(1);
            } else if (gate.blocking && bypass) {
                console.warn(`\n⚠️  Gate Failed: ${gate.name} (BYPASSED)`);
                allPassed = false; // Track dirty state
            } else {
                console.warn(`\n⚠️  Gate Warning: ${gate.name}`);
            }
        } else {
            console.log(`✅ Gate Passed: ${gate.name}`);
        }
    }

    console.log('\n📝 Committing...');
    try {
        // Construct commit command
        execSync(`git commit -m "${commitMsg}"`, { stdio: 'inherit' });
        console.log('\n🚀 Commit Successful!');
    } catch (e) {
        console.error('\n❌ Git Commit Failed (check git output above)');
        process.exit(1);
    }
}

main();

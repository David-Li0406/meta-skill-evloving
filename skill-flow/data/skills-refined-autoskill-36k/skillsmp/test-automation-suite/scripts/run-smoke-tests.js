const { execSync } = require('child_process');

function runSmokeTests() {
    console.log('🧪 Starting Smoke Test Suite...\n');

    try {
        console.log('👉 Running: npx playwright test --config=playwright.smoke.config.ts');
        // Using stdio: inherit to show live output
        execSync('npx playwright test --config=playwright.smoke.config.ts', { stdio: 'inherit' });
        console.log('\n✅ Smoke Tests Passed!');
    } catch (error) {
        console.error('\n❌ Smoke Tests FAILED. Please review the output above.');
        process.exit(1);
    }
}

runSmokeTests();

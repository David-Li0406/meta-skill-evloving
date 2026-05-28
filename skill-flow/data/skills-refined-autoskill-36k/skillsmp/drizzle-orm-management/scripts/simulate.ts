import { config } from 'dotenv';
config({ path: '.env.local', override: true });

async function main() {
    const { simulationService } = await import("../../../src/lib/services/simulation.service");

    const roundId = process.argv[2];

    if (!roundId) {
        console.error("Usage: npx tsx skills/drizzle/scripts/simulate.ts <roundId>");
        process.exit(1);
    }

    console.log(`🚀 Simulating round: ${roundId}...`);

    try {
        const result = await simulationService.simulateRound(roundId);
        if (result.success && 'processedMatches' in result) {
            console.log(`✅ Simulation successful: ${result.processedMatches} matches processed.`);
        } else {
            console.log(`✅ Simulation successful.`);
        }
    } catch (error) {
        console.error("❌ Simulation failed:");
        console.error(error);
        process.exit(1);
    }
}

main();

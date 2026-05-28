import { config } from 'dotenv';
config({ path: '.env.local', override: true });

async function clearAllData() {
    const { db } = await import("../../../src/db");
    const { rounds } = await import("../../../src/db/schema");
    const { scoringRepository } = await import("../../../src/db/repositories/scoring.repository");

    console.log("🧹 Clearing all scores from the database...");

    try {
        await db.transaction(async (tx) => {
            await scoringRepository.deleteAll(tx);
            console.log("✅ All scores deleted.");
            await tx.update(rounds).set({ status: 'scheduled' });
            console.log("✅ All rounds reset to 'scheduled'.");
        });

        console.log("✨ Database clean-up complete.");
    } catch (error) {
        console.error("❌ Failed to clear scores:");
        console.error(error);
        process.exit(1);
    }
}

clearAllData();

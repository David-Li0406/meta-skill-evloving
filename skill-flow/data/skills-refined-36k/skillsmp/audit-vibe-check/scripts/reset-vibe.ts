import { db } from '../../../../server/src/firebaseAdmin.js';

const VENUE_ID = 'brotherhood-lounge';

async function resetVibe() {
  console.log(`[ResetVibe] Resetting venue: ${VENUE_ID}...`);

  try {
    const venueRef = db.collection('venues').doc(VENUE_ID);
    const doc = await venueRef.get();

    if (!doc.exists) {
      console.error(`❌ Venue ${VENUE_ID} not found!`);
      process.exit(1);
    }

    // 1. Reset Venue Score
    await venueRef.update({
      buzzScore: 0,
      clockIns: 0,
      lastUpdated: Date.now(),
      // Ensure visualization parameters are reset
      manualOverride: null
    });
    console.log('✅ Venue score reset to 0.');

    // 2. Clear recent checking/signals (Optional but good for purity)
    // Note: In a real "System" audit, we might effectively specific recent signals, 
    // but for now, the venue aggregate is the source of truth for the UI.

    console.log('✨ Vibe Reset Complete.');
    process.exit(0);

  } catch (error) {
    console.error('❌ Error resetting vibe:', error);
    process.exit(1);
  }
}

resetVibe();

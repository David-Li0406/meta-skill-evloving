import { julesFetch, ApprovePlanRequest, ApprovePlanResponse } from './client.js';

async function main() {
  const sessionName = process.argv[2];

  if (!sessionName) {
    console.error('Usage: npx tsx approve-plan.ts <session-name>');
    console.error('Example: npx tsx approve-plan.ts sessions/12345');
    process.exit(1);
  }

  // Use strict type (empty object)
  const payload: ApprovePlanRequest = {};

  try {
    await julesFetch<ApprovePlanResponse>(`${sessionName}:approvePlan`, {
      method: 'POST',
      body: JSON.stringify(payload)
    });

    console.log(`Plan for session ${sessionName} approved successfully.`);

  } catch (error) {
     process.exit(1);
  }
}

main();

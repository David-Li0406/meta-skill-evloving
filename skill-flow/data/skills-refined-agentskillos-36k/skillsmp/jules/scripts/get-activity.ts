import { julesFetch, Activity } from './client.js';

async function main() {
  const sessionName = process.argv[2];
  const activityId = process.argv[3];

  if (!sessionName || !activityId) {
    console.error('Usage: npx tsx get-activity.ts <session-name> <activity-id>');
    console.error('Example: npx tsx get-activity.ts sessions/12345 act123');
    process.exit(1);
  }

  try {
    const activity = await julesFetch<Activity>(`${sessionName}/activities/${activityId}`);

    console.log(JSON.stringify(activity, null, 2));

  } catch (error) {
    process.exit(1);
  }
}

main();

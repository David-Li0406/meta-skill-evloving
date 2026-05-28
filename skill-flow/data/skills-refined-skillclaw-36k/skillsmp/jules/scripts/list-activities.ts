import { julesFetch, ListActivitiesResponse } from './client.js';

async function main() {
  const sessionName = process.argv[2];

  if (!sessionName) {
    console.error('Usage: npx tsx list-activities.ts <session-name>');
    console.error('Example: npx tsx list-activities.ts sessions/12345');
    process.exit(1);
  }

  // Remove trailing slashes or "sessions/" prefix if user inputs are messy,
  // but standard input "sessions/123" is expected.

  try {
    const listResponse = await julesFetch<ListActivitiesResponse>(`${sessionName}/activities?pageSize=50`);

    if (!listResponse.activities || listResponse.activities.length === 0) {
      console.log('No activities found for this session.');
      return;
    }

    console.log(`Activities for ${sessionName}:`);
    listResponse.activities.forEach(activity => {
      console.log('--------------------------------------------------');
      console.log(`ID: ${activity.id}`);
      console.log(`Originator: ${activity.originator}`);
      console.log(`Time: ${activity.createTime}`);
      console.log(`Description: ${activity.description}`);

      // Print specific event details if useful
      if (activity.agentMessaged) console.log(`[Agent]: ${activity.agentMessaged.agentMessage}`);
      if (activity.userMessaged) console.log(`[User]: ${activity.userMessaged.userMessage}`);
      if (activity.sessionFailed) console.log(`[FAILED]: ${activity.sessionFailed.reason}`);
    });
    console.log('--------------------------------------------------');

    if (listResponse.nextPageToken) {
        console.log(`\n(Has more pages. Next Page Token: ${listResponse.nextPageToken})`);
    }

  } catch (error) {
    process.exit(1);
  }
}

main();

import { julesFetch, ListSessionsResponse } from './client.js';

async function main() {
  try {
    const listResponse = await julesFetch<ListSessionsResponse>('sessions?pageSize=30');

    if (!listResponse.sessions || listResponse.sessions.length === 0) {
      console.log('No sessions found.');
      return;
    }

    console.log('Jules Sessions:');
    listResponse.sessions.forEach(session => {
      console.log('--------------------------------------------------');
      console.log(`Title: ${session.title || '(No Title)'}`);
      console.log(`ID: ${session.name}`); // resource name is the ID for most purposes
      console.log(`State: ${session.state}`);
      console.log(`Prompt: ${session.prompt?.substring(0, 50)}...`);
      console.log(`Created: ${session.createTime}`);
    });
    console.log('--------------------------------------------------');

    if (listResponse.nextPageToken) {
        console.log(`\n(Has more pages. Next Page Token: ${listResponse.nextPageToken})`);
    }

  } catch (error) {
    // client.ts handles logging specific errors, so we just exit here.
    process.exit(1);
  }
}

main();

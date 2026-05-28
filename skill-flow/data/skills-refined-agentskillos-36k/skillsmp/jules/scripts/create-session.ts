import { julesFetch, Session, CreateSessionRequest } from './client.js';

// Default source configuration
const DEFAULT_SOURCE = 'sources/github/dappvibe/pexfi';
const DEFAULT_BRANCH = 'master';

async function main() {
  const prompt = process.argv[2];
  const title = process.argv[3];

  if (!prompt) {
    console.error('Usage: npx tsx create-session.ts <prompt> [title]');
    process.exit(1);
  }

  // Construct the payload with strict typing
  const payload: CreateSessionRequest = {
    prompt: prompt,
    title: title || undefined,
    sourceContext: {
      source: DEFAULT_SOURCE,
      githubRepoContext: {
        startingBranch: DEFAULT_BRANCH
      }
    },
    // Optional settings based on types
    requirePlanApproval: true,
    // automationMode: 'AUTO_CREATE_PR' // Commented out by default to avoid issues, can be enabled if needed
  };

  try {
    console.log(`Creating session for source: ${DEFAULT_SOURCE} (branch: ${DEFAULT_BRANCH})...`);

    // Using strict generic type <Session> for the response
    const session = await julesFetch<Session>('sessions', {
      method: 'POST',
      body: JSON.stringify(payload)
    });

    console.log('Session Created Successfully!');
    console.log('--------------------------------------------------');
    console.log(`ID: ${session.name}`);
    console.log(`Title: ${session.title || '(No Title)'}`);
    console.log(`State: ${session.state}`);
    console.log(`URL: ${session.url}`);
    console.log('--------------------------------------------------');

  } catch (error) {
     process.exit(1);
  }
}

main();

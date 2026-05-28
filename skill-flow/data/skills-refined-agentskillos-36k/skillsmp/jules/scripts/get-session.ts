import { julesFetch, Session } from './client.js';

async function main() {
  const sessionName = process.argv[2];

  if (!sessionName) {
    console.error('Usage: npx tsx get-session.ts <session-name>');
    console.error('Example: npx tsx get-session.ts sessions/12345');
    process.exit(1);
  }

  try {
    const session = await julesFetch<Session>(sessionName);

    console.log(JSON.stringify(session, null, 2));

  } catch (error) {
     // client.ts handles logging specific errors
     process.exit(1);
  }
}

main();

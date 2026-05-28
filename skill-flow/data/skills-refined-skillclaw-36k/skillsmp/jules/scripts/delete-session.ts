import { julesFetch } from './client.js';

async function main() {
  const sessionName = process.argv[2];

  if (!sessionName) {
    console.error('Usage: npx tsx delete-session.ts <session-name>');
    console.error('Example: npx tsx delete-session.ts sessions/12345');
    process.exit(1);
  }

  try {
    await julesFetch(sessionName, {
      method: 'DELETE'
    });

    console.log(`Session ${sessionName} deleted successfully.`);

  } catch (error) {
     // client.ts handles logging specific errors
     process.exit(1);
  }
}

main();

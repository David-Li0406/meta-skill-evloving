import { julesFetch, SendMessageRequest, SendMessageResponse } from './client.js';

async function main() {
  const sessionName = process.argv[2];
  const message = process.argv[3];

  if (!sessionName || !message) {
    console.error('Usage: npx tsx send-message.ts <session-name> <message>');
    console.error('Example: npx tsx send-message.ts sessions/12345 "Please add tests"');
    process.exit(1);
  }

  // Use strict type for payload
  const payload: SendMessageRequest = {
    prompt: message
    // Note: client.ts defines this as 'prompt' based on API behavior,
    // even though typical naming might be 'message'.
  };

  try {
    await julesFetch<SendMessageResponse>(`${sessionName}:sendMessage`, {
      method: 'POST',
      body: JSON.stringify(payload)
    });

    console.log(`Message sent to ${sessionName} successfully.`);

  } catch (error) {
     process.exit(1);
  }
}

main();

const fs = require('fs');
const path = require('path');

const apiKey = process.env.GEMINI_API_KEY;
if (!apiKey) {
  console.error("Error: GEMINI_API_KEY environment variable is not set.");
  process.exit(1);
}

const args = process.argv.slice(2);
const command = args[0];

if (!command) {
  console.error("Usage: node deep-research.js <start|check|poll> ...");
  process.exit(1);
}

const BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/interactions';

async function start() {
  let model = "deep-research-pro-preview-12-2025";
  let filename = null;
  const promptParts = [];

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--model') {
      if (i + 1 < args.length) {
        model = args[i + 1];
        i++; // Skip the model value
      } else {
        console.error("Error: --model flag requires a value.");
        process.exit(1);
      }
    } else {
      if (!filename) {
        filename = args[i];
      } else {
        promptParts.push(args[i]);
      }
    }
  }

  const prompt = promptParts.join(' ');

  if (!filename || !prompt) {
    console.error("Usage: node deep-research.js start <filename> [--model <model>] <prompt...>");
    process.exit(1);
  }

  const requestBody = {
    input: prompt,
    agent: model,
    background: true
  };

  try {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-goog-api-key': apiKey
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`API Error (${response.status}):`, errorText);
      process.exit(1);
    }

    const data = await response.json();
    const interactionId = data.id;

    if (!interactionId) {
      console.error("Error: No interaction ID returned.");
      process.exit(1);
    }

    const fileContent = {
      interaction_id: interactionId,
      status: 'in_progress', // Initial assumption
      prompt: prompt,
      started_at: new Date().toISOString()
    };

    fs.writeFileSync(filename, JSON.stringify(fileContent, null, 2));
    console.log(`Research started. Interaction ID: ${interactionId}. Saved to ${filename}`);

  } catch (error) {
    console.error("Request failed:", error);
    process.exit(1);
  }
}

async function check(filename, silent = false) {
  if (!filename) {
    console.error("Usage: node deep-research.js check <filename>");
    if (!silent) process.exit(1);
    return 'error';
  }

  if (!fs.existsSync(filename)) {
    console.error(`Error: File ${filename} not found.`);
    if (!silent) process.exit(1);
    return 'error';
  }

  let fileContent;
  try {
    fileContent = JSON.parse(fs.readFileSync(filename, 'utf8'));
  } catch (e) {
    console.error(`Error: Could not parse ${filename}. Is it a valid JSON file?`);
    if (!silent) process.exit(1);
    return 'error';
  }

  const interactionId = fileContent.interaction_id;
  if (!interactionId) {
    console.error(`Error: No interaction_id found in ${filename}.`);
    if (!silent) process.exit(1);
    return 'error';
  }

  try {
    const response = await fetch(`${BASE_URL}/${interactionId}`, {
      method: 'GET',
      headers: {
        'x-goog-api-key': apiKey
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`API Error (${response.status}):`, errorText);
      if (!silent) process.exit(1);
      return 'error';
    }

    const data = await response.json();
    const status = data.status;

    if (!silent) console.log(`Status: ${status}`);

    if (status === 'completed') {
      let resultText = '';
      if (data.outputs && data.outputs.length > 0 && data.outputs[data.outputs.length - 1].text) {
        resultText = data.outputs[data.outputs.length - 1].text;
      } else {
        resultText = "No text output found in completed interaction.";
      }

      // Replace file content with the result
      fs.writeFileSync(filename, resultText);
      if (!silent) console.log(`Research complete! Result saved to ${filename}`);
      return 'completed';
    } else if (status === 'failed') {
      console.error("Research failed.");
       // Update status in file but keep it JSON for now so user knows it failed
      fileContent.status = 'failed';
      fileContent.error = data.error || "Unknown error";
      fs.writeFileSync(filename, JSON.stringify(fileContent, null, 2));
      return 'failed';
    } else {
        // Update status in file
        fileContent.status = status;
        fs.writeFileSync(filename, JSON.stringify(fileContent, null, 2));
        return 'in_progress';
    }

  } catch (error) {
    console.error("Check failed:", error);
    if (!silent) process.exit(1);
    return 'error';
  }
}

async function poll() {
  const filename = args[1];
  const intervalArg = args[2];
  const intervalSeconds = intervalArg ? parseInt(intervalArg, 10) : 10;
  const intervalMs = intervalSeconds * 1000;

  if (!filename) {
    console.error("Usage: node deep-research.js poll <filename> [interval_seconds]");
    process.exit(1);
  }

  console.log(`Polling ${filename} every ${intervalSeconds} seconds...`);

  const pollLoop = async () => {
    const status = await check(filename, true); // Silent check mostly

    if (status === 'completed') {
      console.log("Research completed.");
      process.exit(0);
    } else if (status === 'failed') {
      console.error("Research failed.");
      process.exit(1);
    } else if (status === 'error') {
        console.error("An error occurred during polling.");
        process.exit(1);
    } else {
      // Still in progress
      console.log(`[${new Date().toLocaleTimeString()}] Status: in_progress...`);
      setTimeout(pollLoop, intervalMs);
    }
  };

  pollLoop();
}

switch (command) {
  case 'start':
    start();
    break;
  case 'check':
    check(args[1]);
    break;
  case 'poll':
    poll();
    break;
  default:
    console.error(`Unknown command: ${command}`);
    console.error("Usage: node deep-research.js <start|check|poll> ...");
    process.exit(1);
}

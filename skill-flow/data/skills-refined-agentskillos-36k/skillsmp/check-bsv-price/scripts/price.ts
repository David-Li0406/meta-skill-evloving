#!/usr/bin/env bun

const args = process.argv.slice(2);

function showHelp(): void {
  console.log(`check-bsv-price - Get current BSV price

USAGE:
  bun run price.ts [options]

OPTIONS:
  --json    Output in JSON format
  --help    Show this help message

EXAMPLES:
  bun run price.ts
  bun run price.ts --json`);
}

async function getBSVPrice(): Promise<void> {
  const jsonOutput = args.includes("--json");

  if (args.includes("--help") || args.includes("-h")) {
    showHelp();
    process.exit(0);
  }

  try {
    const response = await fetch(
      "https://api.whatsonchain.com/v1/bsv/main/exchangerate"
    );

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    const data = await response.json();

    if (jsonOutput) {
      console.log(JSON.stringify({
        price: data.rate,
        currency: data.currency || "USD",
        timestamp: new Date().toISOString()
      }, null, 2));
    } else {
      console.log(`BSV Price: $${data.rate} USD`);
      console.log(`Updated: ${new Date().toISOString()}`);
    }

  } catch (error: any) {
    const msg = `Failed to fetch BSV price: ${error.message}`;
    if (args.includes("--json")) {
      console.error(JSON.stringify({ error: msg }));
    } else {
      console.error(`Error: ${msg}`);
    }
    process.exit(1);
  }
}

getBSVPrice();

import { julesFetch, Source } from './client.js';

async function main() {
  const sourceName = process.argv[2];

  if (!sourceName) {
    console.error('Usage: npx tsx get-source.ts <source-name>');
    console.error('Example: npx tsx get-source.ts sources/github/myorg/myrepo');
    process.exit(1);
  }

  // Handle common shorthand where user provides just "github/myorg/myrepo" instead of "sources/github/myorg/myrepo"
  // The API expects the full resource name starting with "sources/" usually, but let's be safe.
  // Actually, the API docs say `sources/{source}` is the pattern.

  try {
    const source = await julesFetch<Source>(sourceName);

    console.log(JSON.stringify(source, null, 2));

  } catch (error) {
    process.exit(1);
  }
}

main();

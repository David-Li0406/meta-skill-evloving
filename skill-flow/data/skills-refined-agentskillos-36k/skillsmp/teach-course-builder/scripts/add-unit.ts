#!/usr/bin/env -S deno run --allow-net --allow-env

/**
 * Add Unit
 *
 * Adds a unit to an existing course via the authoring API.
 *
 * Usage:
 *   deno run --allow-net --allow-env scripts/add-unit.ts --course-id <id> --title "Unit Title"
 *   deno run --allow-net --allow-env scripts/add-unit.ts --course-id <id> --title "Title" --description "Description"
 *   deno run --allow-net --allow-env scripts/add-unit.ts --course-id <id> --title "Title" --order 2
 */

import { createUnit, parseArgs, showHelp, type Unit } from "./api-client.ts";

// === OUTPUT FORMATTING ===

function formatUnit(unit: Unit): string {
  const lines: string[] = [];
  lines.push(`Unit Created Successfully`);
  lines.push(`========================`);
  lines.push(``);
  lines.push(`ID:          ${unit.id}`);
  lines.push(`Course ID:   ${unit.courseId}`);
  lines.push(`Title:       ${unit.title}`);
  lines.push(`Description: ${unit.description || "(none)"}`);
  lines.push(`Order:       ${unit.order}`);
  lines.push(`Created:     ${unit.createdAt}`);
  lines.push(``);
  lines.push(`Next steps:`);
  lines.push(`  - Add lessons: deno run --allow-net --allow-env scripts/add-lesson.ts --unit-id ${unit.id} --title "Lesson Title"`);
  return lines.join("\n");
}

// === MAIN ===

async function main(): Promise<void> {
  const args = parseArgs(Deno.args);

  if (args.has("help") || args.has("h") || Deno.args.includes("-h")) {
    showHelp(
      "Add Unit",
      "Usage: deno run --allow-net --allow-env scripts/add-unit.ts --course-id <id> --title <title> [options]",
      `  --course-id <id>       Course ID (required)
  --title <title>        Unit title (required)
  --description <desc>   Unit description
  --order <number>       Order within course`
    );
    Deno.exit(0);
  }

  const courseId = args.get("course-id") as string;
  if (!courseId) {
    console.error("Error: --course-id is required");
    Deno.exit(1);
  }

  const title = args.get("title") as string;
  if (!title) {
    console.error("Error: --title is required");
    Deno.exit(1);
  }

  const description = args.get("description") as string | undefined;
  const orderStr = args.get("order") as string | undefined;
  const order = orderStr ? parseInt(orderStr, 10) : undefined;

  try {
    const unit = await createUnit(courseId, {
      title,
      description,
      order,
    });

    if (args.has("json")) {
      console.log(JSON.stringify(unit, null, 2));
    } else {
      console.log(formatUnit(unit));
    }
  } catch (error) {
    console.error(`Error creating unit: ${error}`);
    Deno.exit(1);
  }
}

main();

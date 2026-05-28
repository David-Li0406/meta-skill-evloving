#!/usr/bin/env -S deno run --allow-net --allow-env

/**
 * Create Course
 *
 * Creates a new course via the authoring API.
 *
 * Usage:
 *   deno run --allow-net --allow-env scripts/create-course.ts --title "Course Title"
 *   deno run --allow-net --allow-env scripts/create-course.ts --title "Title" --description "Description"
 *   deno run --allow-net --allow-env scripts/create-course.ts --title "Title" --json
 */

import { createCourse, parseArgs, showHelp, type Course } from "./api-client.ts";

// === OUTPUT FORMATTING ===

function formatCourse(course: Course): string {
  const lines: string[] = [];
  lines.push(`Course Created Successfully`);
  lines.push(`==========================`);
  lines.push(``);
  lines.push(`ID:          ${course.id}`);
  lines.push(`Title:       ${course.title}`);
  lines.push(`Description: ${course.description || "(none)"}`);
  lines.push(`Version:     ${course.version}`);
  lines.push(`Status:      ${course.status}`);
  lines.push(`Created:     ${course.createdAt}`);
  lines.push(``);
  lines.push(`Next steps:`);
  lines.push(`  - Add units: deno run --allow-net --allow-env scripts/add-unit.ts --course-id ${course.id} --title "Unit Title"`);
  lines.push(`  - View in UI: http://localhost:4101/courses/${course.id}`);
  return lines.join("\n");
}

// === MAIN ===

async function main(): Promise<void> {
  const args = parseArgs(Deno.args);

  if (args.has("help") || args.has("h") || Deno.args.includes("-h")) {
    showHelp(
      "Create Course",
      "Usage: deno run --allow-net --allow-env scripts/create-course.ts --title <title> [options]",
      `  --title <title>        Course title (required)
  --description <desc>   Course description
  --version <version>    Version string (default: 1.0.0)`
    );
    Deno.exit(0);
  }

  const title = args.get("title") as string;
  if (!title) {
    console.error("Error: --title is required");
    console.error("Usage: deno run --allow-net --allow-env scripts/create-course.ts --title <title>");
    Deno.exit(1);
  }

  const description = args.get("description") as string | undefined;
  const version = args.get("version") as string | undefined;

  try {
    const course = await createCourse({
      title,
      description,
      version,
    });

    if (args.has("json")) {
      console.log(JSON.stringify(course, null, 2));
    } else {
      console.log(formatCourse(course));
    }
  } catch (error) {
    console.error(`Error creating course: ${error}`);
    Deno.exit(1);
  }
}

main();

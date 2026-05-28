#!/usr/bin/env -S deno run --allow-net --allow-env

/**
 * List Courses
 *
 * Lists all courses in the authoring API.
 *
 * Usage:
 *   deno run --allow-net --allow-env scripts/list-courses.ts
 *   deno run --allow-net --allow-env scripts/list-courses.ts --json
 */

import { listCourses, parseArgs, showHelp, type Course } from "./api-client.ts";

// === OUTPUT FORMATTING ===

function formatCourses(courses: Course[]): string {
  if (courses.length === 0) {
    return "No courses found.\n\nCreate one with:\n  deno run --allow-net --allow-env scripts/create-course.ts --title \"Course Title\"";
  }

  const lines: string[] = [];
  lines.push(`Found ${courses.length} course(s):`);
  lines.push(``);

  for (const course of courses) {
    lines.push(`${course.title}`);
    lines.push(`  ID:     ${course.id}`);
    lines.push(`  Status: ${course.status}`);
    if (course.description) {
      const desc = course.description.length > 60
        ? course.description.slice(0, 57) + "..."
        : course.description;
      lines.push(`  Desc:   ${desc}`);
    }
    lines.push(``);
  }

  return lines.join("\n");
}

// === MAIN ===

async function main(): Promise<void> {
  const args = parseArgs(Deno.args);

  if (args.has("help") || args.has("h") || Deno.args.includes("-h")) {
    showHelp(
      "List Courses",
      "Usage: deno run --allow-net --allow-env scripts/list-courses.ts [options]",
      ``
    );
    Deno.exit(0);
  }

  try {
    const courses = await listCourses();

    if (args.has("json")) {
      console.log(JSON.stringify(courses, null, 2));
    } else {
      console.log(formatCourses(courses));
    }
  } catch (error) {
    console.error(`Error listing courses: ${error}`);
    Deno.exit(1);
  }
}

main();

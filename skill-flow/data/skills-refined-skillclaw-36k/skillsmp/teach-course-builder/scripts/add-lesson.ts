#!/usr/bin/env -S deno run --allow-net --allow-env --allow-read

/**
 * Add Lesson
 *
 * Adds a lesson to an existing unit via the authoring API.
 * Can optionally read content from a markdown file.
 *
 * Usage:
 *   deno run --allow-net --allow-env --allow-read scripts/add-lesson.ts --unit-id <id> --title "Lesson Title"
 *   deno run --allow-net --allow-env --allow-read scripts/add-lesson.ts --unit-id <id> --title "Title" --content-file /path/to/content.md
 *   deno run --allow-net --allow-env --allow-read scripts/add-lesson.ts --unit-id <id> --title "Title" --audience-layer general
 */

import { createLesson, parseArgs, showHelp, type Lesson } from "./api-client.ts";

// === OUTPUT FORMATTING ===

function formatLesson(lesson: Lesson): string {
  const lines: string[] = [];
  lines.push(`Lesson Created Successfully`);
  lines.push(`===========================`);
  lines.push(``);
  lines.push(`ID:             ${lesson.id}`);
  lines.push(`Unit ID:        ${lesson.unitId}`);
  lines.push(`Title:          ${lesson.title}`);
  lines.push(`Description:    ${lesson.description || "(none)"}`);
  lines.push(`Order:          ${lesson.order}`);
  lines.push(`Audience Layer: ${lesson.audienceLayer || "(none)"}`);
  lines.push(`Content Type:   ${lesson.content.type}`);
  lines.push(`Content Length: ${lesson.content.body.length} characters`);
  lines.push(`Created:        ${lesson.createdAt}`);
  return lines.join("\n");
}

// === MAIN ===

async function main(): Promise<void> {
  const args = parseArgs(Deno.args);

  if (args.has("help") || args.has("h") || Deno.args.includes("-h")) {
    showHelp(
      "Add Lesson",
      "Usage: deno run --allow-net --allow-env --allow-read scripts/add-lesson.ts --unit-id <id> --title <title> [options]",
      `  --unit-id <id>              Unit ID (required)
  --title <title>             Lesson title (required)
  --description <desc>        Lesson description
  --content-file <path>       Path to markdown file for content
  --audience-layer <layer>    Audience layer: general, practitioner, specialist
  --order <number>            Order within unit`
    );
    Deno.exit(0);
  }

  const unitId = args.get("unit-id") as string;
  if (!unitId) {
    console.error("Error: --unit-id is required");
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
  const contentFile = args.get("content-file") as string | undefined;
  const audienceLayerRaw = args.get("audience-layer") as string | undefined;

  // Validate audience layer
  let audienceLayer: "general" | "practitioner" | "specialist" | undefined;
  if (audienceLayerRaw) {
    if (!["general", "practitioner", "specialist"].includes(audienceLayerRaw)) {
      console.error("Error: --audience-layer must be one of: general, practitioner, specialist");
      Deno.exit(1);
    }
    audienceLayer = audienceLayerRaw as "general" | "practitioner" | "specialist";
  }

  // Read content from file if specified
  let content: { type: "markdown" | "html"; body: string } | undefined;
  if (contentFile) {
    try {
      const body = await Deno.readTextFile(contentFile);
      content = { type: "markdown", body };
      console.error(`Read ${body.length} characters from ${contentFile}`);
    } catch (error) {
      console.error(`Error reading content file: ${error}`);
      Deno.exit(1);
    }
  }

  try {
    const lesson = await createLesson(unitId, {
      title,
      description,
      order,
      content,
      audienceLayer,
    });

    if (args.has("json")) {
      console.log(JSON.stringify(lesson, null, 2));
    } else {
      console.log(formatLesson(lesson));
    }
  } catch (error) {
    console.error(`Error creating lesson: ${error}`);
    Deno.exit(1);
  }
}

main();

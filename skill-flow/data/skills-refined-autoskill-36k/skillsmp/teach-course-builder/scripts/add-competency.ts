#!/usr/bin/env -S deno run --allow-net --allow-env

/**
 * Add Competency
 *
 * Adds a competency to an existing course via the authoring API.
 * Creates a competency cluster if needed.
 *
 * Usage:
 *   deno run --allow-net --allow-env scripts/add-competency.ts --course-id <id> --name "Competency Name"
 *   deno run --allow-net --allow-env scripts/add-competency.ts --course-id <id> --name "Name" --cluster-name "Cluster"
 *   deno run --allow-net --allow-env scripts/add-competency.ts --cluster-id <id> --name "Name"
 */

import {
  createCompetency,
  createCompetencyCluster,
  listCompetencyClusters,
  parseArgs,
  showHelp,
  type Competency,
  type CompetencyCluster,
} from "./api-client.ts";

// === OUTPUT FORMATTING ===

function formatCompetency(competency: Competency, cluster?: CompetencyCluster): string {
  const lines: string[] = [];
  lines.push(`Competency Created Successfully`);
  lines.push(`===============================`);
  lines.push(``);
  lines.push(`ID:          ${competency.id}`);
  lines.push(`Cluster ID:  ${competency.clusterId}`);
  if (cluster) {
    lines.push(`Cluster:     ${cluster.name}`);
  }
  lines.push(`Name:        ${competency.name}`);
  lines.push(`Description: ${competency.description || "(none)"}`);
  lines.push(`Order:       ${competency.order}`);
  lines.push(`Created:     ${competency.createdAt}`);
  return lines.join("\n");
}

// === MAIN ===

async function main(): Promise<void> {
  const args = parseArgs(Deno.args);

  if (args.has("help") || args.has("h") || Deno.args.includes("-h")) {
    showHelp(
      "Add Competency",
      "Usage: deno run --allow-net --allow-env scripts/add-competency.ts [options]",
      `  --course-id <id>        Course ID (required if no --cluster-id)
  --cluster-id <id>       Cluster ID (use existing cluster)
  --cluster-name <name>   Cluster name (creates new or finds existing)
  --name <name>           Competency name (required)
  --description <desc>    Competency description`
    );
    Deno.exit(0);
  }

  const name = args.get("name") as string;
  if (!name) {
    console.error("Error: --name is required");
    Deno.exit(1);
  }

  const description = args.get("description") as string | undefined;
  let clusterId = args.get("cluster-id") as string | undefined;
  const courseId = args.get("course-id") as string | undefined;
  const clusterName = args.get("cluster-name") as string | undefined;

  // If no cluster-id, we need course-id and optionally cluster-name
  if (!clusterId) {
    if (!courseId) {
      console.error("Error: Either --cluster-id or --course-id is required");
      Deno.exit(1);
    }

    const targetClusterName = clusterName || "General";

    try {
      // Check if cluster exists
      const clusters = await listCompetencyClusters(courseId);
      const existing = clusters.find(
        (c) => c.name.toLowerCase() === targetClusterName.toLowerCase()
      );

      if (existing) {
        clusterId = existing.id;
        console.error(`Using existing cluster: ${existing.name}`);
      } else {
        // Create new cluster
        const newCluster = await createCompetencyCluster(courseId, {
          name: targetClusterName,
          description: `Competency cluster: ${targetClusterName}`,
        });
        clusterId = newCluster.id;
        console.error(`Created new cluster: ${newCluster.name}`);
      }
    } catch (error) {
      console.error(`Error with competency cluster: ${error}`);
      Deno.exit(1);
    }
  }

  try {
    const competency = await createCompetency(clusterId, {
      name,
      description,
    });

    if (args.has("json")) {
      console.log(JSON.stringify(competency, null, 2));
    } else {
      console.log(formatCompetency(competency));
    }
  } catch (error) {
    console.error(`Error creating competency: ${error}`);
    Deno.exit(1);
  }
}

main();

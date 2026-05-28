#!/usr/bin/env node
/**
 * Collect Azure DevOps work items changed recently
 * Usage: node azure-workitems.js --days <n>
 */

import { execSync } from "node:child_process"
import { mkdirSync, writeFileSync } from "node:fs"
import { join } from "node:path"

const args = process.argv.slice(2)
const daysIndex = args.indexOf("--days")
const days = daysIndex >= 0 ? parseInt(args[daysIndex + 1], 10) : 7

const outputDir = join(process.cwd(), ".insights", "raw")
const outputFile = join(outputDir, "workitems.json")

mkdirSync(outputDir, { recursive: true })

// WIQL query for recently changed work items
const wiql = `SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType], [System.AssignedTo], [System.ChangedDate], [System.CreatedDate] FROM WorkItems WHERE [System.ChangedDate] >= @Today - ${days} ORDER BY [System.ChangedDate] DESC`

try {
  // Query work items - use large buffer for big projects
  const queryResult = execSync(
    `az boards query --wiql "${wiql}" --output json`,
    { encoding: "utf8", maxBuffer: 50 * 1024 * 1024 },
  )

  const items = JSON.parse(queryResult)

  // Map to simpler structure
  const workItems = items.map((item) => {
    const id = item.fields?.["System.Id"] || item.id
    // Construct web URL from API URL: .../wit/workItems/{id} -> .../_workitems/edit/{id}
    const url = item.url
      ? item.url.replace(
          /\/_apis\/wit\/workItems\/.*/,
          `/_workitems/edit/${id}`,
        )
      : null
    const title = item.fields?.["System.Title"]
    return {
      id,
      title,
      type: item.fields?.["System.WorkItemType"],
      state: item.fields?.["System.State"],
      assignedTo: item.fields?.["System.AssignedTo"]?.displayName,
      changedDate: item.fields?.["System.ChangedDate"]?.slice(0, 10),
      createdDate: item.fields?.["System.CreatedDate"]?.slice(0, 10),
      url,
      link: url ? `[${title}](${url})` : title, // Pre-formatted markdown link
    }
  })

  writeFileSync(outputFile, JSON.stringify(workItems, null, 2))
  console.log(`Collected ${workItems.length} work items to: ${outputFile}`)
} catch (err) {
  console.error("Error fetching work items:", err.message)
  console.error(
    "Ensure az devops is configured: az devops configure --defaults organization=... project=...",
  )
  process.exit(1)
}

#!/usr/bin/env node
/**
 * Format raw data into markdown summary sections
 * Usage: echo '{"commits":[], "prs":[], "workitems":[]}' | node format-summary.js
 */

import { createInterface } from "node:readline"

async function readStdin() {
  const lines = []
  const rl = createInterface({ input: process.stdin })
  for await (const line of rl) {
    lines.push(line)
  }
  return lines.join("\n")
}

function formatPRs(prs) {
  if (!prs || prs.length === 0) return "No PR activity"

  const opened = prs.filter((p) => p.status === "active")
  const merged = prs.filter((p) => p.status === "completed")
  const abandoned = prs.filter((p) => p.status === "abandoned")

  const lines = []
  lines.push(`- **Opened:** ${opened.length}`)
  lines.push(`- **Merged:** ${merged.length}`)
  if (abandoned.length > 0) lines.push(`- **Abandoned:** ${abandoned.length}`)

  if (merged.length > 0) {
    lines.push("\n**Merged PRs:**")
    for (const pr of merged.slice(0, 10)) {
      // Use pre-formatted link field, fallback to title if not available
      lines.push(`- ${pr.link || pr.title} (${pr.author})`)
    }
  }

  if (opened.length > 0) {
    lines.push("\n**Open PRs:**")
    for (const pr of opened.slice(0, 10)) {
      lines.push(`- ${pr.link || pr.title} (${pr.author})`)
    }
  }

  return lines.join("\n")
}

function formatCommits(commits) {
  if (!commits || commits.length === 0) return "No commits"

  // Group by author
  const byAuthor = {}
  for (const c of commits) {
    if (!byAuthor[c.author]) byAuthor[c.author] = []
    byAuthor[c.author].push(c)
  }

  const lines = [`**Total:** ${commits.length} commits\n`]

  for (const [author, authorCommits] of Object.entries(byAuthor)) {
    lines.push(`**${author}** (${authorCommits.length}):`)
    for (const c of authorCommits.slice(0, 5)) {
      lines.push(`- \`${c.hash}\`: ${c.message}`)
    }
    if (authorCommits.length > 5) {
      lines.push(`- ... and ${authorCommits.length - 5} more`)
    }
    lines.push("")
  }

  return lines.join("\n")
}

function formatWorkItems(items) {
  if (!items || items.length === 0) return "No work item changes"

  // Group by state
  const byState = {}
  for (const item of items) {
    const state = item.state || "Unknown"
    if (!byState[state]) byState[state] = []
    byState[state].push(item)
  }

  const lines = [`**Total:** ${items.length} items changed\n`]

  for (const [state, stateItems] of Object.entries(byState)) {
    lines.push(`**${state}** (${stateItems.length}):`)
    for (const item of stateItems.slice(0, 5)) {
      const assignee = item.assignedTo ? ` (${item.assignedTo})` : ""
      // Use pre-formatted link field, fallback to title if not available
      lines.push(`- ${item.link || item.title}${assignee}`)
    }
    if (stateItems.length > 5) {
      lines.push(`- ... and ${stateItems.length - 5} more`)
    }
    lines.push("")
  }

  return lines.join("\n")
}

try {
  const input = await readStdin()
  const data = JSON.parse(input)

  const output = `### Pull Requests
${formatPRs(data.prs)}

### Commits
${formatCommits(data.commits)}

### Work Items
${formatWorkItems(data.workitems)}`

  console.log(output)
} catch (err) {
  console.error("Error:", err.message)
  process.exit(1)
}

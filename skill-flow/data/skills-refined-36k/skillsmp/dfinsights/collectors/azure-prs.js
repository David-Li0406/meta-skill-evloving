#!/usr/bin/env node
/**
 * Collect Azure DevOps PRs
 * Usage: node azure-prs.js --days <n>
 */

import { execSync } from "node:child_process"
import { mkdirSync, writeFileSync } from "node:fs"
import { join } from "node:path"

const args = process.argv.slice(2)
const daysIndex = args.indexOf("--days")
const days = daysIndex >= 0 ? parseInt(args[daysIndex + 1], 10) : 7

const outputDir = join(process.cwd(), ".insights", "raw")
const outputFile = join(outputDir, "prs.json")

mkdirSync(outputDir, { recursive: true })

function getDateNDaysAgo(n) {
  const date = new Date()
  date.setDate(date.getDate() - n)
  return date.toISOString().slice(0, 10)
}

const sinceDate = getDateNDaysAgo(days)

try {
  // Fetch all PRs (completed, active, abandoned) - large buffer for big repos
  const result = execSync(`az repos pr list --status all --output json`, {
    encoding: "utf8",
    maxBuffer: 50 * 1024 * 1024,
  })

  const allPRs = JSON.parse(result)

  // Filter to PRs created, closed, or updated within the date range
  const prs = allPRs
    .filter((pr) => {
      const createdDate = pr.creationDate?.slice(0, 10)
      const closedDate = pr.closedDate?.slice(0, 10)
      const updatedDate =
        pr.lastMergeSourceCommit?.committer?.date?.slice(0, 10) ||
        pr.closedDate?.slice(0, 10) ||
        pr.creationDate?.slice(0, 10)
      return (
        (createdDate && createdDate >= sinceDate) ||
        (closedDate && closedDate >= sinceDate) ||
        (updatedDate && updatedDate >= sinceDate)
      )
    })
    .map((pr) => {
      const url = pr.repository?.webUrl
        ? `${pr.repository.webUrl}/pullrequest/${pr.pullRequestId}`
        : null
      // Use most recent activity date for grouping (update > close > create)
      const updatedDate =
        pr.lastMergeSourceCommit?.committer?.date?.slice(0, 10) ||
        pr.closedDate?.slice(0, 10) ||
        pr.creationDate?.slice(0, 10)
      return {
        id: pr.pullRequestId,
        title: pr.title,
        author: pr.createdBy?.displayName || "Unknown",
        status: pr.status,
        sourceBranch: pr.sourceRefName?.replace("refs/heads/", ""),
        targetBranch: pr.targetRefName?.replace("refs/heads/", ""),
        createdDate: pr.creationDate?.slice(0, 10),
        closedDate: pr.closedDate?.slice(0, 10),
        updatedDate, // Primary date for grouping - most recent activity
        mergeStatus: pr.mergeStatus,
        reviewers: (pr.reviewers || []).map((r) => ({
          name: r.displayName,
          vote: r.vote, // 10=approved, 5=approved with suggestions, -5=wait, -10=rejected
        })),
        repository: pr.repository?.name,
        url, // Full URL - use this in reports, never construct manually
        link: url ? `[${pr.title}](${url})` : pr.title, // Pre-formatted markdown link
      }
    })

  writeFileSync(outputFile, JSON.stringify(prs, null, 2))
  console.log(`Collected ${prs.length} PRs to: ${outputFile}`)
} catch (err) {
  console.error("Error fetching PRs:", err.message)
  console.error(
    "Ensure az devops is configured: az devops configure --defaults organization=... project=...",
  )
  process.exit(1)
}

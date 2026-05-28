#!/usr/bin/env node
/**
 * Collect git commits from current repository
 * Usage: node git-commits.js --days <n>
 */

import { execSync } from "node:child_process"
import { mkdirSync, writeFileSync } from "node:fs"
import { join, basename } from "node:path"

const args = process.argv.slice(2)
const daysIndex = args.indexOf("--days")
const days = daysIndex >= 0 ? parseInt(args[daysIndex + 1], 10) : 7

const outputDir = join(process.cwd(), ".insights", "raw")
const outputFile = join(outputDir, "commits.json")

mkdirSync(outputDir, { recursive: true })

function getDateNDaysAgo(n) {
  const date = new Date()
  date.setDate(date.getDate() - n)
  return date.toISOString().slice(0, 10)
}

const sinceDate = getDateNDaysAgo(days)
const repoName = basename(process.cwd())

try {
  const gitLog = execSync(
    `git log --since="${sinceDate}" --format="%h|%cs|%an|%s"`,
    { encoding: "utf8", maxBuffer: 50 * 1024 * 1024 },
  ).trim()

  const commits = []

  if (gitLog) {
    for (const line of gitLog.split("\n")) {
      const [hash, date, author, ...messageParts] = line.split("|")
      const message = messageParts.join("|")

      commits.push({
        repo: repoName,
        hash,
        date,
        author,
        message,
      })
    }
  }

  writeFileSync(outputFile, JSON.stringify(commits, null, 2))
  console.log(`Collected ${commits.length} commits to: ${outputFile}`)
} catch (err) {
  console.error("Error collecting commits:", err.message)
  process.exit(1)
}

#!/usr/bin/env node
/**
 * Format raw insights data into significance-based monthly review
 * Usage: node format-review.js [--month YYYY-MM]
 *
 * Reads from .insights/raw/ and outputs markdown focusing on:
 * - High-impact initiatives (grouped by theme)
 * - Effort estimation based on PR count and revisions
 * - Top contributors by area
 * - Key observations
 */

import fs from "node:fs"
import path from "node:path"

const RAW_DIR = ".insights/raw"

// Theme detection patterns
const THEMES = {
  "Nuxt 4 / Framework": [
    "nuxt4",
    "nuxt 4",
    "nuxt3",
    "layer",
    "config refactor",
  ],
  "Performance (INP/CLS)": ["inp", "cls", "performance", "ttfb", "lcp"],
  "Registration / Auth": [
    "registration",
    "login",
    "auth",
    "customer",
    "my-account",
    "email change",
  ],
  "Reviews System": ["review", "rating"],
  "Checkout / Delivery": [
    "checkout",
    "delivery",
    "cart",
    "packeta",
    "shipping",
    "payment",
  ],
  "Catalog / PDP": [
    "catalog",
    "pdp",
    "product",
    "filter",
    "category",
    "search",
  ],
  "CMS / Content": ["cms", "banner", "pb-", "content", "pagebuilder"],
  Infrastructure: ["hotfix", "deploy", "ci", "pipeline", "docker"],
}

function classifyPR(pr) {
  const title = pr.title.toLowerCase()
  for (const [theme, patterns] of Object.entries(THEMES)) {
    if (patterns.some((p) => title.includes(p))) {
      return theme
    }
  }
  return "Other"
}

function estimateEffort(prs) {
  // High: 5+ PRs or multiple reverts/revisions
  // Medium: 2-4 PRs
  // Low: 1 PR
  const reverts = prs.filter((p) =>
    p.title.toLowerCase().includes("revert"),
  ).length
  const abandoned = prs.filter((p) => p.status === "abandoned").length

  if (prs.length >= 5 || reverts >= 2 || abandoned >= 3) return "HIGH"
  if (prs.length >= 2) return "MEDIUM"
  return "LOW"
}

function getStatus(prs) {
  const merged = prs.filter((p) => p.status === "completed").length
  const active = prs.filter((p) => p.status === "active").length
  const abandoned = prs.filter((p) => p.status === "abandoned").length

  if (abandoned > merged) return "Troubled"
  if (active > merged) return "In Review"
  if (merged === prs.length) return "Shipped"
  return "In Progress"
}

function formatReview(month) {
  const prs = JSON.parse(
    fs.readFileSync(path.join(RAW_DIR, "prs.json"), "utf8"),
  )
  const commits = JSON.parse(
    fs.readFileSync(path.join(RAW_DIR, "commits.json"), "utf8"),
  )

  let workitems = []
  try {
    workitems = JSON.parse(
      fs.readFileSync(path.join(RAW_DIR, "workitems.json"), "utf8"),
    )
  } catch {}

  // Filter by month if specified (prefer updatedDate over createdDate)
  const monthFilter = month ? (d) => d?.startsWith(month) : () => true
  const filteredPRs = prs.filter((p) =>
    monthFilter(p.updatedDate || p.createdDate),
  )
  const filteredCommits = commits.filter((c) => monthFilter(c.date))

  // Group PRs by theme
  const byTheme = {}
  filteredPRs.forEach((pr) => {
    const theme = classifyPR(pr)
    if (!byTheme[theme]) byTheme[theme] = []
    byTheme[theme].push(pr)
  })

  // Sort themes by PR count
  const sortedThemes = Object.entries(byTheme).sort(
    (a, b) => b[1].length - a[1].length,
  )

  // Author stats
  const authorStats = {}
  filteredPRs.forEach((pr) => {
    const author = pr.author
    if (!authorStats[author])
      authorStats[author] = { count: 0, themes: new Set() }
    authorStats[author].count++
    authorStats[author].themes.add(classifyPR(pr))
  })
  const topAuthors = Object.entries(authorStats)
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, 8)

  // Generate report
  const lines = []
  const periodLabel = month || "Period"

  lines.push(`# ${periodLabel} Monthly Review\n`)
  lines.push(
    `**PRs:** ${filteredPRs.length} (${filteredPRs.filter((p) => p.status === "completed").length} merged)`,
  )
  lines.push(`**Commits:** ${filteredCommits.length}`)
  lines.push(`**Work Items:** ${workitems.length}\n`)
  lines.push("---\n")

  // High-impact initiatives
  lines.push("## High-Impact Initiatives\n")

  let initNum = 1
  for (const [theme, themePRs] of sortedThemes.slice(0, 5)) {
    if (themePRs.length < 2 && theme === "Other") continue

    const effort = estimateEffort(themePRs)
    const status = getStatus(themePRs)

    lines.push(`### ${initNum}. ${theme}`)
    lines.push(`**Effort: ${effort} | Status: ${status}**\n`)

    // List key PRs (use pre-formatted link field)
    lines.push("Key PRs:")
    themePRs.slice(0, 5).forEach((pr) => {
      const icon =
        pr.status === "completed" ? "✅" : pr.status === "active" ? "🔄" : "❌"
      const shortAuthor = pr.author.split(" ")[0]
      lines.push(`- ${icon} ${pr.link || pr.title} (${shortAuthor})`)
    })
    if (themePRs.length > 5) {
      lines.push(`- ... and ${themePRs.length - 5} more`)
    }
    lines.push("")
    initNum++
  }

  lines.push("---\n")

  // Top contributors
  lines.push("## Top Contributors\n")
  lines.push("| Contributor | PRs | Focus Area |")
  lines.push("|-------------|-----|------------|")
  topAuthors.forEach(([author, stats]) => {
    const focus = [...stats.themes].slice(0, 2).join(", ")
    lines.push(`| ${author} | ${stats.count} | ${focus} |`)
  })
  lines.push("")

  lines.push("---\n")

  // Theme summary table
  lines.push("## Themes Summary\n")
  lines.push("| Theme | PRs | Merged | Status |")
  lines.push("|-------|-----|--------|--------|")
  sortedThemes.forEach(([theme, themePRs]) => {
    const merged = themePRs.filter((p) => p.status === "completed").length
    const status = getStatus(themePRs)
    lines.push(`| ${theme} | ${themePRs.length} | ${merged} | ${status} |`)
  })
  lines.push("")

  // Observations
  lines.push("---\n")
  lines.push("## Key Observations\n")

  const activeCount = filteredPRs.filter((p) => p.status === "active").length
  const abandonedCount = filteredPRs.filter(
    (p) => p.status === "abandoned",
  ).length
  const mergeRate = Math.round(
    (filteredPRs.filter((p) => p.status === "completed").length /
      filteredPRs.length) *
      100,
  )

  if (activeCount > 10) {
    lines.push(`- **Review bottleneck:** ${activeCount} PRs still in review`)
  }
  if (abandonedCount > 3) {
    lines.push(
      `- **Iteration churn:** ${abandonedCount} PRs abandoned (rework/reverts)`,
    )
  }
  lines.push(`- **Merge rate:** ${mergeRate}%`)

  // Find most active theme
  if (sortedThemes.length > 0) {
    const [topTheme, topPRs] = sortedThemes[0]
    lines.push(`- **Primary focus:** ${topTheme} (${topPRs.length} PRs)`)
  }

  lines.push("\n---\n")
  lines.push("*Generated by .insights/format-review.js*")

  return lines.join("\n")
}

// CLI
const args = process.argv.slice(2)
let month = null
const monthIdx = args.indexOf("--month")
if (monthIdx !== -1 && args[monthIdx + 1]) {
  month = args[monthIdx + 1]
}

console.log(formatReview(month))

#!/usr/bin/env -S deno run --allow-read --allow-write --allow-net

/**
 * Insights Dashboard Generator
 *
 * Reads .insights/ data and generates a self-contained HTML dashboard.
 *
 * Usage:
 *   deno run --allow-read --allow-write --allow-net generate.ts [options]
 *
 * Options:
 *   --output <path>   Output path (default: .insights/dashboard.html)
 *   --serve           Start local server instead of writing file
 *   --port <n>        Server port (default: 3456)
 *   --open            Open browser after generation/serve
 */

import { parse } from "https://deno.land/std@0.224.0/flags/mod.ts"
import {
  join,
  dirname,
  fromFileUrl,
} from "https://deno.land/std@0.224.0/path/mod.ts"
import { exists } from "https://deno.land/std@0.224.0/fs/exists.ts"

const CHART_JS_URL =
  "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"
const MARKED_URL = "https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.js"

interface RawData {
  prs: unknown[]
  commits: unknown[]
  workitems: unknown[]
  confluence: unknown[]
}

interface Report {
  name: string
  content: string
}

async function fetchLib(url: string): Promise<string> {
  console.log(`Fetching ${url}...`)
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(`Failed to fetch ${url}: ${response.status}`)
  }
  return response.text()
}

async function readJsonFile(path: string): Promise<unknown[]> {
  try {
    const content = await Deno.readTextFile(path)
    return JSON.parse(content)
  } catch {
    return []
  }
}

async function readReports(insightsDir: string): Promise<Report[]> {
  const reports: Report[] = []
  try {
    for await (const entry of Deno.readDir(insightsDir)) {
      if (
        entry.isFile &&
        entry.name.endsWith(".md") &&
        entry.name.includes("insights")
      ) {
        const content = await Deno.readTextFile(join(insightsDir, entry.name))
        reports.push({ name: entry.name, content })
      }
    }
  } catch {
    // Directory doesn't exist or is empty
  }
  return reports
}

async function generateDashboard(insightsDir: string): Promise<string> {
  // Read raw data
  const rawDir = join(insightsDir, "raw")
  const data: RawData = {
    prs: await readJsonFile(join(rawDir, "prs.json")),
    commits: await readJsonFile(join(rawDir, "commits.json")),
    workitems: await readJsonFile(join(rawDir, "workitems.json")),
    confluence: await readJsonFile(join(rawDir, "confluence.json")),
  }

  // Read reports
  const reports = await readReports(insightsDir)

  // Fetch libraries
  const [chartJs, markedJs] = await Promise.all([
    fetchLib(CHART_JS_URL),
    fetchLib(MARKED_URL),
  ])

  // Read template
  const scriptDir = dirname(fromFileUrl(import.meta.url))
  const templatePath = join(scriptDir, "template.html")
  let template = await Deno.readTextFile(templatePath)

  // Inject libraries
  template = template.replace(
    "<!-- CHARTJS_PLACEHOLDER -->",
    `<script>${chartJs}</script>`,
  )
  template = template.replace(
    "<!-- MARKED_PLACEHOLDER -->",
    `<script>${markedJs}</script>`,
  )

  // Inject data
  template = template.replace("{{DATA}}", JSON.stringify(data))
  template = template.replace("{{REPORTS}}", JSON.stringify(reports))

  return template
}

async function startServer(html: string, port: number) {
  console.log(`Starting server on http://localhost:${port}`)
  Deno.serve({ port }, () => {
    return new Response(html, {
      headers: { "content-type": "text/html; charset=utf-8" },
    })
  })
}

async function openBrowser(url: string) {
  const cmd =
    Deno.build.os === "darwin"
      ? ["open", url]
      : Deno.build.os === "windows"
        ? ["cmd", "/c", "start", url]
        : ["xdg-open", url]

  try {
    const process = new Deno.Command(cmd[0], { args: cmd.slice(1) })
    await process.output()
  } catch {
    console.log(`Open ${url} in your browser`)
  }
}

async function main() {
  const args = parse(Deno.args, {
    string: ["output", "port", "insights-dir"],
    boolean: ["serve", "open", "help"],
    default: {
      output: ".insights/dashboard.html",
      port: "3456",
      "insights-dir": ".insights",
      serve: false,
      open: false,
    },
  })

  if (args.help) {
    console.log(`
Insights Dashboard Generator

Usage:
  deno run --allow-read --allow-write --allow-net generate.ts [options]

Options:
  --output <path>       Output path (default: .insights/dashboard.html)
  --insights-dir <dir>  Insights directory (default: .insights)
  --serve               Start local server instead of writing file
  --port <n>            Server port (default: 3456)
  --open                Open browser after generation/serve
  --help                Show this help
`)
    Deno.exit(0)
  }

  const insightsDir = args["insights-dir"] as string

  // Check if insights directory exists
  if (!(await exists(insightsDir))) {
    console.error(`Error: Insights directory not found: ${insightsDir}`)
    console.error(
      "Run /df:insights:daily or /df:insights:catchup first to generate data.",
    )
    Deno.exit(1)
  }

  console.log("Generating dashboard...")
  const html = await generateDashboard(insightsDir)

  if (args.serve) {
    const port = parseInt(args.port as string, 10)
    if (args.open) {
      setTimeout(() => openBrowser(`http://localhost:${port}`), 500)
    }
    await startServer(html, port)
  } else {
    const outputPath = args.output as string
    await Deno.writeTextFile(outputPath, html)
    console.log(`Dashboard generated: ${outputPath}`)

    if (args.open) {
      await openBrowser(outputPath)
    }
  }
}

main()

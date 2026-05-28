#!/usr/bin/env node

// Clean error output - suppress verbose stack traces
process.on("uncaughtException", (e) => {
  console.error(`✗ ${e.message}`)
  process.exit(1)
})
process.on("unhandledRejection", (e) => {
  console.error(`✗ ${e.message}`)
  process.exit(1)
})

import { spawn, execSync } from "node:child_process"
import { tmpdir } from "node:os"
import { join } from "node:path"
import puppeteer from "puppeteer-core"

const useProfile = process.argv[2] === "--profile"

if (process.argv[2] && process.argv[2] !== "--profile") {
  console.log("Usage: browser-start.js [--profile]")
  console.log("\nOptions:")
  console.log("  --profile  Use persistent Chrome profile")
  console.log("\nExamples:")
  console.log("  browser-start.js            # Start with fresh profile")
  console.log("  browser-start.js --profile  # Start with persistent profile")
  process.exit(1)
}

// Kill existing Chrome
try {
  execSync("killall google-chrome chrome", { stdio: "ignore" })
} catch {}

// Wait a bit for processes to fully die
await new Promise((r) => setTimeout(r, 1000))

// Setup profile directory
const profileDir = useProfile
  ? "/tmp/chrome-profile-browser-tools"
  : join(tmpdir(), `chrome-profile-${Date.now()}`)

execSync(`mkdir -p "${profileDir}"`, { stdio: "ignore" })

// Start Chrome in background (detached so Node can exit)
spawn(
  "google-chrome",
  ["--remote-debugging-port=9222", `--user-data-dir=${profileDir}`],
  { detached: true, stdio: "ignore" },
).unref()

// Wait for Chrome to be ready by attempting to connect
let connected = false
for (let i = 0; i < 30; i++) {
  try {
    const browser = await puppeteer.connect({
      browserURL: "http://localhost:9222",
      defaultViewport: null,
    })
    await browser.disconnect()
    // Brief delay to let Chrome fully stabilize after initial connection
    await new Promise((r) => setTimeout(r, 500))
    connected = true
    break
  } catch {
    await new Promise((r) => setTimeout(r, 500))
  }
}

if (!connected) {
  console.error("✗ Failed to connect to Chrome")
  process.exit(1)
}

console.log(
  `✓ Chrome started on :9222${useProfile ? " with persistent profile" : ""}`,
)

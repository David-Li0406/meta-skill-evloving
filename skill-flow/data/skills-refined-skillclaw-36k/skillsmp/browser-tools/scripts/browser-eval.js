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

import puppeteer from "puppeteer-core"

const code = process.argv.slice(2).join(" ")
if (!code) {
  console.log("Usage: browser-eval.js 'code'")
  console.log("\nExamples:")
  console.log('  browser-eval.js "document.title"')
  console.log("  browser-eval.js \"document.querySelectorAll('a').length\"")
  process.exit(1)
}

const b = await puppeteer.connect({
  browserURL: "http://localhost:9222",
  defaultViewport: null,
})

const p = (await b.pages()).at(-1)

if (!p) {
  console.error("✗ No active tab found")
  process.exit(1)
}

const result = await p.evaluate((c) => {
  const AsyncFunction = (async () => {}).constructor
  // Try as expression first, fall back to statements
  try {
    return new AsyncFunction(`return (${c})`)()
  } catch {
    return new AsyncFunction(c)()
  }
}, code)

if (Array.isArray(result)) {
  for (let i = 0; i < result.length; i++) {
    if (i > 0) console.log("")
    for (const [key, value] of Object.entries(result[i])) {
      console.log(`${key}: ${value}`)
    }
  }
} else if (typeof result === "object" && result !== null) {
  for (const [key, value] of Object.entries(result)) {
    console.log(`${key}: ${value}`)
  }
} else {
  console.log(result)
}

await b.disconnect()

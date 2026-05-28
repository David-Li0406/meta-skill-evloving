#!/usr/bin/env node
/**
 * Filter raw data JSON by date range
 * Usage: node filter-by-date.js <input.json> <mode> [date]
 *
 * Modes:
 *   --day YYYY-MM-DD     Filter single day
 *   --week YYYY-MM-DD    Filter week containing date (Mon-Sun)
 *   --range START END    Filter date range (inclusive)
 */

import { readFile } from "node:fs/promises"

const args = process.argv.slice(2)
const inputFile = args[0]
const mode = args[1]

if (!inputFile || !mode) {
  console.error(
    "Usage: node filter-by-date.js <input.json> --day|--week|--range <date(s)>",
  )
  process.exit(1)
}

function getWeekRange(dateStr) {
  const date = new Date(dateStr)
  const day = date.getDay()
  // Adjust to Monday (day 0 = Sunday, so Monday = 1)
  const mondayOffset = day === 0 ? -6 : 1 - day
  const monday = new Date(date)
  monday.setDate(date.getDate() + mondayOffset)
  const sunday = new Date(monday)
  sunday.setDate(monday.getDate() + 6)
  return {
    start: monday.toISOString().slice(0, 10),
    end: sunday.toISOString().slice(0, 10),
  }
}

function getISOWeek(dateStr) {
  const date = new Date(dateStr)
  const thursday = new Date(date)
  thursday.setDate(date.getDate() + (4 - (date.getDay() || 7)))
  const yearStart = new Date(thursday.getFullYear(), 0, 1)
  const weekNumber = Math.ceil(((thursday - yearStart) / 86400000 + 1) / 7)
  return `${thursday.getFullYear()}-W${String(weekNumber).padStart(2, "0")}`
}

function isInRange(itemDate, start, end) {
  return itemDate >= start && itemDate <= end
}

function getItemDate(item) {
  // Prefer updatedDate (most recent activity) over createdDate
  // This ensures PRs appear in reports for when they were last active, not just created
  return item.updatedDate || item.date || item.changedDate || item.createdDate
}

try {
  const data = JSON.parse(await readFile(inputFile, "utf8"))
  let filtered
  let weekInfo = null

  switch (mode) {
    case "--day": {
      const day = args[2] || new Date().toISOString().slice(0, 10)
      filtered = data.filter((item) => getItemDate(item) === day)
      break
    }
    case "--week": {
      const date = args[2] || new Date().toISOString().slice(0, 10)
      const { start, end } = getWeekRange(date)
      weekInfo = { start, end, isoWeek: getISOWeek(date) }
      filtered = data.filter((item) => isInRange(getItemDate(item), start, end))
      console.error(`Week: ${start} to ${end} (${weekInfo.isoWeek})`)
      break
    }
    case "--range": {
      const [start, end] = args.slice(2)
      if (!start || !end)
        throw new Error("Range requires start and end: --range START END")
      filtered = data.filter((item) => isInRange(getItemDate(item), start, end))
      break
    }
    default:
      throw new Error(`Unknown mode: ${mode}`)
  }

  console.log(JSON.stringify(filtered, null, 2))
} catch (err) {
  console.error("Error:", err.message)
  process.exit(1)
}

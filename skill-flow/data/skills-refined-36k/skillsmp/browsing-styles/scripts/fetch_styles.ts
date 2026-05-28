#!/usr/bin/env bun
/**
 * Fetch reference images from museum APIs
 * Primary source: Metropolitan Museum of Art (CC0, no auth required)
 */

import { readFileSync, mkdirSync, existsSync, writeFileSync } from "node:fs"
import { resolve, dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { homedir } from "node:os"

const __dirname = dirname(fileURLToPath(import.meta.url))
const STYLES_PATH = resolve(__dirname, "../../../styles/styles.json")
const CACHE_DIR = join(homedir(), ".cache", "gemskills", "styles")

interface StyleSource {
  api: string
  objectId: number
  title: string
}

interface Style {
  id: string
  shortName: string
  name: string
  category: string
  promptHints: string
  sources: StyleSource[]
}

interface StylesRegistry {
  styles: Style[]
}

interface MetObject {
  objectID: number
  primaryImage: string
  primaryImageSmall: string
  title: string
  artistDisplayName: string
}

function loadStyles(): StylesRegistry {
  const content = readFileSync(STYLES_PATH, "utf-8")
  return JSON.parse(content)
}

function parseArgs(): { style?: string; force: boolean } {
  const args = process.argv.slice(2)
  const result: ReturnType<typeof parseArgs> = { force: false }

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]
    if (arg === "--style" && args[i + 1]) {
      result.style = args[++i]
    } else if (arg === "--force") {
      result.force = true
    }
  }

  return result
}

async function fetchMetObject(objectId: number): Promise<MetObject | null> {
  const url = `https://collectionapi.metmuseum.org/public/collection/v1/objects/${objectId}`
  try {
    const response = await fetch(url)
    if (!response.ok) {
      console.error(`  Failed to fetch Met object ${objectId}: ${response.status}`)
      return null
    }
    return (await response.json()) as MetObject
  } catch (error) {
    console.error(`  Error fetching Met object ${objectId}:`, error)
    return null
  }
}

async function downloadImage(url: string, path: string): Promise<boolean> {
  try {
    const response = await fetch(url)
    if (!response.ok) {
      console.error(`  Failed to download image: ${response.status}`)
      return false
    }
    const buffer = await response.arrayBuffer()
    writeFileSync(path, Buffer.from(buffer))
    return true
  } catch (error) {
    console.error(`  Error downloading image:`, error)
    return false
  }
}

async function fetchStyleImages(style: Style, force: boolean): Promise<void> {
  const styleDir = join(CACHE_DIR, style.id)

  // Check if already cached
  const thumbPath = join(styleDir, "thumb.jpg")
  if (!force && existsSync(thumbPath)) {
    console.log(`  [cached] ${style.name}`)
    return
  }

  // Create style directory
  mkdirSync(styleDir, { recursive: true })

  // Filter to Met API sources only
  const metSources = style.sources.filter((s) => s.api === "met")
  if (metSources.length === 0) {
    console.log(`  [no sources] ${style.name}`)
    return
  }

  let imageCount = 0
  for (let i = 0; i < metSources.length && imageCount < 3; i++) {
    const source = metSources[i]
    console.log(`  Fetching: ${source.title} (${source.objectId})`)

    const obj = await fetchMetObject(source.objectId)
    if (!obj || !obj.primaryImage) {
      console.log(`    No image available`)
      continue
    }

    // Download full resolution
    const refPath = join(styleDir, `ref-${imageCount + 1}.jpg`)
    const downloaded = await downloadImage(obj.primaryImage, refPath)
    if (!downloaded) continue

    // Use small image as thumbnail for first image
    if (imageCount === 0 && obj.primaryImageSmall) {
      await downloadImage(obj.primaryImageSmall, thumbPath)
    }

    imageCount++
    console.log(`    Downloaded: ref-${imageCount}.jpg`)

    // Rate limit: Met API requests
    await new Promise((r) => setTimeout(r, 100))
  }

  if (imageCount === 0) {
    console.log(`  [no images found] ${style.name}`)
  } else {
    console.log(`  [done] ${style.name}: ${imageCount} images`)
  }
}

async function main(): Promise<void> {
  const opts = parseArgs()
  const registry = loadStyles()

  console.log(`Cache directory: ${CACHE_DIR}`)
  mkdirSync(CACHE_DIR, { recursive: true })

  let styles = registry.styles
  if (opts.style) {
    styles = styles.filter((s) => s.id === opts.style || s.shortName === opts.style)
    if (styles.length === 0) {
      console.error(`Style not found: ${opts.style}`)
      process.exit(1)
    }
  }

  console.log(`\nFetching ${styles.length} styles...\n`)

  for (const style of styles) {
    console.log(`[${style.shortName}] ${style.name}`)
    await fetchStyleImages(style, opts.force)
  }

  console.log("\nDone!")
}

main()

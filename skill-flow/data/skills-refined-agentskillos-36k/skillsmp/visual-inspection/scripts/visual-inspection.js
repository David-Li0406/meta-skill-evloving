#!/usr/bin/env node
/**
 * Visual Inspection Helper Script
 *
 * This script provides utilities for the visual-inspection skill.
 * The main Playwright MCP workflow is executed directly by Claude using MCP tools.
 *
 * This script can be used to:
 * - Check if the dev server is running
 * - Validate screenshot file naming conventions
 * - Clean up old screenshots
 */

import { existsSync, readdirSync, statSync, unlinkSync } from 'node:fs'
import { join } from 'node:path'
import { spawn } from 'node:child_process'

/**
 * Check if the dev server is running
 * @param {string} url - The URL to check
 * @returns {Promise<boolean>}
 */
const checkDevServer = async (url = 'http://localhost:4321') => {
    try {
        const response = await fetch(url, { signal: AbortSignal.timeout(2000) })
        if (response.ok) {
            console.log(`✓ Dev server is running at ${url}`)
            return true
        }
        console.log(`✗ Dev server is NOT running at ${url}`)
        return false
    } catch {
        console.log(`✗ Dev server is NOT running at ${url}`)
        return false
    }
}

/**
 * Start the dev server in the background
 * @returns {Promise<boolean>}
 */
const startDevServer = async () => {
    try {
        console.log("Starting dev server with 'pnpm dev'...")

        const proc = spawn('pnpm', ['dev'], {
            detached: true,
            stdio: 'ignore',
        })

        proc.unref()

        console.log('✓ Dev server started. Waiting for it to be ready...')

        // Wait for server to start (max 30 seconds)
        for (let i = 0; i < 30; i++) {
            await new Promise((resolve) => setTimeout(resolve, 1000))
            if (await checkDevServer()) {
                return true
            }
        }

        console.log('✗ Server did not start within 30 seconds')
        return false
    } catch {
        console.log('✗ Error: Could not start dev server. Is pnpm installed?')
        return false
    }
}

/**
 * Stop the dev server by killing processes on port 4321
 * @returns {Promise<boolean>}
 */
const stopDevServer = async () => {
    try {
        // First check if server is even running
        const isRunning = await checkDevServer()
        if (!isRunning) {
            console.log('✓ Dev server is not running, nothing to stop')
            return true
        }

        console.log('Stopping dev server on port 4321...')

        // Use lsof to find processes on port 4321 and kill them
        const { execSync } = await import('node:child_process')

        try {
            // Get PIDs of processes listening on port 4321
            const output = execSync('lsof -ti :4321', { encoding: 'utf-8' })
            const pids = output.trim().split('\n').filter(Boolean)

            if (pids.length === 0) {
                console.log('✓ No processes found on port 4321')
                return true
            }

            // Kill each process
            for (const pid of pids) {
                try {
                    execSync(`kill ${pid}`)
                    console.log(`✓ Killed process ${pid}`)
                } catch {
                    // Process may have already exited
                }
            }

            // Verify server is stopped
            await new Promise((resolve) => setTimeout(resolve, 1000))
            const stillRunning = await checkDevServer()

            if (stillRunning) {
                console.log('✗ Server is still running after kill attempt')
                return false
            }

            console.log('✓ Dev server stopped successfully')
            return true
        } catch {
            // lsof returns non-zero if no processes found
            console.log('✓ No processes found on port 4321')
            return true
        }
    } catch (error) {
        console.log(`✗ Error stopping dev server: ${error.message}`)
        return false
    }
}

/**
 * Validate screenshot filename follows conventions
 * Expected format: {viewport}-{pagename}-YYYY-MM-DD.png
 * Example: desktop-homepage-2026-01-09.png
 * @param {string} filename
 * @returns {{ isValid: boolean; message: string }}
 */
const validateFilename = (filename) => {
    const parts = filename.replace('.png', '').split('-')

    if (parts.length < 4) {
        return {
            isValid: false,
            message:
                'Filename must include: viewport, pagename, and date (YYYY-MM-DD)',
        }
    }

    const viewport = parts[0]
    if (!['desktop', 'tablet', 'mobile'].includes(viewport)) {
        return {
            isValid: false,
            message: `Invalid viewport '${viewport}'. Must be: desktop, tablet, or mobile`,
        }
    }

    // Check if last 3 parts form a valid date (YYYY-MM-DD)
    try {
        const dateStr = parts.slice(-3).join('-')
        const date = new Date(dateStr)
        if (isNaN(date.getTime())) {
            throw new Error('Invalid date')
        }
        // Verify it matches the format
        if (!/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
            throw new Error('Invalid date format')
        }
    } catch {
        return {
            isValid: false,
            message: 'Filename must end with date in YYYY-MM-DD format',
        }
    }

    return { isValid: true, message: 'Valid filename' }
}

/**
 * Remove screenshots older than specified days
 * @param {number} days
 */
const cleanOldScreenshots = (days = 7) => {
    const screenshotsDir = '.playwright-mcp'

    if (!existsSync(screenshotsDir)) {
        console.log(`✗ Directory ${screenshotsDir} does not exist`)
        return
    }

    const cutoffDate = new Date()
    cutoffDate.setDate(cutoffDate.getDate() - days)

    const files = readdirSync(screenshotsDir).filter((f) => f.endsWith('.png'))
    let removedCount = 0

    for (const file of files) {
        const filepath = join(screenshotsDir, file)
        const stats = statSync(filepath)

        if (stats.mtime < cutoffDate) {
            unlinkSync(filepath)
            removedCount++
            console.log(`Removed old screenshot: ${file}`)
        }
    }

    console.log(`✓ Removed ${removedCount} screenshots older than ${days} days`)
}

/**
 * List all screenshots with metadata
 */
const listScreenshots = () => {
    const screenshotsDir = '.playwright-mcp'

    if (!existsSync(screenshotsDir)) {
        console.log(`✗ Directory ${screenshotsDir} does not exist`)
        return
    }

    const files = readdirSync(screenshotsDir).filter((f) => f.endsWith('.png'))

    if (files.length === 0) {
        console.log('No screenshots found in .playwright-mcp/')
        return
    }

    const screenshots = files
        .map((file) => {
            const filepath = join(screenshotsDir, file)
            const stats = statSync(filepath)
            const { isValid } = validateFilename(file)

            return {
                filename: file,
                sizeKB: stats.size / 1024,
                modified: stats.mtime,
                isValid,
            }
        })
        .sort((a, b) => b.modified.getTime() - a.modified.getTime())

    console.log(`\nFound ${screenshots.length} screenshots:\n`)
    console.log(
        `${'Filename'.padEnd(50)} ${'Size'.padEnd(10)} ${'Modified'.padEnd(20)} ${'Valid'.padEnd(10)}`
    )
    console.log('-'.repeat(95))

    for (const screenshot of screenshots) {
        const sizeStr = `${screenshot.sizeKB.toFixed(1)}KB`
        const modifiedStr = screenshot.modified
            .toISOString()
            .slice(0, 19)
            .replace('T', ' ')
        const validStr = screenshot.isValid ? '✓' : '✗'

        console.log(
            `${screenshot.filename.padEnd(50)} ${sizeStr.padEnd(10)} ${modifiedStr.padEnd(20)} ${validStr.padEnd(10)}`
        )
    }
}

/**
 * Main CLI entry point
 */
const main = async () => {
    const args = process.argv.slice(2)
    const command = args[0]

    if (!command) {
        console.log(`
Visual Inspection Helper - Utilities for the visual-inspection skill

Usage:
  node visual-inspection.js <command> [options]

Commands:
  check-server              Check if dev server is running
  start-server              Start the dev server
  stop-server               Stop the dev server (kills processes on port 4321)
  clean [--days N]          Remove screenshots older than N days (default: 7)
  list                      List all screenshots with metadata
  validate <filename>       Validate screenshot filename

Examples:
  node visual-inspection.js check-server
  node visual-inspection.js stop-server
  node visual-inspection.js clean --days 14
  node visual-inspection.js validate desktop-homepage-2026-01-09.png
		`)
        process.exit(1)
    }

    switch (command) {
        case 'check-server': {
            const isRunning = await checkDevServer()
            process.exit(isRunning ? 0 : 1)
        }

        case 'start-server': {
            const started = await startDevServer()
            process.exit(started ? 0 : 1)
        }

        case 'stop-server': {
            const stopped = await stopDevServer()
            process.exit(stopped ? 0 : 1)
        }

        case 'clean': {
            const daysIndex = args.indexOf('--days')
            const days =
                daysIndex !== -1 ? parseInt(args[daysIndex + 1], 10) : 7
            cleanOldScreenshots(days)
            process.exit(0)
        }

        case 'list': {
            listScreenshots()
            process.exit(0)
        }

        case 'validate': {
            const filename = args[1]
            if (!filename) {
                console.log('✗ Error: Please provide a filename to validate')
                process.exit(1)
            }
            const { isValid, message } = validateFilename(filename)
            console.log(`${filename}: ${message}`)
            process.exit(isValid ? 0 : 1)
        }

        default: {
            console.log(`✗ Unknown command: ${command}`)
            process.exit(1)
        }
    }
}

main()

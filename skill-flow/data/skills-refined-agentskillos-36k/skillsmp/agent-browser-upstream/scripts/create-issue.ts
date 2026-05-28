#!/usr/bin/env bun
/**
 * Create a GitHub issue from a markdown file with YAML frontmatter.
 *
 * Usage:
 *   bun run create-issue.ts <path-to-integration.md>
 *   bun run create-issue.ts docs/_upstream/v0.6.0/integration.md
 *
 * Frontmatter format:
 *   ---
 *   issue:
 *     title: "Issue title"
 *     labels: [label1, label2]
 *   ---
 *
 * The markdown body (after frontmatter) becomes the issue body.
 */

import { parseArgs } from 'util'
import { $ } from 'bun'
import { parse as parseYaml } from 'yaml'

interface IssueFrontmatter {
	issue: {
		title: string
		labels?: string[]
		assignees?: string[]
		milestone?: string
	}
	[key: string]: unknown
}

function parseFrontmatter(content: string): {
	frontmatter: IssueFrontmatter
	body: string
} {
	const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)

	if (!match) {
		throw new Error('No YAML frontmatter found. File must start with ---')
	}

	const [, yamlContent, body] = match
	const frontmatter = parseYaml(yamlContent) as IssueFrontmatter

	if (!frontmatter.issue?.title) {
		throw new Error('Frontmatter must have issue.title')
	}

	return { frontmatter, body: body.trim() }
}

async function createIssue(
	title: string,
	body: string,
	labels: string[] = [],
	dryRun = false,
): Promise<string> {
	const labelArgs = labels.length > 0 ? ['--label', labels.join(',')] : []

	if (dryRun) {
		console.log('=== DRY RUN ===')
		console.log(`Title: ${title}`)
		console.log(`Labels: ${labels.join(', ') || '(none)'}`)
		console.log(`Body length: ${body.length} chars`)
		console.log('\n--- Body Preview (first 500 chars) ---')
		console.log(body.slice(0, 500))
		if (body.length > 500) console.log('...')
		return 'dry-run'
	}

	// Create the issue using gh CLI
	const result =
		await $`gh issue create --title ${title} --body ${body} ${labelArgs}`.text()

	// gh issue create returns the URL of the created issue
	return result.trim()
}

async function main() {
	const { values, positionals } = parseArgs({
		args: Bun.argv.slice(2),
		options: {
			'dry-run': { type: 'boolean', short: 'n' },
			help: { type: 'boolean', short: 'h' },
		},
		allowPositionals: true,
	})

	if (values.help || positionals.length === 0) {
		console.log(`
Usage: bun run create-issue.ts [options] <file.md>

Creates a GitHub issue from a markdown file with YAML frontmatter.

Arguments:
  <file.md>       Path to markdown file with issue frontmatter

Options:
  -n, --dry-run   Show what would be created without creating
  -h, --help      Show this help

Frontmatter format:
  ---
  issue:
    title: "chore(deps): integrate agent-browser v0.6.0"
    labels: [dependencies, chore]
  ---

  # Markdown body becomes issue body
`)
		process.exit(values.help ? 0 : 1)
	}

	const filePath = positionals[0]
	const file = Bun.file(filePath)

	if (!(await file.exists())) {
		console.error(`Error: File not found: ${filePath}`)
		process.exit(1)
	}

	const content = await file.text()

	try {
		const { frontmatter, body } = parseFrontmatter(content)
		const { title, labels = [] } = frontmatter.issue

		console.log(`Creating issue: ${title}`)

		const url = await createIssue(title, body, labels, values['dry-run'])

		if (!values['dry-run']) {
			console.log(`\nCreated: ${url}`)
		}
	} catch (err) {
		console.error(`Error: ${(err as Error).message}`)
		process.exit(1)
	}
}

main()

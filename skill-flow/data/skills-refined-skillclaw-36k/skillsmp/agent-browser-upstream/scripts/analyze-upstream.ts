#!/usr/bin/env bun
/**
 * Analyze upstream agent-browser changes between two refs.
 *
 * Usage:
 *   bun run analyze-upstream.ts [--base origin/main] [--target upstream/main]
 *
 * The script uses .agent-browser/repo/ in the navigator repo root by default.
 * If missing, it clones the fork automatically.
 *
 * Output: JSON with categorized commits and file changes
 */

import { dirname, join } from 'path'
import { parseArgs } from 'util'
import { $ } from 'bun'

const FORK_URL = 'git@github.com:outfitter-dev/agent-browser.git'
const UPSTREAM_URL = 'git@github.com:vercel-labs/agent-browser.git'

// Validate git ref to prevent command injection
// Valid refs: alphanumeric, /, ., -, _ (no shell metacharacters)
function isValidGitRef(ref: string): boolean {
	return /^[a-zA-Z0-9._\/-]+$/.test(ref) && !ref.startsWith('-')
}

interface Commit {
	sha: string
	shortSha: string
	message: string
	type: CommitType
	scope?: string
	breaking: boolean
	body?: string
}

type CommitType =
	| 'feat'
	| 'fix'
	| 'docs'
	| 'chore'
	| 'refactor'
	| 'test'
	| 'style'
	| 'perf'
	| 'ci'
	| 'build'
	| 'unknown'

interface FileChange {
	path: string
	additions: number
	deletions: number
	status: 'A' | 'M' | 'D' | 'R' | 'C'
}

interface AnalysisResult {
	meta: {
		repo: string
		base: string
		target: string
		analyzedAt: string
	}
	summary: {
		totalCommits: number
		breaking: number
		additive: number
		fixes: number
		docs: number
		other: number
	}
	commits: {
		breaking: Commit[]
		additive: Commit[]
		fixes: Commit[]
		docs: Commit[]
		other: Commit[]
	}
	files: {
		critical: FileChange[] // protocol.ts, browser.ts, index.ts
		all: FileChange[]
	}
}

const CRITICAL_FILES = [
	'src/protocol.ts',
	'src/browser.ts',
	'src/index.ts',
	'src/types.ts',
]

function parseConventionalCommit(message: string): {
	type: CommitType
	scope?: string
	breaking: boolean
	description: string
} {
	// Match: type(scope)!: description or type!: description or type(scope): description
	const match = message.match(/^(\w+)(?:\(([^)]+)\))?(!)?\s*:\s*(.+?)(?:\n|$)/)

	if (!match) {
		return {
			type: 'unknown',
			breaking: message.toLowerCase().includes('breaking'),
			description: message.split('\n')[0],
		}
	}

	const [, rawType, scope, bang, description] = match
	const type = rawType.toLowerCase() as CommitType
	const validTypes: CommitType[] = [
		'feat',
		'fix',
		'docs',
		'chore',
		'refactor',
		'test',
		'style',
		'perf',
		'ci',
		'build',
	]

	return {
		type: validTypes.includes(type) ? type : 'unknown',
		scope: scope || undefined,
		breaking: !!bang || message.toLowerCase().includes('breaking change'),
		description,
	}
}

function categorizeCommit(commit: Commit): keyof AnalysisResult['commits'] {
	if (commit.breaking) return 'breaking'
	if (commit.type === 'feat') return 'additive'
	if (commit.type === 'fix') return 'fixes'
	if (commit.type === 'docs') return 'docs'
	return 'other'
}

async function getCommits(
	repo: string,
	base: string,
	target: string,
): Promise<Commit[]> {
	// Format: sha|message
	const result =
		await $`cd ${repo} && git log --format="%H|%s" ${base}..${target}`.text()

	if (!result.trim()) {
		return []
	}

	const commits: Commit[] = []

	for (const line of result.trim().split('\n')) {
		const [sha, ...messageParts] = line.split('|')
		const message = messageParts.join('|') // Handle | in commit messages

		// Get full commit body for breaking change detection
		const body = await $`cd ${repo} && git log --format="%b" -1 ${sha}`.text()

		const parsed = parseConventionalCommit(message)

		commits.push({
			sha,
			shortSha: sha.slice(0, 7),
			message,
			type: parsed.type,
			scope: parsed.scope,
			breaking:
				parsed.breaking || body.toLowerCase().includes('breaking change'),
			body: body.trim() || undefined,
		})
	}

	return commits
}

async function getFileChanges(
	repo: string,
	base: string,
	target: string,
): Promise<FileChange[]> {
	// Format: status additions deletions path
	const result =
		await $`cd ${repo} && git diff --numstat --diff-filter=ADMRC ${base}..${target}`.text()

	if (!result.trim()) {
		return []
	}

	const changes: FileChange[] = []

	for (const line of result.trim().split('\n')) {
		const [additions, deletions, path] = line.split('\t')

		// Handle binary files (show as -)
		const add = additions === '-' ? 0 : Number.parseInt(additions, 10)
		const del = deletions === '-' ? 0 : Number.parseInt(deletions, 10)

		// Get status
		const statusResult =
			await $`cd ${repo} && git diff --name-status ${base}..${target} -- ${path}`.text()
		const status = (statusResult.trim().split('\t')[0] || 'M') as
			| 'A'
			| 'M'
			| 'D'
			| 'R'
			| 'C'

		changes.push({
			path,
			additions: add,
			deletions: del,
			status,
		})
	}

	return changes
}

async function findRepoRoot(): Promise<string> {
	// Walk up from script location to find navigator repo root
	let dir = dirname(Bun.main)
	while (dir !== '/') {
		if (await Bun.file(join(dir, '.git/config')).exists()) {
			return dir
		}
		dir = dirname(dir)
	}
	throw new Error('Could not find navigator repo root')
}

async function ensureAgentBrowserRepo(repoPath: string): Promise<void> {
	const gitConfig = join(repoPath, '.git/config')

	if (await Bun.file(gitConfig).exists()) {
		// Repo exists, ensure upstream remote is configured
		const remotes = await $`cd ${repoPath} && git remote -v`.text()
		if (!remotes.includes('upstream')) {
			console.error('Adding upstream remote...')
			await $`cd ${repoPath} && git remote add upstream ${UPSTREAM_URL}`
		}
		return
	}

	// Clone the fork
	console.error(`Cloning agent-browser fork to ${repoPath}...`)
	await $`git clone ${FORK_URL} ${repoPath}`

	// Add upstream remote
	console.error('Adding upstream remote...')
	await $`cd ${repoPath} && git remote add upstream ${UPSTREAM_URL}`

	console.error('Done.\n')
}

async function main() {
	const { values } = parseArgs({
		args: Bun.argv.slice(2),
		options: {
			repo: { type: 'string' },
			base: { type: 'string', default: 'origin/main' },
			target: { type: 'string', default: 'upstream/main' },
			format: { type: 'string', default: 'json' },
			help: { type: 'boolean', short: 'h' },
		},
	})

	if (values.help) {
		console.log(`
Usage: bun run analyze-upstream.ts [options]

Options:
  --repo <path>     Path to agent-browser repo (default: .agent-browser/repo/ in navigator root)
  --base <ref>      Base ref (default: origin/main)
  --target <ref>    Target ref (default: upstream/main)
  --format <fmt>    Output format: json, summary (default: json)
  -h, --help        Show this help

Environment:
  AGENT_BROWSER_LOCAL   Override default repo path
`)
		process.exit(0)
	}

	// Determine repo path: explicit > env var > .agent-browser/repo/
	let repo: string
	if (values.repo) {
		repo = values.repo
	} else if (process.env.AGENT_BROWSER_LOCAL) {
		repo = process.env.AGENT_BROWSER_LOCAL
	} else {
		const navigatorRoot = await findRepoRoot()
		repo = join(navigatorRoot, '.agent-browser', 'repo')
	}

	const base = values.base!
	const target = values.target!

	// Validate refs to prevent command injection
	if (!isValidGitRef(base)) {
		console.error(`Invalid base ref: ${base}`)
		process.exit(1)
	}
	if (!isValidGitRef(target)) {
		console.error(`Invalid target ref: ${target}`)
		process.exit(1)
	}

	// Ensure repo exists (clone if needed)
	await ensureAgentBrowserRepo(repo)

	// Fetch to ensure refs are up to date
	console.error('Fetching latest from origin and upstream...')
	await $`cd ${repo} && git fetch origin && git fetch upstream`.quiet()

	// Get commits and file changes
	const commits = await getCommits(repo, base, target)
	const fileChanges = await getFileChanges(repo, base, target)

	// Categorize commits
	const categorized: AnalysisResult['commits'] = {
		breaking: [],
		additive: [],
		fixes: [],
		docs: [],
		other: [],
	}

	for (const commit of commits) {
		const category = categorizeCommit(commit)
		categorized[category].push(commit)
	}

	// Identify critical file changes
	const criticalFiles = fileChanges.filter((f) =>
		CRITICAL_FILES.some((cf) => f.path.includes(cf)),
	)

	const result: AnalysisResult = {
		meta: {
			repo,
			base,
			target,
			analyzedAt: new Date().toISOString(),
		},
		summary: {
			totalCommits: commits.length,
			breaking: categorized.breaking.length,
			additive: categorized.additive.length,
			fixes: categorized.fixes.length,
			docs: categorized.docs.length,
			other: categorized.other.length,
		},
		commits: categorized,
		files: {
			critical: criticalFiles,
			all: fileChanges,
		},
	}

	if (values.format === 'summary') {
		console.log(`\n## Upstream Analysis: ${base} → ${target}\n`)
		console.log(`| Category | Count |`)
		console.log(`|----------|-------|`)
		console.log(`| Total | ${result.summary.totalCommits} |`)
		console.log(`| Breaking | ${result.summary.breaking} |`)
		console.log(`| Additive | ${result.summary.additive} |`)
		console.log(`| Fixes | ${result.summary.fixes} |`)
		console.log(`| Docs | ${result.summary.docs} |`)
		console.log(`| Other | ${result.summary.other} |`)

		if (categorized.breaking.length > 0) {
			console.log(`\n### Breaking Changes\n`)
			for (const c of categorized.breaking) {
				console.log(`- \`${c.shortSha}\` ${c.message}`)
			}
		}

		if (categorized.additive.length > 0) {
			console.log(`\n### New Features\n`)
			for (const c of categorized.additive) {
				console.log(`- \`${c.shortSha}\` ${c.message}`)
			}
		}

		if (criticalFiles.length > 0) {
			console.log(`\n### Critical File Changes\n`)
			for (const f of criticalFiles) {
				console.log(`- \`${f.path}\` (+${f.additions}/-${f.deletions})`)
			}
		}
	} else {
		console.log(JSON.stringify(result, null, 2))
	}
}

main().catch((err) => {
	console.error('Error:', err.message)
	process.exit(1)
})

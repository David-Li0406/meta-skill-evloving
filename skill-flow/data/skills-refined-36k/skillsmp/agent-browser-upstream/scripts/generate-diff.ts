#!/usr/bin/env bun
/**
 * Generate structured diff artifacts for agent consumption.
 *
 * Usage:
 *   bun run generate-diff.ts [--refresh]
 *
 * Outputs to .agent-browser/analysis/<sha>/:
 *   - summary.json         Small overview (load first)
 *   - release-notes.md     GitHub release notes if available
 *   - commits.json         All commits with metadata
 *   - by-category/         Commits split by type
 *   - diffs/               Individual file diffs
 *   - navigator-impact.json  Navigator files using changed APIs
 *
 * The SHA-based directory allows comparing multiple upstream versions.
 */

import { basename, dirname, join } from 'path'
import { parseArgs } from 'util'
import { $, Glob } from 'bun'
import { mkdir, rm } from 'fs/promises'

const FORK_URL = 'git@github.com:outfitter-dev/agent-browser.git'
const UPSTREAM_URL = 'git@github.com:vercel-labs/agent-browser.git'
const UPSTREAM_OWNER = 'vercel-labs'
const UPSTREAM_REPO = 'agent-browser'

// Files to generate individual diffs for
const DIFF_FILES = [
	'src/protocol.ts',
	'src/browser.ts',
	'src/index.ts',
	'src/types.ts',
	'src/snapshot.ts',
	'src/daemon.ts',
]

interface Commit {
	sha: string
	shortSha: string
	message: string
	type: string
	scope?: string
	breaking: boolean
	body?: string
	files: string[]
	url: string
}

interface Summary {
	generated: string
	upToDate: boolean
	versions: {
		fork: string
		forkSha: string
		upstream: string
		upstreamSha: string
	}
	counts: {
		total: number
		breaking: number
		features: number
		fixes: number
		other: number
	}
	hasReleaseNotes: boolean
	criticalFilesChanged: string[]
	navigatorFilesAffected: number
}

interface NavigatorImpact {
	file: string
	imports: string[]
	usages: string[]
}

// Parse conventional commit message
function parseConventionalCommit(message: string): {
	type: string
	scope?: string
	breaking: boolean
	description: string
} {
	const match = message.match(/^(\w+)(?:\(([^)]+)\))?(!)?\s*:\s*(.+?)(?:\n|$)/)

	if (!match) {
		return {
			type: 'unknown',
			breaking: message.toLowerCase().includes('breaking'),
			description: message.split('\n')[0],
		}
	}

	const [, rawType, scope, bang, description] = match
	const type = rawType.toLowerCase()
	const validTypes = [
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

// Find navigator repo root
async function findRepoRoot(): Promise<string> {
	let dir = dirname(Bun.main)
	while (dir !== '/') {
		if (await Bun.file(join(dir, '.git/config')).exists()) {
			return dir
		}
		dir = dirname(dir)
	}
	throw new Error('Could not find navigator repo root')
}

// Ensure agent-browser repo is cloned and configured
async function ensureAgentBrowserRepo(repoPath: string): Promise<void> {
	const gitConfig = join(repoPath, '.git/config')

	if (await Bun.file(gitConfig).exists()) {
		const remotes = await $`cd ${repoPath} && git remote -v`.text()
		if (!remotes.includes('upstream')) {
			console.error('Adding upstream remote...')
			await $`cd ${repoPath} && git remote add upstream ${UPSTREAM_URL}`
		}
		return
	}

	console.error(`Cloning agent-browser fork to ${repoPath}...`)
	await $`git clone ${FORK_URL} ${repoPath}`
	console.error('Adding upstream remote...')
	await $`cd ${repoPath} && git remote add upstream ${UPSTREAM_URL}`
	console.error('Done.\n')
}

// Get version/tag for a ref
async function getVersion(repo: string, ref: string): Promise<string> {
	try {
		const tag =
			await $`cd ${repo} && git describe --tags ${ref} 2>/dev/null`.text()
		return tag.trim()
	} catch {
		const sha = await $`cd ${repo} && git rev-parse --short ${ref}`.text()
		return sha.trim()
	}
}

// Get full SHA for a ref
async function getSha(repo: string, ref: string): Promise<string> {
	const sha = await $`cd ${repo} && git rev-parse ${ref}`.text()
	return sha.trim()
}

// Get commits between two refs
async function getCommits(
	repo: string,
	base: string,
	target: string,
): Promise<Commit[]> {
	const result =
		await $`cd ${repo} && git log --format="%H|%s" ${base}..${target}`.text()

	if (!result.trim()) return []

	const commits: Commit[] = []

	for (const line of result.trim().split('\n')) {
		const [sha, ...messageParts] = line.split('|')
		const message = messageParts.join('|')

		const body = await $`cd ${repo} && git log --format="%b" -1 ${sha}`.text()
		const filesRaw =
			await $`cd ${repo} && git diff-tree --no-commit-id --name-only -r ${sha}`.text()
		const files = filesRaw.trim().split('\n').filter(Boolean)

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
			files,
			url: `https://github.com/${UPSTREAM_OWNER}/${UPSTREAM_REPO}/commit/${sha}`,
		})
	}

	return commits
}

// Fetch GitHub release notes
async function fetchReleaseNotes(version: string): Promise<string | null> {
	try {
		// Try exact tag first, then with 'v' prefix
		const tags = [version, `v${version}`, version.replace(/^v/, '')]

		for (const tag of tags) {
			try {
				const response = await fetch(
					`https://api.github.com/repos/${UPSTREAM_OWNER}/${UPSTREAM_REPO}/releases/tags/${tag}`,
					{
						headers: {
							Accept: 'application/vnd.github.v3+json',
							'User-Agent': 'navigator-agent-browser-sync',
						},
					},
				)

				if (response.ok) {
					const data = await response.json()
					return data.body || null
				}
			} catch {
				continue
			}
		}

		// Try latest release
		const latestResponse = await fetch(
			`https://api.github.com/repos/${UPSTREAM_OWNER}/${UPSTREAM_REPO}/releases/latest`,
			{
				headers: {
					Accept: 'application/vnd.github.v3+json',
					'User-Agent': 'navigator-agent-browser-sync',
				},
			},
		)

		if (latestResponse.ok) {
			const data = await latestResponse.json()
			return `# ${data.tag_name}\n\n${data.body || 'No release notes.'}`
		}

		return null
	} catch {
		return null
	}
}

// Generate diff for a specific file
async function getFileDiff(
	repo: string,
	base: string,
	target: string,
	filePath: string,
): Promise<string | null> {
	try {
		const diff =
			await $`cd ${repo} && git diff ${base}..${target} -- ${filePath}`.text()
		return diff.trim() || null
	} catch {
		return null
	}
}

// Find navigator files that import from agent-browser
async function findNavigatorImpact(
	navigatorRoot: string,
): Promise<NavigatorImpact[]> {
	const impacts: NavigatorImpact[] = []

	// Use Bun's Glob API to find TypeScript files (shell globs don't expand in Bun's $)
	const glob = new Glob('packages/*/src/**/*.ts')

	for await (const relativePath of glob.scan({
		cwd: navigatorRoot,
		absolute: false,
	})) {
		const filePath = join(navigatorRoot, relativePath)
		const content = await Bun.file(filePath).text()

		// Skip files that don't import from agent-browser
		if (!content.includes('@outfitter/agent-browser')) {
			continue
		}

		// Extract import statements
		const importMatches = content.matchAll(
			/import\s+\{([^}]+)\}\s+from\s+['"]@outfitter\/agent-browser['"]/g,
		)
		const imports: string[] = []
		for (const match of importMatches) {
			imports.push(
				...match[1]
					.split(',')
					.map((s) => s.trim())
					.filter(Boolean),
			)
		}

		// Find usage patterns (simplified)
		const usages: string[] = []
		if (content.includes('BrowserManager')) usages.push('BrowserManager')
		if (content.includes('protocol')) usages.push('protocol')
		if (content.includes('snapshot')) usages.push('snapshot')

		if (imports.length > 0 || usages.length > 0) {
			impacts.push({
				file: relativePath,
				imports,
				usages,
			})
		}
	}

	return impacts
}

// Main
async function main() {
	const { values } = parseArgs({
		args: Bun.argv.slice(2),
		options: {
			refresh: { type: 'boolean', default: false },
			help: { type: 'boolean', short: 'h' },
		},
	})

	if (values.help) {
		console.log(`
Usage: bun run generate-diff.ts [options]

Options:
  --refresh    Force refresh (re-fetch from upstream)
  -h, --help   Show this help

Outputs to .agent-browser/analysis/<sha>/
`)
		process.exit(0)
	}

	const navigatorRoot = await findRepoRoot()
	const agentBrowserRoot = join(navigatorRoot, '.agent-browser')
	const agentBrowserPath =
		process.env.AGENT_BROWSER_LOCAL || join(agentBrowserRoot, 'repo')

	// Ensure repo exists
	await ensureAgentBrowserRepo(agentBrowserPath)

	// Fetch latest
	console.error('Fetching latest from origin and upstream...')
	await $`cd ${agentBrowserPath} && git fetch origin && git fetch upstream`.quiet()

	// Get versions
	const forkVersion = await getVersion(agentBrowserPath, 'origin/main')
	const forkSha = await getSha(agentBrowserPath, 'origin/main')
	const upstreamVersion = await getVersion(agentBrowserPath, 'upstream/main')
	const upstreamSha = await getSha(agentBrowserPath, 'upstream/main')

	// Output directory uses upstream SHA for versioning
	const shortSha = upstreamSha.slice(0, 7)
	const outputDir = join(agentBrowserRoot, 'analysis', shortSha)

	// Get commits
	const commits = await getCommits(
		agentBrowserPath,
		'origin/main',
		'upstream/main',
	)

	// Check if up to date
	if (commits.length === 0) {
		console.log(
			JSON.stringify({
				upToDate: true,
				message: 'Fork is up to date with upstream',
			}),
		)
		return
	}

	// Categorize commits
	const breaking = commits.filter((c) => c.breaking)
	const features = commits.filter((c) => c.type === 'feat' && !c.breaking)
	const fixes = commits.filter((c) => c.type === 'fix')
	const other = commits.filter(
		(c) => !c.breaking && c.type !== 'feat' && c.type !== 'fix',
	)

	// Find critical files changed
	const allFilesChanged = new Set<string>()
	for (const c of commits) {
		for (const f of c.files) {
			allFilesChanged.add(f)
		}
	}
	const criticalFilesChanged = DIFF_FILES.filter((f) => allFilesChanged.has(f))

	// Prepare output directory
	await rm(outputDir, { recursive: true, force: true })
	await mkdir(outputDir, { recursive: true })
	await mkdir(join(outputDir, 'by-category'), { recursive: true })
	await mkdir(join(outputDir, 'diffs'), { recursive: true })

	// Fetch release notes
	console.error('Fetching release notes...')
	const releaseNotes = await fetchReleaseNotes(upstreamVersion)
	const hasReleaseNotes = !!releaseNotes

	if (releaseNotes) {
		await Bun.write(join(outputDir, 'release-notes.md'), releaseNotes)
	}

	// Find navigator impact
	console.error('Analyzing navigator impact...')
	const navigatorImpact = await findNavigatorImpact(navigatorRoot)
	await Bun.write(
		join(outputDir, 'navigator-impact.json'),
		JSON.stringify(navigatorImpact, null, 2),
	)

	// Generate summary
	const summary: Summary = {
		generated: new Date().toISOString(),
		upToDate: false,
		versions: {
			fork: forkVersion,
			forkSha: forkSha.slice(0, 7),
			upstream: upstreamVersion,
			upstreamSha: upstreamSha.slice(0, 7),
		},
		counts: {
			total: commits.length,
			breaking: breaking.length,
			features: features.length,
			fixes: fixes.length,
			other: other.length,
		},
		hasReleaseNotes,
		criticalFilesChanged,
		navigatorFilesAffected: navigatorImpact.length,
	}
	await Bun.write(
		join(outputDir, 'summary.json'),
		JSON.stringify(summary, null, 2),
	)

	// Write all commits
	await Bun.write(
		join(outputDir, 'commits.json'),
		JSON.stringify(commits, null, 2),
	)

	// Write by category
	await Bun.write(
		join(outputDir, 'by-category/breaking.json'),
		JSON.stringify(breaking, null, 2),
	)
	await Bun.write(
		join(outputDir, 'by-category/features.json'),
		JSON.stringify(features, null, 2),
	)
	await Bun.write(
		join(outputDir, 'by-category/fixes.json'),
		JSON.stringify(fixes, null, 2),
	)
	await Bun.write(
		join(outputDir, 'by-category/other.json'),
		JSON.stringify(other, null, 2),
	)

	// Generate individual file diffs
	console.error('Generating file diffs...')
	for (const file of DIFF_FILES) {
		const diff = await getFileDiff(
			agentBrowserPath,
			'origin/main',
			'upstream/main',
			file,
		)
		if (diff) {
			const filename = basename(file) + '.diff'
			await Bun.write(join(outputDir, 'diffs', filename), diff)
		}
	}

	// Output summary to console
	console.log(`
## Diff Artifacts Generated

**Output:** \`.agent-browser/analysis/${shortSha}/\`

| Metric | Value |
|--------|-------|
| Fork | ${forkVersion} (\`${summary.versions.forkSha}\`) |
| Upstream | ${upstreamVersion} (\`${summary.versions.upstreamSha}\`) |
| Total commits | ${summary.counts.total} |
| Breaking | ${summary.counts.breaking} |
| Features | ${summary.counts.features} |
| Fixes | ${summary.counts.fixes} |
| Release notes | ${hasReleaseNotes ? 'Yes' : 'No'} |
| Critical files changed | ${criticalFilesChanged.length} |
| Navigator files affected | ${navigatorImpact.length} |

### Files Generated

\`\`\`
.agent-browser/analysis/${shortSha}/
├── summary.json              # Start here
├── release-notes.md          ${hasReleaseNotes ? '# Available' : '# Not available'}
├── commits.json              # ${commits.length} commits
├── navigator-impact.json     # ${navigatorImpact.length} files
├── by-category/
│   ├── breaking.json         # ${breaking.length} commits
│   ├── features.json         # ${features.length} commits
│   ├── fixes.json            # ${fixes.length} commits
│   └── other.json            # ${other.length} commits
└── diffs/
${criticalFilesChanged.map((f) => `    ├── ${basename(f)}.diff`).join('\n') || '    └── (no critical file changes)'}
\`\`\`

### Next Steps

1. Read \`summary.json\` to understand scope
2. If breaking > 0, review \`by-category/breaking.json\`
3. Check \`navigator-impact.json\` for affected files
4. Use \`/agent-browser:check\` for full analysis
`)
}

main().catch((err) => {
	console.error('Error:', err.message)
	process.exit(1)
})

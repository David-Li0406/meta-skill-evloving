import { mkdir, writeFile } from 'node:fs/promises'
import { join } from 'node:path'

async function initSkill() {
    const skillName = process.argv[2]
    if (!skillName) {
        console.error('Usage: bun init_skill.ts <skill-name>')
        process.exit(1)
    }

    const rootDir = join(process.cwd(), '.skills', skillName)
    const dirs = ['scripts', 'references', 'assets']

    console.log(`🚀 Initializing skill: ${skillName}...`)

    try {
        // Create directories
        await mkdir(rootDir, { recursive: true })
        for (const dir of dirs) {
            await mkdir(join(rootDir, dir), { recursive: true })
        }

        // Create SKILL.md template
        const skillMdContent = `---
name: ${skillName}
description: Describe what this skill does and when an agent should use it.
---

# ${skillName
                .split('-')
                .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
                .join(' ')}

Add your skill instructions and workflow here.

## Resources
- **Scripts**: [List any scripts in ./scripts/]
- **References**: [List any references in ./references/]
- **Assets**: [List any assets in ./assets/]
`

        await writeFile(join(rootDir, 'SKILL.md'), skillMdContent)

        // Create placeholder files
        await writeFile(join(rootDir, 'scripts', '.keep'), '')
        await writeFile(join(rootDir, 'references', '.keep'), '')
        await writeFile(join(rootDir, 'assets', '.keep'), '')

        console.log(`✅ Skill "${skillName}" initialized at ${rootDir}`)
    } catch (error) {
        console.error('❌ Failed to initialize skill:', error)
        process.exit(1)
    }
}

initSkill()

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// --- Configuration ---
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// We assume this script is located at: .gemini/antigravity/skills/ai-tools/claude-skill-importer/scripts/importer.js
// So the repo root is 5 levels up.
const REPO_ROOT = path.resolve(__dirname, '../../../../../../');
const AGENT_SKILLS_ROOT = path.resolve(REPO_ROOT, '.gemini/antigravity/skills');

// Default target category if not specified
const DEFAULT_CATEGORY = 'imported-skills';

function log(msg) { console.log(`[ClaudeImporter] ${msg}`); }
function error(msg) { console.error(`[ClaudeImporter] ❌ ${msg}`); }

// --- Helpers ---

function ensureDir(dir) {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function parseFrontmatter(content) {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return null;
    const frontmatter = {};
    const lines = match[1].split('\n');
    for (const line of lines) {
        const [key, ...rest] = line.split(':');
        if (key && rest.length) {
            frontmatter[key.trim()] = rest.join(':').trim();
        }
    }
    return frontmatter;
}

function createMetadataJson(dir, skillName, description) {
    const metadataPath = path.join(dir, 'metadata.json');
    if (fs.existsSync(metadataPath)) return;

    const metadata = {
        name: skillName,
        description: description,
        version: "1.0.0",
        files: ["SKILL.md", "SKILL.ja.md"]
    };
    fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));
    log(`Created metadata.json for ${skillName}`);
}

function createJaPlaceholder(dir, skillName, description, originalContent) {
    const jaPath = path.join(dir, 'SKILL.ja.md');
    if (fs.existsSync(jaPath)) return;

    // Strip frontmatter from original for the body
    const body = originalContent.replace(/^---\n[\s\S]*?\n---\n/, '');
    
    const content = [
        '---',
        `name: ${skillName} (JP)`,
        `description: ${description} (JP)`,
        'language: ja',
        '---',
        '',
        '> **Note**: This is a placeholder for the Japanese translation.',
        '> **注記**: これは日本語訳のプレースホルダーです。',
        '',
        body
    ].join('\n');

    fs.writeFileSync(jaPath, content);
    log(`Created SKILL.ja.md for ${skillName}`);
}

function normalizeSkill(dir, fileName = 'SKILL.md') {
    const filePath = path.join(dir, fileName);
    if (!fs.existsSync(filePath)) return;

    let content = fs.readFileSync(filePath, 'utf-8');
    let frontmatter = parseFrontmatter(content);
    const folderName = path.basename(dir);
    
    let name = frontmatter?.name || folderName;
    let description = frontmatter?.description;

    // 1. Ensure Frontmatter
    if (!frontmatter) {
        // Try to infer description from first lines
        if (!description) {
            const lines = content.split('\n');
             for (const line of lines) {
                if (line.trim().length > 0 && !line.startsWith('#') && !line.startsWith('!')) {
                    description = line.trim().substring(0, 150).replace(/:/g, '') + '...';
                    break;
                }
            }
            description = description || `Imported skill: ${name}`;
        }

        const newFrontmatter = [
            '---',
            `name: ${name}`,
            `description: ${description}`,
            '---',
            '',
            ''
        ].join('\n');
        
        content = newFrontmatter + content;
        fs.writeFileSync(filePath, content);
        log(`Added frontmatter to ${name}`);
    } else {
        // If description was missing in parsed frontmatter (unlikely if valid yaml)
        description = description || `Sort of ${name}`;
    }

    // 2. Metadata & Translations
    createMetadataJson(dir, name, description);
    createJaPlaceholder(dir, name, description, content);
}

function copyRecursive(src, dest) {
    ensureDir(dest);
    for (const child of fs.readdirSync(src)) {
        const srcChild = path.join(src, child);
        const destChild = path.join(dest, child);
        if (fs.statSync(srcChild).isDirectory()) {
            copyRecursive(srcChild, destChild);
        } else {
            fs.copyFileSync(srcChild, destChild);
        }
    }
}

// --- Main Logic ---

async function main() {
    const sourcePath = process.argv[2];
    const categoryName = process.argv[3] || DEFAULT_CATEGORY;

    if (!sourcePath) {
        error("Usage: node importer.js <source_directory> [target_category_name]");
        process.exit(1);
    }

    if (!fs.existsSync(sourcePath)) {
        error(`Source directory not found: ${sourcePath}`);
        process.exit(1);
    }

    const targetBase = path.join(AGENT_SKILLS_ROOT, categoryName);
    ensureDir(targetBase);
    
    log(`Importing from: ${sourcePath}`);
    log(`Target: ${targetBase}`);

    let count = 0;
    const sourceStat = fs.statSync(sourcePath);

    // Strategy 1: Source is a direct folder of .md files (Simple Claude Code style)
    if (sourceStat.isDirectory()) {
        const items = fs.readdirSync(sourcePath);
        
        // Check if there are plugins (Trail of Bits style / plugins folder)
        if (items.includes('plugins') && fs.statSync(path.join(sourcePath, 'plugins')).isDirectory()) {
            log("Detected 'plugins' directory. Using nested plugin import strategy.");
            const pluginsDir = path.join(sourcePath, 'plugins');
            const pluginFolders = fs.readdirSync(pluginsDir);
            
            for (const p of pluginFolders) {
                if (p.startsWith('.')) continue;
                const pDir = path.join(pluginsDir, p);
                const skillsDir = path.join(pDir, 'skills'); // Check for 'skills' subfolder
                
                if (fs.existsSync(skillsDir)) {
                     const skills = fs.readdirSync(skillsDir);
                     for (const s of skills) {
                         const sDir = path.join(skillsDir, s);
                         const sDest = path.join(targetBase, s);
                         copyRecursive(sDir, sDest);
                         normalizeSkill(sDest, 'SKILL.md');
                         count++;
                     }
                }
            }
        } 
        // Strategy 2: Flat list of MD files
        else {
             for (const item of items) {
                const fullPath = path.join(sourcePath, item);
                if (item.endsWith('.md') && !fs.statSync(fullPath).isDirectory()) {
                    // It's a skill file like "my-skill.md"
                    const skillName = path.basename(item, '.md').toLowerCase().replace(/\s+/g, '-');
                    const destDir = path.join(targetBase, skillName);
                    ensureDir(destDir);
                    fs.copyFileSync(fullPath, path.join(destDir, 'SKILL.md'));
                    normalizeSkill(destDir, 'SKILL.md');
                    count++;
                } else if (fs.statSync(fullPath).isDirectory()) {
                    // Check if it's a skill directory (contains SKILL.md or similar)
                    if (fs.existsSync(path.join(fullPath, 'SKILL.md'))) {
                         const destDir = path.join(targetBase, item);
                         copyRecursive(fullPath, destDir);
                         normalizeSkill(destDir, 'SKILL.md');
                         count++;
                    }
                }
            }
        }
    }

    log(`✅ Successfully imported/normalized ${count} skills into ${categoryName}`);
}

main();

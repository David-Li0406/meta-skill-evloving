#!/usr/bin/env node

/**
 * Quick validation script for skills - minimal version
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml'); // Assuming js-yaml might not be available, we'll try to parse manually or warn usage.
// Note: Since this is a standalone script in a skill, we should try to avoid external deps if possible,
// OR assume the environment has them. 
// Given the environment likelihood, let's implement a very basic YAML parser for frontmatter 
// or assume we can require 'js-yaml' if available, otherwise strict regex.
// The Python script used `yaml` library. 
// For robustness without deps, regex is often enough for simple frontmatter.

function parseFrontmatter(content) {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return null;
    
    const frontmatterRaw = match[1];
    const frontmatter = {};
    
    // Very basic YAML parsing for top-level keys
    const lines = frontmatterRaw.split('\n');
    let currentKey = null;

    for (const line of lines) {
        if (!line.trim() || line.trim().startsWith('#')) continue;

        const keyMatch = line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
        if (keyMatch) {
            const key = keyMatch[1].trim();
            const value = keyMatch[2].trim();
            frontmatter[key] = value;
            currentKey = key;
        } else if (currentKey) {
            // Multiline string continuation (very basic support)
            frontmatter[currentKey] += ' ' + line.trim();
        }
    }
    
    return frontmatter;
}

function validateSkill(skillPath) {
    const resolvedPath = path.resolve(skillPath);

    // Check SKILL.md exists
    const skillMdPath = path.join(resolvedPath, 'SKILL.md');
    if (!fs.existsSync(skillMdPath)) {
        return { valid: false, message: "SKILL.md not found" };
    }

    // Read and validate frontmatter
    const content = fs.readFileSync(skillMdPath, 'utf8');
    if (!content.startsWith('---')) {
        return { valid: false, message: "No YAML frontmatter found (must start with ---)" };
    }

    const frontmatter = parseFrontmatter(content);
    if (!frontmatter) {
        return { valid: false, message: "Invalid frontmatter format" };
    }

    // Define allowed properties
    const ALLOWED_PROPERTIES = new Set(['name', 'description', 'license', 'allowed-tools', 'metadata']);

    // Check for unexpected properties
    const keys = Object.keys(frontmatter);
    const unexpectedKeys = keys.filter(k => !ALLOWED_PROPERTIES.has(k));
    if (unexpectedKeys.length > 0) {
        return { 
            valid: false, 
            message: `Unexpected key(s) in SKILL.md frontmatter: ${unexpectedKeys.join(', ')}. Allowed properties are: ${Array.from(ALLOWED_PROPERTIES).join(', ')}` 
        };
    }

    // Check required fields
    if (!frontmatter.name) {
        return { valid: false, message: "Missing 'name' in frontmatter" };
    }
    if (!frontmatter.description) {
        return { valid: false, message: "Missing 'description' in frontmatter" };
    }

    // Validate name
    const name = frontmatter.name.trim();
    if (name) {
         // Check naming convention (hyphen-case: lowercase with hyphens)
         if (!/^[a-z0-9-]+$/.test(name)) {
            return { valid: false, message: `Name '${name}' should be hyphen-case (lowercase letters, digits, and hyphens only)` };
         }
         if (name.startsWith('-') || name.endsWith('-') || name.includes('--')) {
            return { valid: false, message: `Name '${name}' cannot start/end with hyphen or contain consecutive hyphens` };
         }
         if (name.length > 64) {
            return { valid: false, message: `Name is too long (${name.length} characters). Maximum is 64 characters.` };
         }
    }

    // Validate description
    const description = frontmatter.description.trim();
    if (description) {
        if (description.includes('<') || description.includes('>')) {
            return { valid: false, message: "Description cannot contain angle brackets (< or >)" };
        }
        if (description.length > 1024) {
            return { valid: false, message: `Description is too long (${description.length} characters). Maximum is 1024 characters.` };
        }
    }

    return { valid: true, message: "Skill is valid!" };
}

function main() {
    if (process.argv.length !== 3) {
        console.log("Usage: node quick_validate.js <skill_directory>");
        process.exit(1);
    }

    const { valid, message } = validateSkill(process.argv[2]);
    console.log(message);
    process.exit(valid ? 0 : 1);
}

// Export for usage in package_skill.js
module.exports = { validateSkill };

if (require.main === module) {
    main();
}

#!/usr/bin/env node

/**
 * Skill Packager - Creates a distributable .skill file of a skill folder
 * 
 * Usage:
 *     node package_skill.js <path/to/skill-folder> [output-directory]
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { validateSkill } = require('./quick_validate');

function packageSkill(skillPathRaw, outputDir) {
    const skillPath = path.resolve(skillPathRaw);

    // Validate skill folder exists
    if (!fs.existsSync(skillPath)) {
        console.error(`❌ Error: Skill folder not found: ${skillPath}`);
        return null;
    }

    if (!fs.statSync(skillPath).isDirectory()) {
        console.error(`❌ Error: Path is not a directory: ${skillPath}`);
        return null;
    }

    // Validate SKILL.md exists
    const skillMd = path.join(skillPath, "SKILL.md");
    if (!fs.existsSync(skillMd)) {
        console.error(`❌ Error: SKILL.md not found in ${skillPath}`);
        return null;
    }

    // Run validation before packaging
    console.log("🔍 Validating skill...");
    const { valid, message } = validateSkill(skillPath);
    if (!valid) {
        console.error(`❌ Validation failed: ${message}`);
        console.error("   Please fix the validation errors before packaging.");
        return null;
    }
    console.log(`✅ ${message}\n`);

    // Determine output location
    const skillName = path.basename(skillPath);
    let outputPath;
    if (outputDir) {
        outputPath = path.resolve(outputDir);
        fs.mkdirSync(outputPath, { recursive: true });
    } else {
        outputPath = process.cwd();
    }

    const skillFilename = path.join(outputPath, `${skillName}.skill`);

    // Create the .skill file (using system zip command for reliability and no-deps)
    try {
        // Remove existing file if it exists
        if (fs.existsSync(skillFilename)) {
            fs.unlinkSync(skillFilename);
        }
        
        // We use 'zip' command which is available on standard Mac/Linux/Unix
        // -r: recursive
        // -j: junk paths (do not use, we want relative structure)
        // Check if zip is available
        try {
            execSync('zip --version', { stdio: 'ignore' });
        } catch (e) {
            console.error("❌ Error: 'zip' command not found. Please install zip.");
            return null;
        }

        console.log(`📦 Zipping contents of ${skillPath} to ${skillFilename}...`);
        
        // Use cwd as the parent of skill directory so that the zip root is the skill folder itself? 
        // Actually, standard conventions for these skills usually expect the structure INSIDE the zip
        // to match the folder structure (e.g., skill-name/SKILL.md).
        // The python script used:
        // arcname = file_path.relative_to(skill_path.parent)
        // So yes, it includes the skill-name folder.
        
        const parentDir = path.dirname(skillPath);
        const folderName = path.basename(skillPath);
        
        // Command: zip -r <absolute_path_to_dest> <folder_name>
        execSync(`zip -r "${skillFilename}" "${folderName}"`, { 
            cwd: parentDir,
            stdio: 'inherit' 
        });

        console.log(`\n✅ Successfully packaged skill to: ${skillFilename}`);
        return skillFilename;

    } catch (e) {
        console.error(`❌ Error creating .skill file: ${e.message}`);
        return null;
    }
}

function main() {
    const args = process.argv.slice(2);
    if (args.length < 1) {
        console.log("Usage: node package_skill.js <path/to/skill-folder> [output-directory]");
        console.log("\nExample:");
        console.log("  node package_skill.js skills/public/my-skill");
        console.log("  node package_skill.js skills/public/my-skill ./dist");
        process.exit(1);
    }

    const skillPath = args[0];
    const outputDir = args.length > 1 ? args[1] : null;

    console.log(`📦 Packaging skill: ${skillPath}`);
    if (outputDir) {
        console.log(`   Output directory: ${outputDir}`);
    }
    console.log();

    const result = packageSkill(skillPath, outputDir);

    if (result) {
        process.exit(0);
    } else {
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

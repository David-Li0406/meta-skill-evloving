---
name: skill-importer
description: Import and synchronize skills from remote GitHub repositories. Use this skill when you need to copy skills from other repositories, maintain a list of remote skill sources, or update local skills with fresh copies from upstream sources.
---

# Skill Importer

## Overview

The Skill Importer maintains a list of skills from remote GitHub repositories that can be imported into the local `.github/skills/` directory. It uses a configuration file to track skill sources and provides both automated and manual import methods.

## Quick Start (Automated)

The easiest way to import skills is using the automated script located in the `scripts/` directory:

```bash
# Import all enabled skills
cd .github/skills/skill-importer
python3 scripts/import_skills.py --all

# Import a specific skill
python3 scripts/import_skills.py --skill sync-job-expert

# Update existing skills
python3 scripts/import_skills.py --all --update
```

See [scripts/import_skills.py](scripts/import_skills.py) for the implementation.

## Core Workflow

### 1. Managing Skill Sources

Skill sources are maintained in `assets/skill-sources.yaml`:

```yaml
skills:
  - name: skill-name
    url: https://github.com/owner/repo/tree/branch/.github/skills/skill-name
    enabled: true
    description: Brief description of the skill
```

**URL Format:**
- GitHub tree URLs: `https://github.com/owner/repo/tree/branch/path/to/skill`

### 2. Automated Importing (Recommended)

Use the `import_skills.py` script (located in `scripts/` directory) for automated imports:

```bash
python3 scripts/import_skills.py --all          # Import all enabled skills
python3 scripts/import_skills.py --skill NAME   # Import specific skill
python3 scripts/import_skills.py --all --update # Update existing skills
python3 scripts/import_skills.py --all --dry-run # Preview without importing
```

The script automates all the manual steps below (cloning, copying, cleanup, verification).

### 3. Manual Importing Skills

To import a skill from a remote repository, follow these steps:

#### Step 1: Clone the Source Repository

```bash
# Clone the repository containing the skill
cd /tmp
git clone --depth 1 --branch <branch> --single-branch https://github.com/<owner>/<repo>.git <temp_dir>
```

**Example:**
```bash
cd /tmp
git clone --depth 1 --branch custom --single-branch https://github.com/kehwar/frappe.git frappe_custom
```

#### Step 2: Copy the Skill to Local Directory

```bash
# Copy the skill directory to your local .github/skills/ directory
cp -r <temp_dir>/.github/skills/<skill-name> /path/to/your/repo/.github/skills/
```

**Example:**
```bash
cp -r /tmp/frappe_custom/.github/skills/doctype-schema-expert /home/runner/work/frappe_soldamundo/frappe_soldamundo/.github/skills/
```

#### Step 3: Clean Up Temporary Files

```bash
# Remove the temporary clone
rm -rf <temp_dir>
```

**Example:**
```bash
rm -rf /tmp/frappe_custom
```

#### Step 4: Verify the Import

```bash
# Check that the skill was copied correctly
ls -la /path/to/your/repo/.github/skills/<skill-name>/
```

### 4. Adding New Skill Sources

To add a new skill source:

1. Find the GitHub URL to the skill directory (tree view)
2. Add an entry to `assets/skill-sources.yaml`:

```yaml
skills:
  # ... existing skills ...
  - name: new-skill-name
    url: https://github.com/user/repo/tree/main/.github/skills/new-skill
    enabled: true
    description: What this skill does
```

3. Import the skill using the automated script:
   ```bash
   python3 scripts/import_skills.py --skill new-skill-name
   ```

### 5. Updating Skills

To update skills with the latest versions from remote sources:

**Using the automated script (recommended):**
```bash
python3 scripts/import_skills.py --skill <skill-name> --update  # Update one skill
python3 scripts/import_skills.py --all --update                 # Update all skills
```

**Manual method:**
1. Remove the existing local skill directory:
   ```bash
   rm -rf .github/skills/<skill-name>
   ```

2. Follow the manual import steps above to re-download the skill

## Important Notes

**Warning:** When updating, the local skill directory will be completely replaced. Any local modifications will be lost.

**Network Dependency:** Manual importing requires internet access to clone skills from GitHub.

## Use Cases

1. **Copying Skills Between Repositories**
   - Add skill sources from other projects
   - Import them into current repository
   - Keep them synchronized by re-importing when needed

2. **Maintaining Skill Libraries**
   - Track multiple upstream skill sources
   - Update skills manually when needed
   - Disable/enable specific skills as needed

3. **Distributing Common Skills**
   - Maintain canonical skill versions in one repository
   - Import them into multiple dependent repositories
   - Keep all copies in sync by re-importing

## Complete Example

Here's a complete example of importing the `doctype-schema-expert` skill:

```bash
# Step 1: Add to skill-sources.yaml
cat >> .github/skills/skill-importer/assets/skill-sources.yaml << 'EOF'
  - name: doctype-schema-expert
    url: https://github.com/kehwar/frappe/tree/custom/.github/skills/doctype-schema-expert
    enabled: true
    description: Expert skill for working with Frappe DocType schemas
EOF

# Step 2: Clone the source repository
cd /tmp
git clone --depth 1 --branch custom --single-branch https://github.com/kehwar/frappe.git frappe_custom

# Step 3: Copy the skill
cp -r /tmp/frappe_custom/.github/skills/doctype-schema-expert .github/skills/

# Step 4: Clean up
rm -rf /tmp/frappe_custom

# Step 5: Verify
ls -la .github/skills/doctype-schema-expert/
```

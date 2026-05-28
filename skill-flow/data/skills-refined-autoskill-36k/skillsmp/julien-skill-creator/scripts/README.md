# Scripts for Skill Creation

The Anthropic skills repository includes helper scripts for skill creation that work with skill-creator:

## Available Scripts

### 1. `init_skill.py` - Initialize New Skill

Generates a new skill template with proper structure.

**Location**: https://github.com/anthropics/skills/blob/main/scripts/init_skill.py

**Usage**:
```bash
# Clone Anthropic repo first
git clone https://github.com/anthropics/skills
cd skills

# Initialize a new skill
python scripts/init_skill.py <skill-name> --path <output-directory>

# Example: Create skill in your marketplace
python scripts/init_skill.py my-deployment-skill --path ../my-marketplace/skills/
```

**What it creates**:
- `SKILL.md` with proper frontmatter and TODO placeholders
- `scripts/` directory with example Python script
- `references/` directory with example reference file
- `assets/` directory for templates

### 2. `package_skill.py` - Validate and Package

Validates skill structure and creates distributable ZIP file.

**Location**: https://github.com/anthropics/skills/blob/main/scripts/package_skill.py

**Usage**:
```bash
# Package a skill
python scripts/package_skill.py <path/to/skill-folder>

# Example
python scripts/package_skill.py ../my-marketplace/skills/my-deployment-skill

# Optional: specify output directory
python scripts/package_skill.py <path/to/skill-folder> ./dist
```

**What it does**:
1. **Validates**:
   - YAML frontmatter format
   - Required fields (name, description)
   - Skill naming conventions
   - Directory structure
   - File organization

2. **Packages** (if validation passes):
   - Creates `<skill-name>.zip`
   - Includes all files
   - Maintains proper structure
   - Ready for distribution

## How to Get the Scripts

### Option 1: Clone Anthropic Repository
```bash
git clone https://github.com/anthropics/skills
# Scripts are in skills/scripts/
```

### Option 2: Download Directly
```bash
# Download init_skill.py
curl -o init_skill.py https://raw.githubusercontent.com/anthropics/skills/main/scripts/init_skill.py

# Download package_skill.py
curl -o package_skill.py https://raw.githubusercontent.com/anthropics/skills/main/scripts/package_skill.py
```

### Option 3: Copy to This Directory

You can copy the scripts here for convenience:
```bash
# From within anthropics/skills repo
cp scripts/init_skill.py ../my-marketplace/skills/skill-creator/scripts/
cp scripts/package_skill.py ../my-marketplace/skills/skill-creator/scripts/
```

## Recommended Workflow

1. **Clone Anthropic repo** (one time):
   ```bash
   git clone https://github.com/anthropics/skills ~/anthropic-skills
   ```

2. **Alias the scripts** for easy access:
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   alias skill-init="python ~/anthropic-skills/scripts/init_skill.py"
   alias skill-package="python ~/anthropic-skills/scripts/package_skill.py"
   ```

3. **Use from anywhere**:
   ```bash
   skill-init my-new-skill --path ./skills/
   # ... develop your skill ...
   skill-package ./skills/my-new-skill
   ```

## Integration with skill-creator

When using skill-creator, follow the complete workflow:

1. **Step 3**: Use `init_skill.py` to initialize
2. **Step 4**: Edit SKILL.md, add Skill Chaining section
3. **Step 5**: Use `package_skill.py` to validate & package
4. **Step 6**: Iterate based on quality rubric

The scripts work seamlessly with the enhanced Skill Chaining documentation format added in skill-creator.

## Notes

- Scripts are maintained by Anthropic in the official skills repository
- They may be updated over time (check the repo for latest version)
- Validation includes all standard skill requirements
- The Skill Chaining section added by skill-creator is optional from a validation perspective, but highly recommended for workflow skills

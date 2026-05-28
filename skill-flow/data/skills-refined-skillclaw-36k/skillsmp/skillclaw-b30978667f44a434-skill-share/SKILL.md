---
name: skill-share
description: Use this skill when you need to create new agent skills with proper structure and automatically share them on Slack for team collaboration and skill discovery.
---

# Skill body

## When to use this skill

Use this skill when you need to:
- **Create new agent skills** with proper structure and metadata
- **Generate skill packages** ready for distribution
- **Automatically share created skills** on Slack channels for team visibility
- **Validate skill structure** before sharing
- **Package and distribute** skills to your team

Also use this skill when:
- **User says they want to create/share their skill** 

This skill is ideal for:
- Creating skills as part of team workflows
- Building internal tools that need skill creation + team notification
- Automating the skill development pipeline
- Collaborative skill creation with team notifications

## Key Features

### 1. Skill Creation
- Creates properly structured skill directories with SKILL.md
- Generates standardized scripts/, references/, and assets/ directories
- Auto-generates YAML frontmatter with required metadata
- Enforces naming conventions (hyphen-case)

### 2. Skill Validation
- Validates SKILL.md format and required fields
- Checks naming conventions
- Ensures metadata completeness before packaging

### 3. Skill Packaging
- Creates distributable zip files
- Includes all skill assets and documentation
- Runs validation automatically before packaging

### 4. Slack Integration via Rube
- Automatically sends created skill information to designated Slack channels
- Shares skill metadata (name, description, link)
- Posts skill summary for team discovery
- Provides direct links to skill files

## How It Works

1. **Initialization**: Provide skill name and description
2. **Creation**: Skill directory is created with proper structure
3. **Validation**: Skill metadata is validated for correctness
4. **Packaging**: Skill is packaged into a distributable format
5. **Slack Notification**: Skill details are posted to your team's Slack channel

## Example Usage

```
When you ask Claude to create a skill called "pdf-analyzer":
1. Creates /skill-pdf-analyzer/ with SKILL.md template
2. Generates structured directories (scripts/, references/, assets/)
3. Validates the skill structure
4. Packages the skill as a zip file
5. Posts to Slack: "New Skill Created: pdf-analyzer - Advanced PDF analysis and extraction capabilities"
```
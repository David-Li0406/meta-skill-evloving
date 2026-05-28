---
name: git-workflow
description: Manage Git workflow for campaign content, including commit messages, branching, and creature article creation.
---

## What I do
- Generate descriptive commit messages following project conventions.
- Create appropriate branches for content development.
- Manage content publication workflow with proper staging.
- Generate changelogs for campaign updates.
- Coordinate multi-file commits with logical grouping.
- Handle content review and approval processes.
- Create detailed creature/monster articles for The Scarlet Wood TTRPG campaign hub, following Utopia TTRPG system rules for stats and abilities.

## When to use me
Use this when:
- Committing new campaign content or updates.
- Preparing content for publication.
- Managing collaborative development with multiple contributors.
- Creating release points for campaign milestones.
- Organizing content development workflow.
- Generating new creature stats articles based on user input descriptions.

## Usage Examples

### Content Publication Commit
```
/skill({ name: "git-workflow" })
Operation: Commit content
Files: <file_list>
Type: Feature (new content updates)
Message: Auto-generated based on content changes
```

### Branch Creation
```
/skill({ name: "git-workflow" })
Operation: Create development branch
Purpose: <branch_purpose>
Based on: <base_branch>
Duration: Temporary for content staging
```

### Release Preparation
```
/skill({ name: "git-workflow" })
Operation: Prepare release
Version: <release_version>
Changelog: Generate from commits since last release
Files: <file_list>
```

## Git Operations

### Commit Message Generation
1. Analyze changed files to determine content type.
2. Generate descriptive commit message following conventions.
3. Categorize changes (feat, fix, docs, style, refactor, test, chore).
4. Include relevant character names and session numbers.
5. Add context about campaign impact.

### Branch Management
1. Create feature branches for content development.
2. Merge branches after content review and approval.
3. Handle branch naming conventions consistently.
4. Manage branch lifecycle and cleanup.
5. Coordinate parallel development streams.

### Release Workflow
1. Prepare content for publication (remove draft status).
2. Generate changelog of changes since last release.
3. Create tagged release points for campaign milestones.
4. Handle versioning based on session numbers or content significance.
5. Coordinate GitHub Pages deployment.

## Creature Article Creation

### Purpose
Generate complete, campaign-ready creature articles with:
- Proper stat blocks using Utopia TTRPG mechanics.
- Lore and ecological information.
- Combat tactics and behavior.
- Proper Jekyll front matter and markdown formatting.
- Internal links following site conventions.

### Input Parameters
The skill accepts natural language descriptions containing:
- **Required Information**: Name, Basic concept, Size, Role.
- **Recommended Information**: Habitat, Behavior, Combat style, Special abilities, Appearance.
- **Optional Information**: Loot, Variants, Relationships, Campaign integration.

### Process
1. Gather information from user input.
2. Generate stats using Utopia TTRPG rules.
3. Design abilities and write lore.
4. Format document with Jekyll front matter and markdown structure.
5. Add appropriate internal references.

### Output Format
Generate a complete markdown file following this structure:
```markdown
---
layout: page
title: [Creature Name]
summary: [One-line description]
topic: Creatures
tags:
    - creature
    - [combat/exploration/social]
    - [enemy/neutral/ally]
    - [habitat type]

published: false # REMOVE WHEN LIVE
---

![Creature Token]({{ "/assets/images/[slug]_token.png" | relative_url }})
{: .character-token}

[2-3 sentence introduction]

## Overview
[Detailed description of creature's role, behavior, and place in world]

## Appearance
- **Species/Type:** [Type]
- **Size:** [Small/Medium/Large]
- **Physical Description:** [Visual details]
- **Notable Features:** [Distinguishing characteristics]

## Stat Block
### Basic Statistics
- **Constitution:** [number]
- **Endurance:** [number]
- **Effervescence:** [number]
- **Block Rating:** [dice]
- **Dodge Rating:** [dice]
- **Size:** [Size]
- **HP:** [value or formula]
- **Stamina:** [value or formula]

### Abilities
[Full ability and sub-ability score breakdown with modifiers]

### Attacks
[Attack entries with type, range, damage, special effects]

## Behavior and Tactics
[Combat behavior and strategy]

## Ecology and Habitat
[Where found, diet, social structure, activity patterns]

## Loot and Resources
[Harvestable materials]

## Links
- Back to [World]({{ "/world/" | relative_url }})
[Additional relevant links]
```

## Quality Checklist
Before finalizing, verify:
- Front matter complete and valid YAML.
- Title, summary, and topic set.
- Stats match selected body/kit(s)/class(es).
- All ability scores have modifiers.
- Attacks include type, range, damage.
- All internal links use `relative_url` filter.

## Notes for AI Assistant
- Follow Utopia TTRPG custom creature and item rules precisely.
- Include evocative descriptions that inspire roleplaying.
- Provide enough detail without overwhelming.

## Workflow
1. Analyze user input for key creature details.
2. Calculate stats based on selected body/kit(s)/class(es).
3. Format with proper front matter and links.
4. Review against quality checklist.
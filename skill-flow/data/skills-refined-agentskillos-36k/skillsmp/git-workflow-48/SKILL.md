---
name: git-workflow
description: Manage Git workflow for campaign content with proper commit messages and branching
license: MIT
compatibility: opencode
metadata:
  audience: campaign-managers
  workflow: jekyll
---

## What I do
- Generate descriptive commit messages following project conventions
- Create appropriate branches for content development
- Manage content publication workflow with proper staging
- Generate changelogs for campaign updates
- Coordinate multi-file commits with logical grouping
- Handle content review and approval processes

## When to use me
Use this when:
- Committing new campaign content or updates
- Preparing content for publication
- Managing collaborative development with multiple contributors
- Creating release points for campaign milestones
- Organizing content development workflow
- Reviewing and approving content changes

## Usage Examples

### Content Publication Commit
```
/skill({ name: "git-workflow" })
Operation: Commit content
Files: session-07.md, marla-mossfur.md, creeve.md
Type: Feature (new session and character updates)
Message: Auto-generated based on content changes
```

### Branch Creation
```
/skill({ name: "git-workflow" })
Operation: Create development branch
Purpose: Session 7 content development
Based on: main
Duration: Temporary for content staging
```

### Release Preparation
```
/skill({ name: "git-workflow" })
Operation: Prepare release
Version: Session 7 publication
Changelog: Generate from commits since last release
Files: All published content updates
```

## Git Operations

### Commit Message Generation
1. Analyze changed files to determine content type
2. Generate descriptive commit message following conventions
3. Categorize changes (feat, fix, docs, style, refactor, test, chore)
4. Include relevant character names and session numbers
5. Add context about campaign impact

### Branch Management
1. Create feature branches for content development
2. Merge branches after content review and approval
3. Handle branch naming conventions consistently
4. Manage branch lifecycle and cleanup
5. Coordinate parallel development streams

### Release Workflow
1. Prepare content for publication (remove draft status)
2. Generate changelog of changes since last release
3. Create tagged release points for campaign milestones
4. Handle versioning based on session numbers or content significance
5. Coordinate GitHub Pages deployment

## Commit Message Templates

### Content Creation
```
feat(sessions): Add Session 7 - Council's Decision with character development

- Session summary covering council debate and strategic choices
- Introduce new faction dynamics and character motivations
- Update cross-references between related NPCs and sessions
- Add WoodCo R&D threat escalation

Fixes #session-007
```

### Character Updates
```
feat(npcs): Develop Marla Mossfur with council leadership arc

- Expand background and political motivations
- Add relationship with Earth-Movers alliance
- Update cross-references in Sessions 5-7
- Include campaign involvement progression

Related to #council-dynamics
```

### Maintenance Operations
```
docs: Update character relationship map and faction alignments

- Reflect new alliances formed in Session 7
- Update power dynamics between Moss-Fur Clan and Earth-Movers
- Add enemy relationship changes following WoodCo escalation
- Validate link integrity across all updated articles

Prepares for session-008 content
```

## Branch Strategy

### Development Branches
- **Content Creation**: `feature/session-###-title` for new sessions
- **Character Development**: `feature/character-name` for NPC arcs
- **Faction Updates**: `feature/faction-name-rework` for major changes
- **Site Maintenance**: `fix/issue-description` for corrections
- **Asset Management**: `feature/media-organization` for image work

### Staging and Review
- **Review Branches**: `review/session-content` for approval workflow
- **Publication Staging**: `staging/publication-ready` for final content
- **Emergency Fixes**: `hotfix/urgent-issue` for immediate publication
- **Collaborative**: `team/contributor-name` for multi-author work

### Release Branches
- **Session Milestones**: `release/session-###` for major updates
- **Character Arcs**: `release/character-completion` for story arcs
- **Campaign Arcs**: `release/act-name` for major story beats
- **Site Updates**: `release/jekyll-upgrade` for platform changes

## Workflow Management

### Content Development Cycle
1. Create feature branch for new content
2. Draft content with `published: false` status
3. Update cross-references and validate links
4. Request review through pull request or internal process
5. Merge to staging after approval
6. Remove draft status for publication
7. Create release commit with changelog

### Quality Assurance Integration
1. Run `jekyll-build` validation before commits
2. Use `campaign-sync` to maintain consistency
3. Verify all links and references are functional
4. Test content display in development environment
5. Generate pre-publication reports

### Publication Process
1. Prepare content for production deployment
2. Generate appropriate changelog and release notes
3. Create tagged release for milestone tracking
4. Coordinate with GitHub Actions for automatic deployment
5. Update project documentation and guides

## Automation Features

### Smart Commit Generation
- Detect content type from file paths and names
- Generate contextual commit messages automatically
- Include relevant issue numbers or references
- Group related changes into logical commits
- Follow established project conventions

### Changelog Generation
1. Parse commit messages since last release
2. Categorize changes by type and impact
3. Generate human-readable changelog
4. Include character development summaries
5. Highlight major campaign progression points

### Release Coordination
1. Prepare content with proper front matter
2. Validate that all draft content is ready
3. Generate release notes for players/audience
4. Create version tags following project scheme
5. Coordinate with deployment pipeline

## Reports Generated

### Commit Analysis
- Change categorization and frequency
- Author contribution patterns
- Content development velocity
- Branch merging efficiency
- Code/content quality metrics

### Release Summary
- New content published in release
- Character development highlights
- Campaign progression milestones
- Known issues and limitations
- Upcoming content teasers

### Workflow Efficiency
- Time from creation to publication
- Review and approval cycle length
- Branch management overhead
- Automated process success rate
- Bottleneck identification and suggestions

Ask clarifying questions about:
- Preferred commit message conventions for this project
- How to handle collaborative content development
- Whether to use semantic versioning or session-based releases
- What content approval process to implement
- How to handle emergency content fixes or updates
---
name: content-validator
description: Validate new campaign articles for template adherence, proper links, frontmatter compliance, and consistent style
license: MIT
compatibility: opencode
metadata:
  audience: campaign-managers
  workflow: jekyll
---

## What I do
- Validate articles against campaign-specific templates and formatting standards
- Check front matter completeness and correctness for all content types
- Verify internal links use proper Jekyll `relative_url` filter
- Ensure writing style consistency with campaign voice and tone
- Generate detailed validation reports with specific fixes needed
- Auto-correct common formatting and link issues when authorized

## When to use me
Use this when:
- Creating new campaign articles of any type (sessions, NPCs, factions, enemies, organizations, info)
- Updating existing content to ensure continued compliance
- Preparing content for publication
- Reviewing content from other contributors
- Establishing quality standards for campaign maintenance

## Usage Examples

### Validate New Article
```
/skill({ name: "content-validator" })
Target: world/npcs/new-character.md
Type: Full validation (template, links, frontmatter, style)
Fix: Auto-correct minor issues, flag major ones for review
```

### Batch Validation
```
/skill({ name: "content-validator" })
Scope: All articles in _sessions/ directory
Type: Template compliance and link validation
Output: Batch report with comprehensive findings
```

### Style Consistency Check
```
/skill({ name: "content-validator" })
Target: Multiple files across different collections
Focus: Writing style, tone, and narrative voice
Options: Compare against style guide, generate consistency report
```

## Validation Dimensions

### Template Adherence
- **Structure Compliance**: Article follows correct section organization
- **Heading Hierarchy**: Proper H1 from title, H2 for main sections
- **Section Completeness**: All required sections present and properly ordered
- **Format Consistency**: Lists, bold terms, and formatting match campaign standards
- **Content Type Specifics**: Validation tailored to sessions, NPCs, factions, enemies, organizations, info articles

### Front Matter Validation
- **Required Fields**: All mandatory fields present per content type
- **YAML Syntax**: Proper indentation and formatting without errors
- **Field Values**: Correct data types and value formats
- **Optional Fields**: Appropriate use of optional front matter elements
- **Publication Status**: Proper `published: false` for drafts, removed for live content

### Link Validation
- **Internal Link Format**: All internal links use `[Text]({{ "/path/" | relative_url }})` pattern
- **File Existence**: Referenced files exist in correct directories
- **Path Accuracy**: Link paths match actual file locations
- **Reciprocal Links**: Related articles reference each other appropriately
- **Context Appropriateness**: Links make sense within article context

### Style Consistency
- **Campaign Voice**: Writing tone matches established campaign narrative style
- **Character Naming**: Consistent character name usage throughout article
- **Tense Usage**: Appropriate tense for content type (past for sessions, present for world content)
- **Formatting Patterns**: Consistent use of bolding, lists, and emphasis
- **Punctuation and Grammar**: Campaign-standard conventions followed

## Template Reference Validation

### Session Articles
```markdown
Required structure:
---
layout: page
title: Session X - Title
summary: One-line summary
index: X (integer)
act: X (integer)
tags:
    - [combat|exploration|lore|roleplay]
---

[Brief paragraph referencing key events and characters]

## Overview
[1-2 sentence overview]

## Key Characters
[List with character links and roles]

## Details
[Bulleted list of major events]

## Links
[Proper navigation and cross-references]
```

### Character Articles
```markdown
Required structure:
---
layout: page
title: Character Name
summary: Role and faction affiliation
topic: NPCs
tags:
    - [ally|neutral|antagonist]
    - [species]
    - [faction-representative]
---

[Character token image if available]

[Brief introduction paragraph]

## Overview
[Detailed character description]

## Appearance
[Bulleted physical description]

## Role and Position
[Position details and faction affiliation]

## Personality and Motivations
[Character psychology and driving forces]

## Relationships
[Allies, rivals, important connections]

## Campaign Involvement
[Character's role in story to date]

## Links
[Comprehensive cross-references]
```

### Faction Articles
```markdown
Required structure:
---
layout: page
title: The Faction Name
summary: Brief description
topic: Factions
tags:
    - faction
---

[Introductory paragraph]

## Overview
[Faction background and identity]

## Notable Members
[List of character links]

## Values
[Cultural and political values]

## Role
[Function in campaign world]

## Links
[Related content references]
```

## Auto-Correction Features

### Link Format Fixes
1. Convert bare URLs to proper `relative_url` format
2. Fix missing or incorrect filter syntax
3. Update file paths when content is moved
4. Add missing reciprocal links between related articles
5. Standardize link text and descriptions

### Front Matter Repairs
1. Add missing required fields with appropriate defaults
2. Fix YAML indentation and syntax errors
3. Standardize field ordering and formatting
4. Validate data types and correct value formats
5. Ensure consistent tag usage across similar content

### Style Standardization
1. Apply consistent character name capitalization
2. Standardize heading formatting and hierarchy
3. Fix list formatting and punctuation
4. Ensure consistent tense usage throughout article
5. Apply campaign voice and tone standards

## Validation Reports

### Article Quality Score
- **Template Adherence**: % of required structure elements present
- **Front Matter Compliance**: Valid fields and syntax rating
- **Link Integrity**: % of functional internal links
- **Style Consistency**: Match with campaign standards rating
- **Overall Quality**: Composite score with recommendations

### Issue Categorization
- **Critical Errors**: Prevent Jekyll build or content display
- **Major Issues**: Impact content quality significantly
- **Minor Issues**: Cosmetic or formatting problems
- **Style Suggestions**: Voice, tone, or convention improvements
- **Enhancement Opportunities**: Ways to improve article effectiveness

### Fix Recommendations
- **Auto-Fixed**: Issues corrected automatically
- **Manual Review**: Requiring human judgment or creative input
- **Optional Enhancements**: Improvements beyond minimum requirements
- **Best Practice Updates**: Align with latest campaign standards
- **Template Updates**: Suggests template improvements for future content

## Integration with Other Skills

### Pre-Publication Workflow
1. **content-validator**: Validate new article compliance
2. **campaign-sync**: Update cross-references if validated
3. **jekyll-build**: Test site rendering with validated content
4. **git-workflow**: Commit validated content with appropriate message

### Batch Quality Assurance
1. **content-batch**: Create multiple articles from templates
2. **content-validator**: Validate all created articles
3. **media-manager**: Ensure image references work correctly
4. **campaign-analytics**: Track quality trends over time

### Content Improvement
1. **content-validator**: Identify existing content issues
2. **update-links**: Fix broken or missing references
3. **campaign-sync**: Ensure consistency across related articles
4. **content-guide**: Apply best practices for improvements

## Quality Metrics

### Compliance Scores
- **100%**: Perfect adherence to all standards
- **90-99%**: Minor issues, publication ready
- **80-89%**: Moderate issues, needs fixes before publication
- **70-79%**: Significant issues, major revisions needed
- **<70%**: Critical issues, comprehensive overhaul required

### Consistency Tracking
- **Character Naming**: Track name usage variations and standardize
- **Link Patterns**: Monitor link format compliance trends
- **Template Evolution**: Track how templates change over time
- **Quality Improvement**: Measure content quality progression
- **Error Patterns**: Identify common validation failures

Ask clarifying questions about:
- Which validation dimensions are most important for your workflow
- Whether to auto-correct issues or flag for manual review
- How strict to be with style consistency requirements
- Whether to validate against current or historical template versions
- What quality thresholds should trigger publication approval
---
name: content-batch
description: Batch process campaign content creation and updates using templates and CSV data
license: MIT
compatibility: opencode
metadata:
  audience: campaign-managers
  workflow: jekyll
---

## What I do
- Create multiple articles in bulk from CSV data or structured input
- Apply consistent formatting and front matter across batch operations
- Generate cross-references between related content
- Update existing content with consistent changes
- Create campaign content templates for future use

## When to use me
Use this when:
- Adding multiple NPCs for a new faction
- Creating enemy entries for organization staff
- Generating session templates for campaign planning
- Bulk updating formatting across existing content
- Creating campaign content from external data sources

## Usage Examples

### Batch NPC Creation
```
/skill({ name: "content-batch" })
Operation: Create NPCs
Data Source: CSV with name, species, role, faction
Template: character-profile-standard
Options: Auto-generate cross-references
```

### Session Template Generation
```
/skill({ name: "content-batch" })
Operation: Generate templates
Target: Sessions 7-12
Template: campaign-structure
Options: Include character placeholders, plot hooks
```

### Format Standardization
```
/skill({ name: "content-batch" })
Operation: Update formatting
Target: All faction articles
Template: jekyll-standard-v2
Options: Fix front matter, standardize links
```

## Batch Operations

### CSV-Based Content Creation
1. Parse input CSV with defined column structure
2. Validate data against content type requirements
3. Generate individual articles using specified template
4. Apply consistent front matter formatting
5. Create reciprocal cross-references between related items

### Template Generation
1. Create skeleton articles for planned content
2. Include placeholder sections and front matter
3. Add comment instructions for content filling
4. Generate batch files for systematic content creation
5. Apply campaign-specific formatting patterns

### Content Updates
1. Apply formatting changes across multiple files
2. Update front matter fields consistently
3. Standardize link formatting and structure
4. Add or remove sections per template specifications
5. Maintain content relationships during updates

## CSV Data Formats

### NPC Batch Format
```csv
name,species,role,faction,personality,summary
"Thorn Quickstrike","squirrel","Scout Captain","Sky-Sailors","Aggressive but loyal leader of reconnaissance teams"
"Riverpaws","otter","Defense Coordinator","Earth-Movers","Steadfast defender of water barriers and traps"
```

### Session Batch Format
```csv
index,title,summary,act,key_characters,main_plot_points
7,"Council's Decision","The council debates response to violence",2,"Marla Mossfur, Creeve","Debate about WoodCo retaliation, choose defensive strategy"
8,"First Strike","Party conducts offensive operation",2,"Full party","Attack WoodCo convoy, gather intelligence"
```

### Enemy Batch Format
```csv
name,species,role,organization,motivation,threat_level
"Dr. Marcus","human","R&D Director","WoodCo","Magical resource exploitation","High"
"Sergeant Stone","human","Security Commander","WoodCo","Corporate enforcement","Medium"
```

## Template Types

### Character Templates
- **Standard Character**: Full NPC article with all sections
- **Minor Character**: Simplified article for brief appearances
- **Antagonist**: Enemy-focused character with threat assessment
- **Support Character**: Ally-focused with helpful capabilities

### Session Templates
- **Planning Outline**: Skeleton for upcoming sessions
- **Summary Template**: Structure for completed sessions
- **Campaign Arc**: Multi-session planning template
- **Combat Focus**: Session structure emphasizing tactical elements

### Organization Templates
- **Corporate Structure**: Business or corporation profile
- **Security Force**: Military or security group template
- **Research Facility**: Scientific organization template
- **Local Business**: Small operation or contractor template

## Batch Processing Features

### Data Validation
- CSV format validation and error reporting
- Required field checking per content type
- Consistency validation across batch
- Duplicate detection and resolution
- Field format standardization

### Content Generation
- Automatic front matter creation
- Template-based article structure
- Cross-reference generation between related items
- Placeholder image and link creation
- Draft status application for review

### Relationship Mapping
- Auto-link characters to their factions
- Connect enemies to organizations
- Reference sessions to involved characters
- Generate reciprocal links between related content
- Maintain campaign narrative consistency

## Output Management

### File Organization
- Automatic directory placement per content type
- Consistent naming conventions
- Sequential numbering for indexed content
- Backup creation for existing files
- Conflict resolution for duplicate names

### Quality Assurance
- Template application validation
- Link syntax checking
- Front matter completeness verification
- Markdown formatting validation
- Cross-reference integrity testing

## Reports Generated

### Batch Operation Summary
- Number of articles created/updated
- Processing time and performance metrics
- Error report with specific file references
- Validation warnings and recommendations
- Next steps for content publication

### Data Quality Report
- CSV parsing statistics and issues
- Field validation results
- Duplicate content detection
- Relationship mapping summary
- Template application success rate

Ask clarifying questions about:
- CSV structure and column definitions
- Template customization requirements
- Handling of data conflicts or duplicates
- Cross-reference generation preferences
- Publication workflow for batch-generated content
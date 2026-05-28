---
name: campaign-sync
description: Sync campaign content and update cross-references between sessions, NPCs, and related articles
license: MIT
compatibility: opencode
metadata:
  audience: campaign-managers
  workflow: jekyll
---

## What I do
- Update cross-references between sessions, NPCs, factions, enemies, and organizations
- Ensure consistent character naming across all campaign content
- Validate that all internal links are properly formatted and functional
- Update session indices and act numbering when new sessions are added
- Generate relationship maps between campaign elements

## When to use me
Use this when:
- Adding new session content that mentions existing NPCs or factions
- Creating new character articles that should be referenced in existing sessions
- Updating character names or relationships across multiple articles
- Verifying campaign content consistency before publication
- Preparing campaign updates or housekeeping

## Usage Examples

### Sync New Session Content
```
/skill({ name: "campaign-sync" })
Target session: session-07-councils-decision
New characters mentioned: Marla Mossfur, Creeve, Dr. Lyle
New organizations: WoodCo R&D Division
Action: Update cross-references and add reciprocal links
```

### Update Character Relationships
```
/skill({ name: "campaign-sync" })
Character update: Marla Mossfur
New relationship: alliance with Earth-Movers
Update locations: All faction relationships, council session mentions
Action: Update related articles with new alliance information
```

### Validate Campaign Consistency
```
/skill({ name: "campaign-sync" })
Scope: Full campaign validation
Focus: Character naming consistency, link integrity, timeline accuracy
Action: Generate consistency report and fix common issues
```

## Analysis Operations

### Content Scanning
- Parse all `.md` files in `_world/` and `_sessions/` directories
- Extract character names, faction affiliations, and cross-references
- Identify broken internal links or formatting inconsistencies
- Track session chronology and character appearances

### Relationship Mapping
- Map character-to-faction relationships
- Track enemy-to-organization affiliations
- Maintain session-to-character appearance records
- Identify missing cross-references between related content

### Consistency Checking
- Verify character names match across all articles
- Check faction alignments remain consistent
- Validate session numbers follow sequential order
- Ensure all internal links use proper Jekyll `relative_url` filter

## Update Operations

### Cross-Reference Addition
When new content references existing elements:
1. Add links to referenced characters/factions in new content
2. Update referenced articles to mention the new content
3. Maintain reciprocal linking between related items
4. Ensure proper formatting with `relative_url` filter

### Link Validation and Repair
1. Check all internal links follow pattern `[Text]({{ "/path/" | relative_url }})`
2. Verify referenced files exist in expected directories
3. Fix broken links by correcting paths or removing dead references
4. Update paths when content is moved between directories

### Timeline Consistency
1. Verify session `index` numbers are sequential
2. Check character appearances follow logical timeline
3. Update session `act` assignments based on content progression
4. Flag timeline inconsistencies for GM review

## Reports Generated

### Consistency Report
- Character name mismatches across articles
- Missing cross-references between related content
- Broken internal links or formatting errors
- Timeline and sequence inconsistencies

### Relationship Summary
- Character-to-faction mapping
- Enemy-to-organization affiliations
- Session appearance chronology
- Missing reciprocal references

### Publication Checklist
- All required front matter fields present
- Internal links properly formatted
- Cross-references complete and reciprocal
- Draft status correctly set for new content

Ask clarifying questions about:
- Which content elements should be linked together
- Whether to fix discovered inconsistencies automatically
- How to handle conflicting character information
- Which timeline takes precedence when inconsistencies found